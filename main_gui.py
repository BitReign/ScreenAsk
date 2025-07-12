import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from config import Config
from openai_handler import OpenAIHandler
from tts_handler import TTSHandler

class MainGUI:
    def __init__(self, main_app):
        self.main_app = main_app
        self.config = Config()
        self.openai_handler = OpenAIHandler()
        self.tts_handler = TTSHandler()
        self.root = None
        self.settings_window = None
        
    def create_main_window(self):
        """Create the main application window"""
        self.root = tk.Tk()
        self.root.title("ScreenAsk - AI Screen Analyzer")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="ScreenAsk", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status section
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(1, weight=1)
        
        # OpenAI API Status
        ttk.Label(status_frame, text="OpenAI API:").grid(row=0, column=0, sticky=tk.W)
        self.openai_status = ttk.Label(status_frame, text="Not configured", foreground="red")
        self.openai_status.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Current hotkey
        ttk.Label(status_frame, text="Hotkey:").grid(row=1, column=0, sticky=tk.W)
        self.hotkey_label = ttk.Label(status_frame, text=self.config.get_hotkey())
        self.hotkey_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        # Buttons section
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0))
        
        # Settings button
        settings_btn = ttk.Button(button_frame, text="Settings", command=self.show_settings)
        settings_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Test API button
        test_btn = ttk.Button(button_frame, text="Test API", command=self.test_api)
        test_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Test capture button
        capture_btn = ttk.Button(button_frame, text="Test Capture", command=self.test_capture)
        capture_btn.grid(row=0, column=2, padx=(0, 10))
        
        # Hide to tray button
        hide_btn = ttk.Button(button_frame, text="Hide to Tray", command=self.hide_to_tray)
        hide_btn.grid(row=0, column=3)
        
        # Instructions
        instructions_frame = ttk.LabelFrame(main_frame, text="Instructions", padding="10")
        instructions_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(20, 0))
        instructions_frame.columnconfigure(0, weight=1)
        instructions_frame.rowconfigure(0, weight=1)
        
        instructions_text = tk.Text(instructions_frame, height=10, wrap=tk.WORD)
        instructions_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(instructions_frame, orient=tk.VERTICAL, command=instructions_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        instructions_text.configure(yscrollcommand=scrollbar.set)
        
        instructions_text.insert(tk.END, 
            "Welcome to ScreenAsk!\n\n"
            "1. Configure your OpenAI API key in Settings\n"
            "2. Set your preferred hotkey combination\n"
            "3. Press the hotkey to capture screen and analyze\n"
            "4. Speak your question when prompted\n"
            "5. Listen to the AI response\n\n"
            "Features:\n"
            "• Screenshot capture with AI analysis\n"
            "• Voice input transcription\n"
            "• Text-to-speech responses\n"
            "• Background operation with tray icon\n\n"
            "The app runs in the background. Right-click the tray icon for options.")
        
        instructions_text.configure(state=tk.DISABLED)
        
        # Update status
        self.update_status()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def show_settings(self):
        """Show settings window"""
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.lift()
            return
            
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Settings")
        self.settings_window.geometry("400x500")
        self.settings_window.resizable(False, False)
        
        # Make it modal
        self.settings_window.transient(self.root)
        self.settings_window.grab_set()
        
        # Settings frame
        settings_frame = ttk.Frame(self.settings_window, padding="10")
        settings_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.settings_window.columnconfigure(0, weight=1)
        self.settings_window.rowconfigure(0, weight=1)
        settings_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # OpenAI Settings
        openai_frame = ttk.LabelFrame(settings_frame, text="OpenAI Configuration", padding="10")
        openai_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        openai_frame.columnconfigure(1, weight=1)
        
        ttk.Label(openai_frame, text="API Key:").grid(row=0, column=0, sticky=tk.W)
        self.api_key_entry = ttk.Entry(openai_frame, show="*", width=40)
        self.api_key_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        self.api_key_entry.insert(0, self.config.get_openai_key())
        
        ttk.Label(openai_frame, text="Model:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.model_var = tk.StringVar(value=self.config.get('OpenAI', 'model', 'gpt-4o'))
        model_combo = ttk.Combobox(openai_frame, textvariable=self.model_var, 
                                  values=["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"])
        model_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(5, 0))
        
        row += 1
        
        # Hotkey Settings
        hotkey_frame = ttk.LabelFrame(settings_frame, text="Hotkey Configuration", padding="10")
        hotkey_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        hotkey_frame.columnconfigure(1, weight=1)
        
        ttk.Label(hotkey_frame, text="Hotkey:").grid(row=0, column=0, sticky=tk.W)
        self.hotkey_var = tk.StringVar(value=self.config.get_hotkey())
        hotkey_combo = ttk.Combobox(hotkey_frame, textvariable=self.hotkey_var,
                                   values=["ctrl+shift+s", "ctrl+alt+s", "ctrl+shift+a", "alt+shift+s"])
        hotkey_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        row += 1
        
        # Audio Settings
        audio_frame = ttk.LabelFrame(settings_frame, text="Audio Configuration", padding="10")
        audio_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        audio_frame.columnconfigure(1, weight=1)
        
        ttk.Label(audio_frame, text="Record Duration (s):").grid(row=0, column=0, sticky=tk.W)
        self.duration_var = tk.StringVar(value=self.config.get('Audio', 'record_duration', '5'))
        duration_spin = ttk.Spinbox(audio_frame, from_=1, to=30, textvariable=self.duration_var, width=10)
        duration_spin.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(audio_frame, text="Language:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.language_var = tk.StringVar(value=self.config.get('Audio', 'language', 'en-US'))
        language_combo = ttk.Combobox(audio_frame, textvariable=self.language_var,
                                     values=["en-US", "en-GB", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-PT", "ru-RU"])
        language_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(5, 0))
        
        row += 1
        
        # TTS Settings
        tts_frame = ttk.LabelFrame(settings_frame, text="Text-to-Speech", padding="10")
        tts_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        tts_frame.columnconfigure(1, weight=1)
        
        ttk.Label(tts_frame, text="Speech Rate:").grid(row=0, column=0, sticky=tk.W)
        self.rate_var = tk.StringVar(value=self.config.get('TTS', 'rate', '200'))
        rate_scale = ttk.Scale(tts_frame, from_=50, to=400, orient=tk.HORIZONTAL, variable=self.rate_var)
        rate_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        ttk.Label(tts_frame, text="Volume:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.volume_var = tk.StringVar(value=self.config.get('TTS', 'volume', '0.8'))
        volume_scale = ttk.Scale(tts_frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL, variable=self.volume_var)
        volume_scale.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(5, 0))
        
        row += 1
        
        # Buttons
        button_frame = ttk.Frame(settings_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=(20, 0))
        
        save_btn = ttk.Button(button_frame, text="Save", command=self.save_settings)
        save_btn.grid(row=0, column=0, padx=(0, 10))
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.settings_window.destroy)
        cancel_btn.grid(row=0, column=1)
        
    def save_settings(self):
        """Save settings to configuration"""
        # Save OpenAI settings
        self.config.set_openai_key(self.api_key_entry.get())
        self.config.set('OpenAI', 'model', self.model_var.get())
        
        # Save hotkey
        self.config.set_hotkey(self.hotkey_var.get())
        
        # Save audio settings
        self.config.set('Audio', 'record_duration', self.duration_var.get())
        self.config.set('Audio', 'language', self.language_var.get())
        
        # Save TTS settings
        self.config.set('TTS', 'rate', self.rate_var.get())
        self.config.set('TTS', 'volume', self.volume_var.get())
        
        # Update handlers with fresh config
        self.openai_handler.setup_client()
        self.tts_handler.setup_voice()
        
        # Update main app components
        if self.main_app:
            # Reload config for all handlers
            self.main_app.config.load_config()
            self.main_app.openai_handler.setup_client()
            self.main_app.update_hotkey()
        
        # Update status
        self.update_status()
        
        # Close settings window
        self.settings_window.destroy()
        
        messagebox.showinfo("Settings", "Settings saved successfully!")
        
    def test_api(self):
        """Test OpenAI API connection"""
        def test_thread():
            success, message = self.openai_handler.test_connection()
            if success:
                messagebox.showinfo("API Test", "OpenAI API connection successful!")
            else:
                messagebox.showerror("API Test", f"API connection failed:\n{message}")
        
        threading.Thread(target=test_thread, daemon=True).start()
        
    def test_capture(self):
        """Test screenshot capture"""
        if self.main_app:
            threading.Thread(target=self.main_app.handle_hotkey, daemon=True).start()
            
    def hide_to_tray(self):
        """Hide window to system tray"""
        if self.root:
            self.root.withdraw()
            
    def show_window(self):
        """Show the main window"""
        if self.root:
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            
    def update_status(self):
        """Update status indicators"""
        if self.openai_handler.is_configured():
            self.openai_status.config(text="Configured", foreground="green")
        else:
            self.openai_status.config(text="Not configured", foreground="red")
            
        self.hotkey_label.config(text=self.config.get_hotkey())
        
    def on_closing(self):
        """Handle window closing"""
        self.hide_to_tray()
        
    def quit_app(self):
        """Quit the application"""
        if self.root:
            self.root.destroy() 