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
            'auto_start': 'false'
        }
        
        self.config['OpenAI'] = {
            'api_key': '',
            'model': 'gpt-4o',
            'max_tokens': '1000'
        }
        
        self.config['Audio'] = {
            'record_duration': '5',
            'language': 'en-US'
        }
        
        self.config['TTS'] = {
            'rate': '200',
            'volume': '0.8'
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