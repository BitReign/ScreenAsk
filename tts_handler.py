import pyttsx3
import threading
from config import Config

class TTSHandler:
    def __init__(self):
        self.config = Config()
        self.engine = pyttsx3.init()
        self.setup_voice()
        
    def setup_voice(self):
        """Setup TTS voice properties"""
        try:
            # Set speech rate
            rate = int(self.config.get('TTS', 'rate', '200'))
            self.engine.setProperty('rate', rate)
            
            # Set volume
            volume = float(self.config.get('TTS', 'volume', '0.8'))
            self.engine.setProperty('volume', volume)
            
            # Set voice (try to use first available voice)
            voices = self.engine.getProperty('voices')
            if voices:
                self.engine.setProperty('voice', voices[0].id)
        except Exception as e:
            print(f"Error setting up TTS voice: {e}")
    
    def speak(self, text, blocking=True):
        """Speak the given text"""
        try:
            if not text:
                return
            
            if blocking:
                self.engine.say(text)
                self.engine.runAndWait()
            else:
                # Run in separate thread for non-blocking speech
                thread = threading.Thread(target=self._speak_async, args=(text,))
                thread.daemon = True
                thread.start()
        except Exception as e:
            print(f"Error speaking text: {e}")
    
    def _speak_async(self, text):
        """Async method for non-blocking speech"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error in async speech: {e}")
    
    def stop(self):
        """Stop current speech"""
        try:
            self.engine.stop()
        except Exception as e:
            print(f"Error stopping TTS: {e}")
    
    def set_rate(self, rate):
        """Set speech rate"""
        try:
            self.engine.setProperty('rate', rate)
            self.config.set('TTS', 'rate', rate)
        except Exception as e:
            print(f"Error setting TTS rate: {e}")
    
    def set_volume(self, volume):
        """Set speech volume (0.0 to 1.0)"""
        try:
            self.engine.setProperty('volume', volume)
            self.config.set('TTS', 'volume', volume)
        except Exception as e:
            print(f"Error setting TTS volume: {e}")
    
    def get_voices(self):
        """Get available voices"""
        try:
            voices = self.engine.getProperty('voices')
            return [(voice.id, voice.name) for voice in voices] if voices else []
        except Exception as e:
            print(f"Error getting voices: {e}")
            return []
    
    def set_voice(self, voice_id):
        """Set voice by ID"""
        try:
            self.engine.setProperty('voice', voice_id)
        except Exception as e:
            print(f"Error setting voice: {e}") 