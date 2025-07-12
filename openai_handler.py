import openai
import base64
from config import Config

class OpenAIHandler:
    def __init__(self):
        self.config = Config()
        self.client = None
        self.setup_client()
    
    def setup_client(self):
        """Setup OpenAI client"""
        # Reload config to get latest settings
        self.config.load_config()
        api_key = self.config.get_openai_key()
        
        if api_key and api_key.strip():
            try:
                self.client = openai.OpenAI(api_key=api_key.strip())
                print("✓ OpenAI client configured successfully")
            except Exception as e:
                print(f"Error setting up OpenAI client: {e}")
                self.client = None
        else:
            print("OpenAI API key not found. Please set it in settings.")
            self.client = None
    
    def set_api_key(self, api_key):
        """Set OpenAI API key"""
        self.config.set_openai_key(api_key)
        self.setup_client()
    
    def analyze_screenshot_with_text(self, screenshot_base64, user_text=None):
        """Analyze screenshot with optional user text using GPT-4 Vision"""
        if not self.client:
            return "Error: OpenAI API key not configured"
        
        try:
            # Prepare the message content
            content = [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{screenshot_base64}"
                    }
                }
            ]
            
            # Add user text if provided
            if user_text:
                content.insert(0, {
                    "type": "text",
                    "text": f"User question: {user_text}\n\nPlease analyze this screenshot and answer the user's question. If no specific question is asked, provide a helpful description of what you see in the image."
                })
            else:
                content.insert(0, {
                    "type": "text",
                    "text": "Please analyze this screenshot and provide a helpful description of what you see."
                })
            
            response = self.client.chat.completions.create(
                model=self.config.get('OpenAI', 'model', 'gpt-4-vision-preview'),
                messages=[
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                max_tokens=int(self.config.get('OpenAI', 'max_tokens', '1000'))
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error analyzing screenshot: {str(e)}"
    
    def chat_completion(self, prompt):
        """Simple chat completion without image"""
        if not self.client:
            return "Error: OpenAI API key not configured"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=int(self.config.get('OpenAI', 'max_tokens', '1000'))
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error getting chat completion: {str(e)}"
    
    def is_configured(self):
        """Check if OpenAI API is properly configured"""
        return self.client is not None and self.config.get_openai_key() != ""
    
    def test_connection(self):
        """Test OpenAI API connection"""
        if not self.client:
            return False, "API key not configured"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=10
            )
            return True, "Connection successful"
        except Exception as e:
            return False, f"Connection failed: {str(e)}" 