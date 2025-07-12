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
            'max_tokens': '1000'
        }
        
        self.config['Audio'] = {
            'language': 'en-US',
            'transcription_service': 'google',
            'enable_recording': 'true'
        }
        
        self.config['TTS'] = {
            'rate': '200',
            'volume': '0.8'
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