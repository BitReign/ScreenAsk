import pystray
from PIL import Image, ImageDraw
import threading
import tkinter as tk
from tkinter import messagebox
import os

class TrayHandler:
    def __init__(self, main_app):
        self.main_app = main_app
        self.icon = None
        self.menu_items = []
        self.create_icon()
        self.create_menu()
        
    def create_icon(self):
        """Create system tray icon"""
        # Try to load the icon file, fallback to programmatic creation
        try:
            if os.path.exists('tray_icon.png'):
                image = Image.open('tray_icon.png')
            elif os.path.exists('screenask_icon.png'):
                image = Image.open('screenask_icon.png')
                image = image.resize((64, 64), Image.Resampling.LANCZOS)
            else:
                # Fallback: create a simple icon programmatically
                width = 64
                height = 64
                image = Image.new('RGB', (width, height), color='white')
                draw = ImageDraw.Draw(image)
                
                # Draw a simple camera icon
                draw.rectangle([10, 20, 54, 44], fill='black', outline='black')
                draw.ellipse([20, 25, 44, 39], fill='white', outline='white')
                draw.ellipse([28, 29, 36, 35], fill='black', outline='black')
                draw.rectangle([45, 22, 52, 28], fill='black', outline='black')
                
        except Exception as e:
            print(f"Error loading icon: {e}")
            # Fallback to simple programmatic icon
            width = 64
            height = 64
            image = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(image)
            draw.rectangle([10, 20, 54, 44], fill='black', outline='black')
            draw.ellipse([20, 25, 44, 39], fill='white', outline='white')
            draw.ellipse([28, 29, 36, 35], fill='black', outline='black')
            draw.rectangle([45, 22, 52, 28], fill='black', outline='black')
        
        self.icon = pystray.Icon("ScreenAsk", image)
        
    def create_menu(self):
        """Create context menu for tray icon"""
        self.menu_items = [
            pystray.MenuItem("Open", self.show_main_window),
            pystray.MenuItem("Settings", self.show_settings),
            pystray.MenuItem("About", self.show_about),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", self.quit_app)
        ]
        
        self.icon.menu = pystray.Menu(*self.menu_items)
        
    def show_main_window(self, icon=None, item=None):
        """Show main application window"""
        if self.main_app:
            self.main_app.show_main_window()
    
    def show_settings(self, icon=None, item=None):
        """Show settings window"""
        if self.main_app:
            self.main_app.show_settings()
    
    def show_about(self, icon=None, item=None):
        """Show about dialog"""
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showinfo("About ScreenAsk", 
                              "ScreenAsk v1.0\n\n"
                              "AI-powered screen capture and analysis tool.\n\n"
                              "Features:\n"
                              "- Screenshot capture with hotkey\n"
                              "- Voice input transcription\n"
                              "- AI analysis with OpenAI GPT-4 Vision\n"
                              "- Text-to-speech responses\n\n"
                              "Press your configured hotkey to capture and analyze!")
            root.destroy()
        except Exception as e:
            print(f"Error showing about dialog: {e}")
    
    def quit_app(self, icon=None, item=None):
        """Quit the application"""
        if self.main_app:
            self.main_app.quit()
    
    def on_double_click(self, icon, item):
        """Handle double click on tray icon - toggle main window visibility"""
        if self.main_app and self.main_app.main_gui and self.main_app.main_gui.root:
            try:
                # Check if window is currently visible
                if self.main_app.main_gui.root.state() == 'normal':
                    # Window is visible, hide it
                    self.main_app.main_gui.hide_to_tray()
                else:
                    # Window is hidden, show it
                    self.main_app.main_gui.show_window()
            except Exception as e:
                print(f"Error toggling window visibility: {e}")
                # Fallback to showing the window
                self.show_main_window()
        else:
            # Fallback to showing the window
            self.show_main_window()
    
    def start_tray(self):
        """Start the system tray in a separate thread"""
        def run_tray():
            try:
                self.icon.run(setup=self.setup_tray)
            except Exception as e:
                print(f"Error running tray: {e}")
        
        tray_thread = threading.Thread(target=run_tray, daemon=True)
        tray_thread.start()
    
    def setup_tray(self, icon):
        """Setup tray icon properties"""
        icon.visible = True
        # Set double-click action
        icon.default_action = self.on_double_click
    
    def stop_tray(self):
        """Stop the system tray"""
        if self.icon:
            self.icon.stop()
    
    def update_icon(self, image=None):
        """Update tray icon image"""
        if image and self.icon:
            self.icon.icon = image
    
    def notify(self, title, message):
        """Show system notification"""
        if self.icon:
            try:
                self.icon.notify(message, title)
            except Exception as e:
                print(f"Error showing notification: {e}")
    
    def set_tooltip(self, tooltip):
        """Set tray icon tooltip"""
        if self.icon:
            self.icon.title = tooltip 