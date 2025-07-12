import configparser
import os

class Config:
    def __init__(self):
        self.config_file = "settings.ini"
        self.config = configparser.ConfigParser()
        self.load_config()
    
    def load_config(self):
        """Load configuration from file or create default if it doesn't exist"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        else:
            self.create_default_config()
    
    def create_default_config(self):
        """Create default configuration"""
        self.config['General'] = {
            'hotkey': 'ctrl+shift+s',
            'stop_speaking_hotkey': 'ctrl+shift+x',
            'auto_start': 'false'
        }
        
        self.config['OpenAI'] = {
            'api_key': '',
            'model': 'gpt-4o',
            'max_tokens': '1000',
            'temperature': '0.1'  # Low temperature for consistent coordinate responses
        }
        
        self.config['Audio'] = {
            'language': 'en-US',
            'transcription_service': 'google',
            'enable_recording': 'true'
        }
        
        self.config['TTS'] = {
            'rate': '200',
            'volume': '0.8',
            'engine': 'auto'
        }
        
        self.config['Response'] = {
            'structured_format': 'true'
        }
        
        self.config['CircleOverlay'] = {
            'enabled': 'true',
            'color': '#00FF00',
            'alpha': '0.7',
            'duration': '4.0',
            'animation': 'pulse',
            'debug_coords': 'false'
        }
        
        self.config['Prompts'] = {
            'system_prompt': 'You are a helpful AI assistant that analyzes screenshots and provides clear, concise answers.',
            'prepend_prompt': '',
            'append_prompt': 'Please be specific and helpful in your response.'
        }
        
        self.save_config()
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            self.config.write(f)
    
    def get(self, section, key, fallback=None):
        """Get configuration value"""
        return self.config.get(section, key, fallback=fallback)
    
    def set(self, section, key, value):
        """Set configuration value"""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = str(value)
        self.save_config()
    
    def get_openai_key(self):
        """Get OpenAI API key"""
        return self.get('OpenAI', 'api_key')
    
    def set_openai_key(self, key):
        """Set OpenAI API key"""
        self.set('OpenAI', 'api_key', key)
    
    def get_hotkey(self):
        """Get global hotkey combination"""
        return self.get('General', 'hotkey', 'ctrl+shift+s')
    
    def set_hotkey(self, hotkey):
        """Set global hotkey combination"""
        self.set('General', 'hotkey', hotkey)
    
    def get_stop_speaking_hotkey(self):
        """Get stop speaking hotkey combination"""
        return self.get('General', 'stop_speaking_hotkey', 'ctrl+shift+x')
    
    def set_stop_speaking_hotkey(self, hotkey):
        """Set stop speaking hotkey combination"""
        self.set('General', 'stop_speaking_hotkey', hotkey)
    
    def get_audio_recording_enabled(self):
        """Get whether audio recording is enabled"""
        return self.get('Audio', 'enable_recording', 'true').lower() == 'true'
    
    def set_audio_recording_enabled(self, enabled):
        """Set whether audio recording is enabled"""
        self.set('Audio', 'enable_recording', 'true' if enabled else 'false')
    
    def get_tts_engine(self):
        """Get TTS engine preference"""
        return self.get('TTS', 'engine', 'auto')
    
    def set_tts_engine(self, engine):
        """Set TTS engine preference"""
        self.set('TTS', 'engine', engine)
    
    def get_structured_format_enabled(self):
        """Get structured format setting"""
        return self.get('Response', 'structured_format', 'false').lower() == 'true'
    
    def set_structured_format_enabled(self, enabled):
        """Set structured format setting"""
        self.set('Response', 'structured_format', str(enabled).lower())
    
    def get_circle_overlay_enabled(self):
        """Get circle overlay enabled setting"""
        return self.get('CircleOverlay', 'enabled', 'true').lower() == 'true'
    
    def set_circle_overlay_enabled(self, enabled):
        """Set circle overlay enabled setting"""
        self.set('CircleOverlay', 'enabled', str(enabled).lower())
    
    def get_circle_overlay_color(self):
        """Get circle overlay color"""
        return self.get('CircleOverlay', 'color', '#00FF00')
    
    def set_circle_overlay_color(self, color):
        """Set circle overlay color"""
        self.set('CircleOverlay', 'color', color)
    
    def get_circle_overlay_alpha(self):
        """Get circle overlay alpha (transparency)"""
        return float(self.get('CircleOverlay', 'alpha', '0.5'))
    
    def set_circle_overlay_alpha(self, alpha):
        """Set circle overlay alpha (transparency)"""
        self.set('CircleOverlay', 'alpha', str(alpha))
    
    def get_circle_overlay_duration(self):
        """Get circle overlay duration"""
        return float(self.get('CircleOverlay', 'duration', '3.0'))
    
    def set_circle_overlay_duration(self, duration):
        """Set circle overlay duration"""
        self.set('CircleOverlay', 'duration', str(duration))
    
    def get_circle_overlay_animation(self):
        """Get circle overlay animation type"""
        return self.get('CircleOverlay', 'animation', 'pulse')
    
    def set_circle_overlay_animation(self, animation):
        """Set circle overlay animation type"""
        self.set('CircleOverlay', 'animation', animation)
    
    def get_circle_overlay_debug_coords(self):
        """Get circle overlay debug coordinates setting"""
        return self.get('CircleOverlay', 'debug_coords', 'false').lower() == 'true'
    
    def set_circle_overlay_debug_coords(self, enabled):
        """Set circle overlay debug coordinates setting"""
        self.set('CircleOverlay', 'debug_coords', str(enabled).lower()) 