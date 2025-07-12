import openai
import base64
import json
import hashlib
import time
from src.core.config import Config

class OpenAIHandler:
    def __init__(self):
        self.config = Config()
        self.client = None
        self.coordinate_cache = {}  # Cache for coordinate consistency
        self.cache_timeout = 300  # 5 minutes cache timeout
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
        """Analyze screenshot with optional user text using GPT-4 Vision - Always returns structured response"""
        if not self.client:
            return "Error: OpenAI API key not configured"
        
        try:
            # Reload config to get latest settings
            self.config.load_config()
            
            # Always use structured response format
            return self._analyze_with_structured_response(screenshot_base64, user_text)
                
        except Exception as e:
            return f"Error analyzing screenshot: {str(e)}"
    
    def _analyze_with_structured_response(self, screenshot_base64, user_text=None):
        """Analyze screenshot and return structured JSON response"""
        # Check for cached coordinates if user_text is provided
        cached_coordinates = None
        query_hash = None
        if user_text:
            query_hash = self._generate_query_hash(user_text)
            cached_coordinates = self._get_cached_coordinates(query_hash)
            
        # Get prompt settings
        system_prompt = self.config.get('Prompts', 'system_prompt', 
                                      'You are a helpful AI assistant that analyzes screenshots and provides clear, concise answers.')
        prepend_prompt = self.config.get('Prompts', 'prepend_prompt', '')
        append_prompt = self.config.get('Prompts', 'append_prompt', 
                                      'Please be specific and helpful in your response.')
        
        # Try to get screen resolution for context
        screen_context = ""
        screen_width = screen_height = None
        try:
            import tkinter as tk
            root = tk._default_root
            if root:
                screen_width = root.winfo_screenwidth()
                screen_height = root.winfo_screenheight()
                screen_context = f"\n\nSCREEN CONTEXT: This screenshot is from a {screen_width}x{screen_height} display."
        except:
            pass
        
        # Prepare the message content
        content = [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{screenshot_base64}"
                }
            }
        ]
        
        # Build the structured prompt
        prompt_parts = []
        
        # Add prepend prompt if provided
        if prepend_prompt.strip():
            prompt_parts.append(prepend_prompt.strip())
        
        # Add structured response instructions
        structured_instructions = f"""
You must respond with a JSON object containing:
- x: X coordinate of the main point of interest (integer)
- y: Y coordinate of the main point of interest (integer)  
- r: Radius around the point of interest for highlighting (integer, typically 25-100 for icons, 50-300 for larger elements)
- tx: The actual text response to be spoken (string)

CRITICAL VISUAL ANALYSIS INSTRUCTIONS:
- Use screen coordinates where (0,0) is at the TOP-LEFT corner
- X increases going RIGHT across the screen
- Y increases going DOWN the screen
- Perform ACTUAL PIXEL-LEVEL VISUAL ANALYSIS of the screenshot
- Identify the exact visual location of the requested element by examining its pixels
- Do NOT make assumptions about typical layouts or standard positions{screen_context}

VISUAL IDENTIFICATION METHODOLOGY:
1. SCAN the entire image systematically for the requested element
2. LOCATE the element by its visual characteristics (colors, shapes, text, icons)
3. MEASURE the pixel coordinates of the element's visual center
4. VERIFY the coordinates by cross-referencing with surrounding visual elements
5. CALCULATE the exact center point of the identified element

ELEMENT ANALYSIS GUIDELINES:
- For icons: Find the exact center of the icon graphic by analyzing its visual boundaries, edges, and shape
- For taskbar icons: Look for small square/rectangular icon shapes in the taskbar area, identify the specific icon requested
- For application icons: Identify the icon by its distinctive visual features (colors, logos, shapes, text)
- For text: Locate the center of the text bounding box by measuring character positions
- For buttons: Identify button borders and calculate the geometric center
- For windows: Find the center of the window content area or title bar
- For UI elements: Analyze the visual structure to determine precise center coordinates

ICON DETECTION SPECIFICS:
- When looking for specific application icons (like Spotify, Chrome, etc.), look for their distinctive visual features
- Taskbar icons are typically small (16x16 to 32x32 pixels) and arranged horizontally
- System tray icons are usually in the bottom-right corner of the screen
- Application icons may have distinctive colors, logos, or shapes that identify them
- If multiple similar icons exist, choose the one that best matches the requested application

ACCURACY REQUIREMENTS:
- Base coordinates ONLY on actual visual analysis of the screenshot
- Ignore any assumptions about "typical" positions or standard layouts
- Use the actual pixel data to determine exact element locations
- Cross-validate coordinates by examining neighboring visual elements
- Ensure coordinates point to the visual center of the identified element

COORDINATE PRECISION:
- Measure coordinates with pixel-level accuracy
- Account for element size when determining center point
- For small icons (16x16 to 32x32 pixels), ensure coordinates point to the center of the icon, not the general area
- Verify coordinates make sense within the visual context
- Double-check measurements against the actual image boundaries
- If an icon is part of a group (like taskbar icons), identify the specific icon requested rather than the general area

Example format:
{{"x": 150, "y": 200, "r": 100, "tx": "I can see a login form with username and password fields"}}

ICON IDENTIFICATION EXAMPLES:
- For "Where is Spotify icon": Look for green circular icon with sound waves, provide exact center coordinates
- For "Find Chrome icon": Look for colorful circular icon with red, yellow, green, blue colors  
- For "Locate file manager": Look for folder icon, typically yellow/blue colored
- Always identify the SPECIFIC icon requested, not the general area where it might be

Instructions:
- Analyze the screenshot using computer vision principles
- Identify the requested element through visual pattern recognition
- Calculate precise coordinates based on actual pixel measurements
- Set radius proportional to the identified element's visual size
- Provide clear, accurate text response
- Respond ONLY with valid JSON, no additional text
"""
        
        prompt_parts.append(structured_instructions)
        
        # Add user text if provided
        if user_text:
            prompt_parts.append(f"User question: {user_text}")
            prompt_parts.append("Please analyze this screenshot and answer the user's question in the structured JSON format above.")
        else:
            prompt_parts.append("Please analyze this screenshot and provide a helpful description in the structured JSON format above.")
        
        # Add append prompt if provided
        if append_prompt.strip():
            prompt_parts.append(append_prompt.strip())
        
        # Combine all parts
        full_prompt = "\n\n".join(prompt_parts)
        
        content.insert(0, {
            "type": "text",
            "text": full_prompt
        })
        
        # Prepare messages with system prompt
        messages = []
        if system_prompt.strip():
            messages.append({
                "role": "system",
                "content": system_prompt.strip()
            })
        
        messages.append({
            "role": "user",
            "content": content
        })
        
        response = self.client.chat.completions.create(
            model=self.config.get('OpenAI', 'model', 'gpt-4o'),
            messages=messages,
            max_tokens=int(self.config.get('OpenAI', 'max_tokens', '1000')),
            temperature=float(self.config.get('OpenAI', 'temperature', '0.1'))  # Low temperature for consistency
        )
        
        response_content = response.choices[0].message.content
        
        # If we have user text, try to apply coordinate smoothing
        if user_text and query_hash:
            try:
                # Parse the response to get coordinates
                parsed_data, error = self.parse_structured_response(response_content)
                if parsed_data and not error:
                    # Apply coordinate smoothing if we have cached coordinates
                    smoothed_data = self._smooth_coordinates(parsed_data, cached_coordinates)
                    
                    # Cache the coordinates for future use
                    self._cache_coordinates(query_hash, smoothed_data)
                    
                    # Return the smoothed response as JSON
                    return json.dumps(smoothed_data)
            except Exception as e:
                print(f"Warning: Coordinate smoothing failed: {e}")
        
        return response_content
    

    
    def parse_structured_response(self, response_text):
        """Parse structured JSON response and return data"""
        try:
            # Clean up the response text
            cleaned_text = response_text.strip()
            
            # Handle markdown code blocks
            if cleaned_text.startswith('```json') and cleaned_text.endswith('```'):
                # Remove markdown code block formatting
                cleaned_text = cleaned_text[7:-3].strip()  # Remove ```json and ```
            elif cleaned_text.startswith('```') and cleaned_text.endswith('```'):
                # Remove generic code block formatting
                cleaned_text = cleaned_text[3:-3].strip()  # Remove ``` and ```
            
            # Try to parse JSON
            data = json.loads(cleaned_text)
            
            # Validate required fields
            if not all(key in data for key in ['x', 'y', 'r', 'tx']):
                return None, "Invalid JSON structure: missing required fields (x, y, r, tx)"
            
            # Validate data types
            if not isinstance(data['x'], int) or not isinstance(data['y'], int):
                return None, "Invalid data types: x and y must be integers"
            
            if not isinstance(data['r'], int) or data['r'] <= 0:
                return None, "Invalid radius: r must be a positive integer"
            
            if not isinstance(data['tx'], str) or not data['tx'].strip():
                return None, "Invalid text: tx must be a non-empty string"
            
            return data, None
            
        except json.JSONDecodeError as e:
            return None, f"JSON parsing error: {str(e)}"
        except Exception as e:
            return None, f"Error parsing response: {str(e)}"
    
    def _generate_query_hash(self, user_text, screenshot_size=None):
        """Generate a hash for the query to use as cache key"""
        if screenshot_size:
            query_string = f"{user_text.lower().strip()}_{screenshot_size}"
        else:
            query_string = user_text.lower().strip()
        return hashlib.md5(query_string.encode()).hexdigest()
    
    def _get_cached_coordinates(self, query_hash):
        """Get cached coordinates for a query"""
        if query_hash in self.coordinate_cache:
            cache_entry = self.coordinate_cache[query_hash]
            # Check if cache is still valid (within timeout)
            if time.time() - cache_entry['timestamp'] < self.cache_timeout:
                return cache_entry['coordinates']
        return None
    
    def _cache_coordinates(self, query_hash, coordinates):
        """Cache coordinates for a query"""
        self.coordinate_cache[query_hash] = {
            'coordinates': coordinates,
            'timestamp': time.time()
        }
    
    def _smooth_coordinates(self, new_coords, cached_coords, similarity_threshold=50):
        """Apply coordinate smoothing if the new coordinates are close to cached ones"""
        if not cached_coords:
            return new_coords
        
        # Calculate distance between new and cached coordinates
        dx = abs(new_coords['x'] - cached_coords['x'])
        dy = abs(new_coords['y'] - cached_coords['y'])
        distance = (dx**2 + dy**2)**0.5
        
        # If coordinates are very close, use cached coordinates for consistency
        if distance < similarity_threshold:
            print(f"🎯 Using cached coordinates for consistency (distance: {distance:.1f}px)")
            return {
                'x': cached_coords['x'],
                'y': cached_coords['y'],
                'r': new_coords['r'],  # Use new radius
                'tx': new_coords['tx']  # Use new text
            }
        
        return new_coords
    
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
                max_tokens=int(self.config.get('OpenAI', 'max_tokens', '1000')),
                temperature=float(self.config.get('OpenAI', 'temperature', '0.1'))
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
                max_tokens=10,
                temperature=float(self.config.get('OpenAI', 'temperature', '0.1'))
            )
            return True, "Connection successful"
        except Exception as e:
            return False, f"Connection failed: {str(e)}" 