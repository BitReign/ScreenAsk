import tkinter as tk
import threading
import time
import math
from typing import Tuple, Optional

class CircleOverlay:
    """Display semi-transparent circle overlay at POI coordinates"""
    
    def __init__(self, config):
        self.config = config
        self.overlay_window = None
        self.canvas = None
        self.circle_id = None
        self.animation_thread = None
        self.is_showing = False
        self.stop_animation = False
        
    def show_circle(self, x: int, y: int, radius: int, duration: Optional[float] = None):
        """Show circle overlay at specified coordinates"""
        if self.is_showing:
            self.hide_circle()
        
        # Get settings
        if duration is None:
            duration = float(self.config.get('CircleOverlay', 'duration', '3.0'))
        
        # Start animation in separate thread
        self.animation_thread = threading.Thread(
            target=self._animate_circle,
            args=(x, y, radius, duration),
            daemon=True
        )
        self.animation_thread.start()
    
    def _animate_circle(self, x: int, y: int, radius: int, duration: float):
        """Animate circle overlay"""
        try:
            self.is_showing = True
            self.stop_animation = False
            
            # Create overlay window
            self._create_overlay_window()
            
            # Get circle settings
            color = self.config.get('CircleOverlay', 'color', '#00FF00')  # Default green
            alpha = float(self.config.get('CircleOverlay', 'alpha', '0.5'))
            animation_type = self.config.get('CircleOverlay', 'animation', 'pulse')
            
            # Convert alpha to tkinter format (0-255)
            alpha_int = int(alpha * 255)
            
            # Animation parameters
            start_time = time.time()
            frames_per_second = 30
            frame_duration = 1.0 / frames_per_second
            
            while time.time() - start_time < duration and not self.stop_animation:
                elapsed = time.time() - start_time
                progress = elapsed / duration
                
                # Calculate current radius based on animation type
                if animation_type == 'pulse':
                    # Pulsing animation
                    pulse_factor = 0.8 + 0.4 * math.sin(elapsed * 4)  # Pulse between 0.8 and 1.2
                    current_radius = int(radius * pulse_factor)
                elif animation_type == 'fade':
                    # Fading animation
                    fade_alpha = alpha * (1 - progress)
                    alpha_int = int(fade_alpha * 255)
                    current_radius = radius
                elif animation_type == 'grow':
                    # Growing animation
                    current_radius = int(radius * (0.5 + 0.5 * progress))
                else:  # static
                    current_radius = radius
                
                # Update circle
                self._update_circle(x, y, current_radius, color, alpha_int)
                
                # Wait for next frame
                time.sleep(frame_duration)
            
            # Hide overlay
            self._hide_overlay_window()
            
        except Exception as e:
            print(f"Error in circle animation: {e}")
        finally:
            self.is_showing = False
            self.stop_animation = False
    
    def _create_overlay_window(self):
        """Create transparent overlay window"""
        try:
            # Create overlay window on main thread
            def create_window():
                try:
                    self.overlay_window = tk.Toplevel()
                    self.overlay_window.title("Circle Overlay")
                    
                    # Make window transparent and always on top
                    self.overlay_window.attributes('-topmost', True)
                    self.overlay_window.attributes('-alpha', 0.7)
                    self.overlay_window.overrideredirect(True)  # Remove window decorations
                    
                    # Make window fullscreen
                    screen_width = self.overlay_window.winfo_screenwidth()
                    screen_height = self.overlay_window.winfo_screenheight()
                    self.overlay_window.geometry(f"{screen_width}x{screen_height}+0+0")
                    
                    # Create canvas
                    self.canvas = tk.Canvas(
                        self.overlay_window,
                        width=screen_width,
                        height=screen_height,
                        highlightthickness=0,
                        bg='black'
                    )
                    self.canvas.pack()
                    
                    # Make canvas transparent
                    self.overlay_window.configure(bg='black')
                    self.overlay_window.attributes('-transparentcolor', 'black')
                    
                    # Bind cleanup on window close
                    self.overlay_window.protocol("WM_DELETE_WINDOW", self._on_window_close)
                    
                except Exception as e:
                    print(f"Error in create_window: {e}")
                    self.overlay_window = None
                    self.canvas = None
            
            # Execute on main thread
            if threading.current_thread() != threading.main_thread():
                # Schedule on main thread
                root = tk._default_root
                if root:
                    root.after(0, create_window)
                    # Wait for window creation with timeout
                    timeout = 2.0  # 2 second timeout
                    start_time = time.time()
                    while self.overlay_window is None and not self.stop_animation:
                        if time.time() - start_time > timeout:
                            print("Timeout waiting for overlay window creation")
                            break
                        time.sleep(0.01)
            else:
                create_window()
                
        except Exception as e:
            print(f"Error creating overlay window: {e}")
            self.overlay_window = None
            self.canvas = None
    
    def _on_window_close(self):
        """Handle window close event"""
        self.stop_animation = True
    
    def _update_circle(self, x: int, y: int, radius: int, color: str, alpha: int):
        """Update circle on canvas"""
        try:
            if self.canvas and self.overlay_window:
                def update():
                    if self.canvas and not self.stop_animation:
                        # Clear previous circle
                        if self.circle_id:
                            self.canvas.delete(self.circle_id)
                        
                        # Draw new circle
                        x1, y1 = x - radius, y - radius
                        x2, y2 = x + radius, y + radius
                        
                        # Create color with alpha
                        fill_color = color
                        outline_color = color
                        
                        self.circle_id = self.canvas.create_oval(
                            x1, y1, x2, y2,
                            fill=fill_color,
                            outline=outline_color,
                            width=2
                        )
                        
                        # Add coordinate text for debugging (if debug mode enabled)
                        debug_mode = self.config.get('CircleOverlay', 'debug_coords', 'false').lower() == 'true'
                        if debug_mode:
                            coord_text = f"({x}, {y})"
                            text_x = x
                            text_y = y - radius - 20  # Position above the circle
                            
                            self.canvas.create_text(
                                text_x, text_y,
                                text=coord_text,
                                fill="white",
                                font=("Arial", 12, "bold"),
                                anchor="center"
                            )
                
                # Execute on main thread
                if threading.current_thread() != threading.main_thread():
                    root = tk._default_root
                    if root:
                        root.after(0, update)
                else:
                    update()
                    
        except Exception as e:
            print(f"Error updating circle: {e}")
    
    def _hide_overlay_window(self):
        """Hide overlay window"""
        try:
            def hide():
                try:
                    if self.overlay_window:
                        # Clear any pending after() calls
                        self.overlay_window.after_cancel("all")
                        self.overlay_window.destroy()
                        self.overlay_window = None
                        self.canvas = None
                        self.circle_id = None
                except Exception as e:
                    print(f"Error destroying overlay window: {e}")
                    # Force cleanup even if destroy fails
                    self.overlay_window = None
                    self.canvas = None
                    self.circle_id = None
            
            # Execute on main thread
            if threading.current_thread() != threading.main_thread():
                root = tk._default_root
                if root:
                    try:
                        root.after(0, hide)
                    except Exception as e:
                        print(f"Error scheduling hide: {e}")
            else:
                hide()
                
        except Exception as e:
            print(f"Error hiding overlay: {e}")
            # Force cleanup
            self.overlay_window = None
            self.canvas = None
            self.circle_id = None
    
    def hide_circle(self):
        """Hide circle overlay immediately"""
        self.stop_animation = True
        
        # Clean up immediately
        if hasattr(self, 'overlay_window') and self.overlay_window:
            try:
                self.overlay_window.after_cancel("all")
            except:
                pass
        
        if self.animation_thread and self.animation_thread.is_alive():
            self.animation_thread.join(timeout=1.0)
        
        self._hide_overlay_window()
        self.is_showing = False
    
    def is_circle_showing(self) -> bool:
        """Check if circle is currently showing"""
        return self.is_showing 