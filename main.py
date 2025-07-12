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

class ScreenAskApp:
    def __init__(self):
        self.config = Config()
        self.running = False
        
        # Initialize handlers
        self.screenshot_handler = ScreenshotHandler()
        self.audio_handler = AudioHandler()
        self.openai_handler = OpenAIHandler()
        self.tts_handler = TTSHandler()
        
        # Initialize UI components
        self.main_gui = MainGUI(self)
        self.tray_handler = TrayHandler(self)
        self.hotkey_handler = HotkeyHandler(self)
        
        # Processing flag to prevent multiple simultaneous captures
        self.processing = False
        
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
        self.tray_handler.set_tooltip("ScreenAsk - Press {} to capture".format(self.config.get_hotkey()))
        
        print("ScreenAsk started successfully!")
        print(f"Hotkey: {self.config.get_hotkey()}")
        
        # Check if OpenAI is configured
        if not self.openai_handler.is_configured():
            self.tray_handler.notify("ScreenAsk", "Please configure your OpenAI API key in settings")
        
        # Start the main loop
        try:
            self.main_gui.root.mainloop()
        except KeyboardInterrupt:
            self.quit()
    
    def handle_hotkey(self):
        """Handle hotkey press - main functionality"""
        if self.processing:
            print("Already processing, ignoring hotkey")
            return
            
        self.processing = True
        
        try:
            print("Hotkey triggered - starting capture process...")
            
            # Show notification
            self.tray_handler.notify("ScreenAsk", "Capturing screenshot and listening for audio...")
            
            # Step 1: Capture screenshot
            print("Capturing screenshot...")
            screenshot_base64 = self.screenshot_handler.capture_screenshot()
            
            if not screenshot_base64:
                self.tray_handler.notify("ScreenAsk", "Failed to capture screenshot")
                return
            
            print("Screenshot captured successfully")
            
            # Step 2: Record audio
            print("Recording audio...")
            self.tray_handler.notify("ScreenAsk", "Say your question now...")
            
            # Use the direct listening method for real-time audio
            user_text = self.audio_handler.listen_for_speech(timeout=10)
            
            if not user_text:
                print("No audio detected or transcription failed")
                user_text = None
            else:
                print(f"Transcribed text: {user_text}")
            
            # Step 3: Send to OpenAI
            print("Sending to OpenAI...")
            self.tray_handler.notify("ScreenAsk", "Analyzing with AI...")
            
            if not self.openai_handler.is_configured():
                self.tray_handler.notify("ScreenAsk", "OpenAI API not configured")
                return
            
            response = self.openai_handler.analyze_screenshot_with_text(screenshot_base64, user_text)
            
            if response.startswith("Error"):
                print(f"OpenAI error: {response}")
                self.tray_handler.notify("ScreenAsk", "AI analysis failed")
                return
            
            print(f"OpenAI response: {response}")
            
            # Step 4: Speak the response
            print("Speaking response...")
            self.tray_handler.notify("ScreenAsk", "Speaking response...")
            
            self.tts_handler.speak(response, blocking=False)
            
            print("Process completed successfully!")
            
        except Exception as e:
            print(f"Error in hotkey handler: {e}")
            self.tray_handler.notify("ScreenAsk", f"Error: {str(e)}")
        finally:
            self.processing = False
    
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
            self.tray_handler.set_tooltip("ScreenAsk - Press {} to capture".format(self.config.get_hotkey()))
        
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