import pyttsx3
import threading
from config import Config

class TTSHandler:
    def __init__(self):
        self.config = Config()
        self.engine = pyttsx3.init()
        self.speaking = False
        self.current_thread = None
        self.stop_requested = False
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
            
            # Set voice based on language preference
            self.set_voice_by_language()
        except Exception as e:
            print(f"Error setting up TTS voice: {e}")
    
    def set_voice_by_language(self):
        """Set voice based on configured language"""
        try:
            language = self.config.get('Audio', 'language', 'en-US')
            voices = self.engine.getProperty('voices')
            
            if not voices:
                print("No TTS voices available")
                return
            
            # Language code to voice selection mapping
            language_keywords = {
                'tr-TR': ['turkish', 'türkçe', 'turk', 'tr'],
                'en-US': ['english', 'united states', 'us', 'american'],
                'en-GB': ['english', 'united kingdom', 'british', 'gb'],
                'es-ES': ['spanish', 'español', 'spain', 'es'],
                'fr-FR': ['french', 'français', 'france', 'fr'],
                'de-DE': ['german', 'deutsch', 'germany', 'de'],
                'it-IT': ['italian', 'italiano', 'italy', 'it'],
                'pt-PT': ['portuguese', 'português', 'portugal', 'pt'],
                'ru-RU': ['russian', 'русский', 'russia', 'ru']
            }
            
            # Try to find a voice that matches the language
            keywords = language_keywords.get(language, language_keywords['en-US'])
            selected_voice = None
            
            for voice in voices:
                voice_name = voice.name.lower()
                for keyword in keywords:
                    if keyword in voice_name:
                        selected_voice = voice
                        break
                if selected_voice:
                    break
            
            # If no matching voice found, use the first available
            if not selected_voice:
                selected_voice = voices[0]
                print(f"No {language} voice found, using default: {selected_voice.name}")
            else:
                print(f"Selected {language} voice: {selected_voice.name}")
            
            self.engine.setProperty('voice', selected_voice.id)
        except Exception as e:
            print(f"Error setting voice by language: {e}")
    
    def speak(self, text, blocking=True):
        """Speak the given text"""
        try:
            if not text:
                return
            
            # Stop any current speech
            self.stop()
            
            if blocking:
                self.speaking = True
                self.stop_requested = False
                self.engine.say(text)
                self.engine.runAndWait()
                self.speaking = False
            else:
                # Run in separate thread for non-blocking speech
                self.current_thread = threading.Thread(target=self._speak_async, args=(text,))
                self.current_thread.daemon = True
                self.current_thread.start()
        except Exception as e:
            print(f"Error speaking text: {e}")
            self.speaking = False
    
    def _speak_async(self, text):
        """Async method for non-blocking speech"""
        try:
            self.speaking = True
            self.stop_requested = False
            
            # Split text into smaller chunks to allow for interruption
            sentences = text.split('. ')
            
            for sentence in sentences:
                if self.stop_requested:
                    print("TTS interrupted by stop request")
                    break
                    
                if sentence.strip():
                    # Add period back if it was removed by split
                    if not sentence.endswith('.') and sentence != sentences[-1]:
                        sentence += '.'
                    
                    self.engine.say(sentence)
                    self.engine.runAndWait()
            
            self.speaking = False
        except Exception as e:
            print(f"Error in async speech: {e}")
            self.speaking = False
    
    def stop(self):
        """Stop current speech immediately"""
        try:
            if self.speaking:
                print("Stopping TTS immediately...")
                self.stop_requested = True
                self.engine.stop()
                
                # Wait briefly for the current speech to stop
                if self.current_thread and self.current_thread.is_alive():
                    self.current_thread.join(timeout=0.5)
                
                self.speaking = False
                print("TTS stopped successfully")
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
    
    def refresh_voice_settings(self):
        """Refresh voice settings based on current configuration"""
        try:
            self.config.load_config()
            self.set_voice_by_language()
        except Exception as e:
            print(f"Error refreshing voice settings: {e}") 