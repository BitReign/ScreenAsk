import pyautogui
import io
import base64
from PIL import Image
import time

class ScreenshotHandler:
    def __init__(self):
        # Disable pyautogui's fail-safe feature
        pyautogui.FAILSAFE = False
    
    def capture_screenshot(self):
        """Capture screenshot and return as base64 encoded string"""
        try:
            # Take screenshot
            screenshot = pyautogui.screenshot()
            
            # Convert PIL Image to bytes
            img_buffer = io.BytesIO()
            screenshot.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            # Convert to base64
            img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
            
            return img_base64
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            return None
    
    def capture_screenshot_file(self, filename=None):
        """Capture screenshot and save to file"""
        try:
            if filename is None:
                timestamp = str(int(time.time()))
                filename = f"screenshot_{timestamp}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            return filename
        except Exception as e:
            print(f"Error saving screenshot: {e}")
            return None
    
    def get_screen_resolution(self):
        """Get current screen resolution"""
        try:
            size = pyautogui.size()
            return size.width, size.height
        except Exception as e:
            print(f"Error getting screen resolution: {e}")
            return None, None 