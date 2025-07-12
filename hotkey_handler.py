import keyboard
import threading
from config import Config

class HotkeyHandler:
    def __init__(self, main_app):
        self.main_app = main_app
        self.config = Config()
        self.current_hotkey = None
        self.is_listening = False
        self.hotkey_thread = None
        
    def start_listening(self):
        """Start listening for global hotkeys"""
        if self.is_listening:
            return
        
        self.is_listening = True
        self.current_hotkey = self.config.get_hotkey()
        
        try:
            # Register the hotkey
            keyboard.add_hotkey(self.current_hotkey, self.on_hotkey_pressed)
            print(f"Hotkey registered: {self.current_hotkey}")
            
            # Start the keyboard listener in a separate thread
            self.hotkey_thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.hotkey_thread.start()
            
        except Exception as e:
            print(f"Error setting up hotkey: {e}")
            self.is_listening = False
    
    def stop_listening(self):
        """Stop listening for global hotkeys"""
        if not self.is_listening:
            return
            
        self.is_listening = False
        
        try:
            # Unregister the hotkey
            if self.current_hotkey:
                keyboard.remove_hotkey(self.current_hotkey)
                print(f"Hotkey unregistered: {self.current_hotkey}")
        except Exception as e:
            print(f"Error removing hotkey: {e}")
    
    def _listen_loop(self):
        """Main listening loop for keyboard events"""
        try:
            while self.is_listening:
                # This will block and wait for keyboard events
                keyboard.wait()
                if not self.is_listening:
                    break
        except Exception as e:
            print(f"Error in hotkey listening loop: {e}")
    
    def on_hotkey_pressed(self):
        """Handle hotkey press event"""
        print(f"Hotkey pressed: {self.current_hotkey}")
        
        try:
            # Call the main app's hotkey handler in a separate thread
            if self.main_app:
                threading.Thread(target=self.main_app.handle_hotkey, daemon=True).start()
        except Exception as e:
            print(f"Error handling hotkey press: {e}")
    
    def update_hotkey(self):
        """Update the hotkey configuration"""
        new_hotkey = self.config.get_hotkey()
        
        if new_hotkey != self.current_hotkey:
            print(f"Updating hotkey from {self.current_hotkey} to {new_hotkey}")
            
            # Stop current listening
            self.stop_listening()
            
            # Start with new hotkey
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