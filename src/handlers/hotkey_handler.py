import keyboard
import threading
import time
from src.core.config import Config

class HotkeyHandler:
    def __init__(self, main_app):
        self.main_app = main_app
        self.config = Config()
        self.current_hotkey = None
        self.current_stop_hotkey = None
        self.is_listening = False
        self.hotkey_pressed = False
        self.stop_hotkey_pressed = False
        self.hotkey_keys = []
        self.stop_hotkey_keys = []
        self.monitor_thread = None
        
    def start_listening(self):
        """Start listening for global hotkeys"""
        if self.is_listening:
            return
        
        self.is_listening = True
        self.current_hotkey = self.config.get_hotkey()
        self.current_stop_hotkey = self.config.get_stop_speaking_hotkey()
        
        try:
            # Parse the hotkey combinations
            self.hotkey_keys = self._parse_hotkey_combination(self.current_hotkey)
            self.stop_hotkey_keys = self._parse_hotkey_combination(self.current_stop_hotkey)
            
            print(f"Push-to-talk hotkey registered: {self.current_hotkey}")
            print(f"Stop speaking hotkey registered: {self.current_stop_hotkey}")
            
            # Start monitoring thread
            self.monitor_thread = threading.Thread(target=self._monitor_keys, daemon=True)
            self.monitor_thread.start()
            
        except Exception as e:
            print(f"Error setting up hotkey: {e}")
            self.is_listening = False
    
    def stop_listening(self):
        """Stop listening for global hotkeys"""
        if not self.is_listening:
            return
            
        self.is_listening = False
        
        try:
            # Wait for monitor thread to finish
            if self.monitor_thread:
                self.monitor_thread.join(timeout=1.0)
            print(f"Push-to-talk hotkey unregistered: {self.current_hotkey}")
        except Exception as e:
            print(f"Error removing hotkey: {e}")
    
    def _monitor_keys(self):
        """Monitor hotkey states continuously"""
        try:
            while self.is_listening:
                try:
                    # Check main hotkey (push-to-talk)
                    main_keys_pressed = self._are_keys_pressed(self.hotkey_keys)
                    
                    if main_keys_pressed and not self.hotkey_pressed:
                        # Main hotkey just pressed
                        self.hotkey_pressed = True
                        print(f"Hotkey pressed - starting capture and recording: {self.current_hotkey}")
                        self._on_hotkey_press()
                    elif not main_keys_pressed and self.hotkey_pressed:
                        # Main hotkey just released
                        self.hotkey_pressed = False
                        print(f"Hotkey released - stopping recording: {self.current_hotkey}")
                        self._on_hotkey_release()
                    
                    # Check stop speaking hotkey
                    stop_keys_pressed = self._are_keys_pressed(self.stop_hotkey_keys)
                    
                    if stop_keys_pressed and not self.stop_hotkey_pressed:
                        # Stop speaking hotkey just pressed
                        self.stop_hotkey_pressed = True
                        print(f"Stop speaking hotkey pressed: {self.current_stop_hotkey}")
                        self._on_stop_speaking_press()
                    elif not stop_keys_pressed and self.stop_hotkey_pressed:
                        # Stop speaking hotkey just released
                        self.stop_hotkey_pressed = False
                    
                    # Sleep briefly to avoid excessive CPU usage
                    time.sleep(0.05)  # 50ms polling interval
                    
                except Exception as e:
                    print(f"Error in key monitoring: {e}")
                    time.sleep(0.1)
                    
        except Exception as e:
            print(f"Error in key monitoring thread: {e}")
    
    def _parse_hotkey_combination(self, hotkey_string):
        """Parse hotkey combination into individual keys"""
        try:
            # Convert hotkey string to list of keys
            keys = []
            parts = hotkey_string.lower().split('+')
            
            for part in parts:
                part = part.strip()
                if part == 'ctrl':
                    keys.append('ctrl')
                elif part == 'alt':
                    keys.append('alt')
                elif part == 'shift':
                    keys.append('shift')
                else:
                    keys.append(part)
            
            return keys
        except Exception as e:
            print(f"Error parsing hotkey: {e}")
            return []
    
    def _are_keys_pressed(self, keys):
        """Check if all specified keys are currently pressed"""
        try:
            for key in keys:
                if key == 'ctrl' and not (keyboard.is_pressed('ctrl') or keyboard.is_pressed('left ctrl') or keyboard.is_pressed('right ctrl')):
                    return False
                elif key == 'alt' and not (keyboard.is_pressed('alt') or keyboard.is_pressed('left alt') or keyboard.is_pressed('right alt')):
                    return False
                elif key == 'shift' and not (keyboard.is_pressed('shift') or keyboard.is_pressed('left shift') or keyboard.is_pressed('right shift')):
                    return False
                elif key not in ['ctrl', 'alt', 'shift'] and not keyboard.is_pressed(key):
                    return False
            return True
        except Exception as e:
            print(f"Error checking key states: {e}")
            return False
    
    def _on_hotkey_press(self):
        """Handle hotkey press event"""
        print(f"Hotkey pressed - starting capture and recording: {self.current_hotkey}")
        
        try:
            # Call the main app's hotkey press handler
            if self.main_app:
                threading.Thread(target=self.main_app.handle_hotkey_press, daemon=True).start()
        except Exception as e:
            print(f"Error handling hotkey press: {e}")
    
    def _on_hotkey_release(self):
        """Handle hotkey release event"""
        print(f"Hotkey released - stopping recording: {self.current_hotkey}")
        
        try:
            # Call the main app's hotkey release handler
            if self.main_app:
                threading.Thread(target=self.main_app.handle_hotkey_release, daemon=True).start()
        except Exception as e:
            print(f"Error handling hotkey release: {e}")
    
    def _on_stop_speaking_press(self):
        """Handle stop speaking hotkey press event"""
        print(f"Stop speaking hotkey pressed: {self.current_stop_hotkey}")
        
        try:
            # Call the main app's stop speaking handler
            if self.main_app:
                threading.Thread(target=self.main_app.handle_stop_speaking, daemon=True).start()
        except Exception as e:
            print(f"Error handling stop speaking hotkey: {e}")
    
    def update_hotkey(self):
        """Update the hotkey configuration"""
        new_hotkey = self.config.get_hotkey()
        new_stop_hotkey = self.config.get_stop_speaking_hotkey()
        
        if new_hotkey != self.current_hotkey or new_stop_hotkey != self.current_stop_hotkey:
            print(f"Updating hotkeys from {self.current_hotkey}/{self.current_stop_hotkey} to {new_hotkey}/{new_stop_hotkey}")
            
            # Stop current listening
            self.stop_listening()
            
            # Start with new hotkeys
            self.start_listening()
    
    def is_valid_hotkey(self, hotkey_string):
        """Check if a hotkey string is valid"""
        try:
            # Try to parse the hotkey string
            keyboard.parse_hotkey(hotkey_string)
            return True
        except Exception:
            return False
    
    def get_available_hotkeys(self):
        """Get a list of suggested hotkey combinations"""
        return [
            "ctrl+shift+s",
            "ctrl+alt+s", 
            "ctrl+shift+a",
            "alt+shift+s",
            "ctrl+shift+q",
            "ctrl+alt+q",
            "ctrl+shift+w",
            "alt+shift+w"
        ] 