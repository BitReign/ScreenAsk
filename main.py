import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox

from config import Config
from tray_handler import TrayHandler
from main_gui import MainGUI
from hotkey_handler import HotkeyHandler
from screenshot_handler import ScreenshotHandler
from audio_handler import AudioHandler
from openai_handler import OpenAIHandler
from tts_handler import TTSHandler
from poi_handler import POIHandler
from circle_overlay import CircleOverlay

class ScreenAskApp:
    def __init__(self):
        self.config = Config()
        self.running = False
        
        # Initialize handlers
        self.screenshot_handler = ScreenshotHandler()
        self.audio_handler = AudioHandler()
        self.openai_handler = OpenAIHandler()
        self.tts_handler = TTSHandler()
        self.poi_handler = POIHandler()
        self.circle_overlay = CircleOverlay(self.config)
        
        # Initialize UI components
        self.main_gui = MainGUI(self)
        self.tray_handler = TrayHandler(self)
        self.hotkey_handler = HotkeyHandler(self)
        
        # Processing flag to prevent multiple simultaneous captures
        self.processing = False
        
        # Store current screenshot for processing
        self.current_screenshot = None
        
    def start(self):
        """Start the application"""
        self.running = True
        
        print("Starting ScreenAsk...")
        
        # Start the main GUI
        self.main_gui.create_main_window()
        
        # Start the system tray
        self.tray_handler.start_tray()
        
        # Start hotkey listening
        self.hotkey_handler.start_listening()
        
        # Set initial tray tooltip
        if self.config.get_audio_recording_enabled():
            self.tray_handler.set_tooltip("ScreenAsk - Hold {} to record, {} to stop speaking".format(
                self.config.get_hotkey(), self.config.get_stop_speaking_hotkey()))
        else:
            self.tray_handler.set_tooltip("ScreenAsk - Press {} to analyze screen, {} to stop speaking".format(
                self.config.get_hotkey(), self.config.get_stop_speaking_hotkey()))
        
        print("ScreenAsk started successfully!")
        print(f"Hotkey: {self.config.get_hotkey()}")
        
        # Set initial status
        if self.main_gui:
            self.main_gui.set_status_ready()
        
        # Check if OpenAI is configured
        if not self.openai_handler.is_configured():
            self.tray_handler.notify("ScreenAsk", "Please configure your OpenAI API key in settings")
        
        # Start the main loop
        try:
            self.main_gui.root.mainloop()
        except KeyboardInterrupt:
            self.quit()
    
    def handle_hotkey_press(self):
        """Handle hotkey press - start recording"""
        if self.processing:
            print("Already processing, ignoring hotkey press")
            return
            
        self.processing = True
        
        try:
            # Check if audio recording is enabled
            audio_enabled = self.config.get_audio_recording_enabled()
            
            if audio_enabled:
                print("Hotkey pressed - starting capture and recording...")
                # Update status to recording
                if self.main_gui:
                    self.main_gui.set_status_recording()
                # Show notification
                self.tray_handler.notify("ScreenAsk", "Hold key and speak your question...")
            else:
                print("Hotkey pressed - capturing screenshot (audio disabled)...")
                # Update status to processing since we'll process immediately
                if self.main_gui:
                    self.main_gui.set_status_processing()
                # Show notification
                self.tray_handler.notify("ScreenAsk", "Analyzing screenshot...")
            
            # Step 1: Capture screenshot
            print("Capturing screenshot...")
            screenshot_base64 = self.screenshot_handler.capture_screenshot()
            
            if not screenshot_base64:
                self.tray_handler.notify("ScreenAsk", "Failed to capture screenshot")
                if self.main_gui:
                    self.main_gui.set_status_ready()
                self.processing = False
                return
            
            print("Screenshot captured successfully")
            
            # Store screenshot for processing
            self.current_screenshot = screenshot_base64
            
            if audio_enabled:
                # Step 2: Start recording audio
                print("Starting audio recording...")
                self.audio_handler.start_recording()
            else:
                # Process immediately without audio
                print("Processing without audio recording...")
                self._process_screenshot_only()
            
        except Exception as e:
            print(f"Error in hotkey press handler: {e}")
            self.tray_handler.notify("ScreenAsk", f"Error: {str(e)}")
            if self.main_gui:
                self.main_gui.set_status_ready()
            self.processing = False
    
    def handle_hotkey_release(self):
        """Handle hotkey release - stop recording and process"""
        if not self.processing:
            print("Not currently processing, ignoring hotkey release")
            return
        
        # Check if audio recording is enabled
        audio_enabled = self.config.get_audio_recording_enabled()
        
        if not audio_enabled:
            print("Audio disabled - hotkey release ignored")
            return
        
        try:
            print("Hotkey released - stopping recording and processing...")
            
            # Step 1: Stop recording
            print("Stopping audio recording...")
            if self.main_gui:
                self.main_gui.set_status_processing()
            self.audio_handler.stop_recording()
            
            # Step 2: Process the recorded audio
            print("Processing recorded audio...")
            self.tray_handler.notify("ScreenAsk", "Processing your question...")
            
            # Save and transcribe the audio
            filename = self.audio_handler.save_recording()
            user_text = None
            
            if filename:
                user_text = self.audio_handler.transcribe_audio(filename)
                
                if not user_text:
                    print("No audio detected or transcription failed")
                    user_text = None
                else:
                    print(f"Transcribed text: {user_text}")
            
            # Step 3: Send to OpenAI with audio text
            self._process_with_openai(user_text)
            
        except Exception as e:
            print(f"Error in hotkey release handler: {e}")
            self.tray_handler.notify("ScreenAsk", f"Error: {str(e)}")
            if self.main_gui:
                self.main_gui.set_status_ready()
        finally:
            self.processing = False
            self.current_screenshot = None
    
    def _process_screenshot_only(self):
        """Process screenshot without audio recording"""
        try:
            # Process immediately without user audio text
            self._process_with_openai(None)
        except Exception as e:
            print(f"Error in screenshot-only processing: {e}")
            self.tray_handler.notify("ScreenAsk", f"Error: {str(e)}")
            if self.main_gui:
                self.main_gui.set_status_ready()
        finally:
            self.processing = False
            self.current_screenshot = None
    
    def _process_with_openai(self, user_text):
        """Send to OpenAI and handle response"""
        print("Sending to OpenAI...")
        if self.main_gui:
            self.main_gui.set_status_analyzing()
        self.tray_handler.notify("ScreenAsk", "Analyzing with AI...")
        
        if not self.openai_handler.is_configured():
            self.tray_handler.notify("ScreenAsk", "OpenAI API not configured")
            if self.main_gui:
                self.main_gui.set_status_ready()
            return
        
        response = self.openai_handler.analyze_screenshot_with_text(self.current_screenshot, user_text)
        
        if response.startswith("Error"):
            print(f"OpenAI error: {response}")
            self.tray_handler.notify("ScreenAsk", "AI analysis failed")
            if self.main_gui:
                self.main_gui.set_status_ready()
            return
        
        print(f"OpenAI response: {response}")
        
        # Parse structured response (always enabled)
        structured_data, error = self.openai_handler.parse_structured_response(response)
        
        if error:
            print(f"Error parsing structured response: {error}")
            print(f"Raw response: {response}")
            self.tray_handler.notify("ScreenAsk", "Error parsing AI response")
            if self.main_gui:
                self.main_gui.set_status_ready()
            return
        
        # Extract structured data
        poi_x = structured_data['x']
        poi_y = structured_data['y']
        poi_radius = structured_data['r']
        text_response = structured_data['tx']
        
        print(f"Structured response - POI: ({poi_x}, {poi_y}), Radius: {poi_radius}")
        print(f"Text to speak: {text_response}")
        
        # Add screen resolution info for debugging
        if self.main_gui and self.main_gui.root:
            try:
                screen_width = self.main_gui.root.winfo_screenwidth()
                screen_height = self.main_gui.root.winfo_screenheight()
                print(f"Screen resolution: {screen_width}x{screen_height}")
                print(f"POI relative position: {poi_x/screen_width:.1%} from left, {poi_y/screen_height:.1%} from top")
                
                # Verify coordinates are within screen bounds
                if poi_x < 0 or poi_x > screen_width or poi_y < 0 or poi_y > screen_height:
                    print(f"⚠️  WARNING: POI coordinates ({poi_x}, {poi_y}) are outside screen bounds!")
                else:
                    print(f"✅ POI coordinates are within screen bounds")
                
                # Give context about screen regions
                region_x = "left" if poi_x < screen_width/3 else ("center" if poi_x < 2*screen_width/3 else "right")
                region_y = "top" if poi_y < screen_height/3 else ("middle" if poi_y < 2*screen_height/3 else "bottom")
                print(f"📍 POI is in {region_y}-{region_x} region of screen")
                
            except:
                pass
        
        # Store POI data using POI handler
        self.poi_handler.set_current_poi(poi_x, poi_y, poi_radius, text_response)
        
        # Show circle overlay if enabled
        if self.config.get_circle_overlay_enabled():
            print(f"Showing circle overlay at ({poi_x}, {poi_y}) with radius {poi_radius}")
            self.circle_overlay.show_circle(poi_x, poi_y, poi_radius)
        
        # Speak only the text portion
        self._speak_response(text_response)
            
        print("Process completed successfully!")
    
    def _speak_response(self, text):
        """Speak the response text"""
        print("Speaking response...")
        if self.main_gui:
            self.main_gui.set_status_speaking()
        self.tray_handler.notify("ScreenAsk", "Speaking response...")
        
        self.tts_handler.speak(text, blocking=False)
        
        # Set status back to ready after a short delay
        import time
        threading.Timer(2.0, lambda: self.main_gui.set_status_ready() if self.main_gui else None).start()
    
    def get_current_poi_data(self):
        """Get the current point of interest data"""
        return self.poi_handler.get_current_poi()
    
    def get_poi_in_user_format(self):
        """Get POI data in user's requested format: x:10,y:50,r:300,tx="text" """
        return self.poi_handler.export_poi_data('simple')
    
    def get_poi_as_json(self):
        """Get POI data as JSON"""
        return self.poi_handler.export_poi_data('json')
    
    def test_circle_at_coordinates(self, x, y, radius=100):
        """Test circle overlay at specific coordinates (for debugging)"""
        if self.circle_overlay:
            print(f"Testing circle overlay at ({x}, {y}) with radius {radius}")
            self.circle_overlay.show_circle(x, y, radius)
        else:
            print("Circle overlay not available")

    def test_coordinate_accuracy(self):
        """Test coordinate accuracy by showing multiple circles at different locations"""
        if not self.circle_overlay:
            print("Circle overlay not available")
            return
        
        # Test coordinates for common taskbar positions
        screen_width = 2560  # Your screen width
        screen_height = 1440  # Your screen height
        
        # Test different taskbar positions
        test_positions = [
            (200, 1400, 30, "Far left of taskbar"),
            (640, 1400, 30, "Left-center of taskbar"),
            (1280, 1400, 30, "Center of taskbar"),
            (1920, 1400, 30, "Right-center of taskbar"),
            (2400, 1400, 30, "Far right of taskbar"),
        ]
        
        print("Testing coordinate accuracy at different taskbar positions:")
        for x, y, radius, description in test_positions:
            print(f"  Testing {description}: ({x}, {y}) with radius {radius}")
            input("Press Enter to show circle...")
            self.circle_overlay.show_circle(x, y, radius)
            
    def clear_coordinate_cache(self):
        """Clear cached coordinates to force fresh detection"""
        if hasattr(self.openai_handler, 'coordinate_cache'):
            self.openai_handler.coordinate_cache.clear()
            print("Coordinate cache cleared - next request will generate fresh coordinates")
        else:
            print("No coordinate cache found")
    
    def hide_current_circle(self):
        """Hide current circle overlay"""
        if self.circle_overlay:
            self.circle_overlay.hide_circle()
    
    def handle_stop_speaking(self):
        """Handle stop speaking hotkey - stop TTS immediately"""
        try:
            print("Stop speaking hotkey pressed - stopping TTS...")
            if self.tts_handler:
                self.tts_handler.stop()
                print("TTS stopped successfully")
                
                # Update status back to ready
                if self.main_gui:
                    self.main_gui.set_status_ready()
                
                # Show notification
                self.tray_handler.notify("ScreenAsk", "Speech stopped")
                
        except Exception as e:
            print(f"Error stopping TTS: {e}")
    
    def show_main_window(self):
        """Show the main application window"""
        if self.main_gui:
            self.main_gui.show_window()
    
    def show_settings(self):
        """Show settings window"""
        if self.main_gui:
            # Make sure main window is available first
            if not self.main_gui.root or not self.main_gui.root.winfo_exists():
                self.show_main_window()
            self.main_gui.show_settings()
    
    def update_hotkey(self):
        """Update hotkey configuration"""
        if self.hotkey_handler:
            self.hotkey_handler.update_hotkey()
            if self.config.get_audio_recording_enabled():
                self.tray_handler.set_tooltip("ScreenAsk - Hold {} to record, {} to stop speaking".format(
                    self.config.get_hotkey(), self.config.get_stop_speaking_hotkey()))
            else:
                self.tray_handler.set_tooltip("ScreenAsk - Press {} to analyze screen, {} to stop speaking".format(
                    self.config.get_hotkey(), self.config.get_stop_speaking_hotkey()))
        
        # Also reload OpenAI configuration
        if self.openai_handler:
            self.openai_handler.setup_client()
    
    def quit(self):
        """Quit the application"""
        print("Shutting down ScreenAsk...")
        self.running = False
        
        # Stop components
        if self.hotkey_handler:
            self.hotkey_handler.stop_listening()
        
        if self.tray_handler:
            self.tray_handler.stop_tray()
        
        if self.tts_handler:
            self.tts_handler.stop()
        
        if self.circle_overlay:
            self.circle_overlay.hide_circle()
        
        if self.main_gui and self.main_gui.root:
            self.main_gui.root.quit()
        
        print("ScreenAsk shutdown complete")
        sys.exit(0)

def main():
    """Main entry point"""
    try:
        app = ScreenAskApp()
        app.start()
    except Exception as e:
        print(f"Fatal error: {e}")
        # Show error dialog if possible
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("ScreenAsk Error", f"Fatal error starting application:\n{e}")
            root.destroy()
        except:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main() 