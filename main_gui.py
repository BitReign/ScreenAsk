import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
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
        self.root.geometry("900x700")
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
        main_frame.columnconfigure(0, weight=2)  # Make chat area wider
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="ScreenAsk", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Create left panel for chat history
        left_frame = ttk.LabelFrame(main_frame, text="Chat History", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)
        
        # Create chat display area
        self.chat_frame = tk.Frame(left_frame, bg='white', relief='sunken', bd=1)
        self.chat_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.chat_frame.columnconfigure(0, weight=1)
        
        # Create scrollable chat area
        self.chat_canvas = tk.Canvas(self.chat_frame, bg='white', highlightthickness=0)
        self.chat_scrollbar = ttk.Scrollbar(self.chat_frame, orient="vertical", command=self.chat_canvas.yview)
        self.chat_scrollable_frame = ttk.Frame(self.chat_canvas)
        
        self.chat_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        )
        
        self.chat_canvas.create_window((0, 0), window=self.chat_scrollable_frame, anchor="nw")
        self.chat_canvas.configure(yscrollcommand=self.chat_scrollbar.set)
        
        self.chat_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.chat_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind mousewheel to chat canvas
        def _on_mousewheel(event):
            self.chat_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.chat_canvas.bind("<MouseWheel>", _on_mousewheel)
        
        # Clear chat button
        clear_chat_btn = ttk.Button(left_frame, text="Clear Chat", command=self.clear_chat_history)
        clear_chat_btn.grid(row=1, column=0, pady=(10, 0), sticky=tk.W)
        
        # Create right panel for status and controls
        right_frame = ttk.Frame(main_frame, padding="10")
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        right_frame.columnconfigure(0, weight=1)
        
        # Status section
        status_frame = ttk.LabelFrame(right_frame, text="Status", padding="10")
        status_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(1, weight=1)
        
        # OpenAI API Status
        ttk.Label(status_frame, text="OpenAI API:").grid(row=0, column=0, sticky=tk.W)
        self.openai_status = ttk.Label(status_frame, text="Not configured", foreground="red")
        self.openai_status.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Current hotkey
        ttk.Label(status_frame, text="Record Hotkey:").grid(row=1, column=0, sticky=tk.W)
        self.hotkey_label = ttk.Label(status_frame, text=self.config.get_hotkey())
        self.hotkey_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        # Stop speaking hotkey
        ttk.Label(status_frame, text="Stop Speaking:").grid(row=2, column=0, sticky=tk.W)
        self.stop_hotkey_label = ttk.Label(status_frame, text=self.config.get_stop_speaking_hotkey())
        self.stop_hotkey_label.grid(row=2, column=1, sticky=tk.W, padx=(10, 0))
        
        # Recording/Processing Status
        ttk.Label(status_frame, text="Status:").grid(row=3, column=0, sticky=tk.W)
        self.recording_status = ttk.Label(status_frame, text="Ready", foreground="green")
        self.recording_status.grid(row=3, column=1, sticky=tk.W, padx=(10, 0))
        
        # Buttons section
        button_frame = ttk.Frame(right_frame)
        button_frame.grid(row=1, column=0, pady=(20, 0))
        
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
        instructions_frame = ttk.LabelFrame(right_frame, text="Instructions", padding="10")
        instructions_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(20, 0))
        instructions_frame.columnconfigure(0, weight=1)
        instructions_frame.rowconfigure(0, weight=1)
        
        instructions_text = tk.Text(instructions_frame, height=10, wrap=tk.WORD)
        instructions_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(instructions_frame, orient=tk.VERTICAL, command=instructions_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        instructions_text.configure(yscrollcommand=scrollbar.set)
        
        audio_enabled = self.config.get_audio_recording_enabled()
        
        if audio_enabled:
            instructions = (
                "Welcome to ScreenAsk!\n\n"
                "1. Configure your OpenAI API key in Settings\n"
                "2. Set your preferred hotkey combination\n"
                "3. Hold the hotkey to capture screen and record audio\n"
                "4. Speak your question while holding the key\n"
                "5. Release the key to stop recording and get AI response\n"
                f"6. Press {self.config.get_stop_speaking_hotkey()} to stop AI speaking\n\n"
                "Features:\n"
                "• Push-to-talk recording (like walkie-talkies)\n"
                "• Stop speaking hotkey to interrupt AI responses\n"
                "• Screenshot capture with AI analysis\n"
                "• Voice input transcription (Google/OpenAI Whisper)\n"
                "• Text-to-speech responses\n"
                "• Background operation with tray icon\n\n"
                "The app runs in the background. Right-click the tray icon for options."
            )
        else:
            instructions = (
                "Welcome to ScreenAsk! (Audio Recording Disabled)\n\n"
                "1. Configure your OpenAI API key in Settings\n"
                "2. Set your preferred hotkey combination\n"
                "3. Press the hotkey to capture and analyze screen\n"
                f"4. Press {self.config.get_stop_speaking_hotkey()} to stop AI speaking\n\n"
                "Features:\n"
                "• Visual-only mode (no audio recording)\n"
                "• Instant screenshot analysis\n"
                "• Stop speaking hotkey to interrupt AI responses\n"
                "• Custom AI prompts for analysis\n"
                "• Text-to-speech responses\n"
                "• Background operation with tray icon\n\n"
                "Note: Audio recording is disabled. Enable it in Settings to use voice input.\n"
                "The app runs in the background. Right-click the tray icon for options."
            )
        
        instructions_text.insert(tk.END, instructions)
        
        instructions_text.configure(state=tk.DISABLED)
        
        # Update status
        self.update_status()
        
        # Load existing chat history
        self.load_chat_history()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def show_settings(self):
        """Show settings window with tabbed interface"""
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.lift()
            return
            
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("ScreenAsk Settings")
        self.settings_window.geometry("750x650")
        self.settings_window.resizable(True, True)
        
        # Make it modal
        self.settings_window.transient(self.root)
        self.settings_window.grab_set()
        
        # Create main frame
        main_frame = ttk.Frame(self.settings_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create tabs
        self._create_api_tab(notebook)
        self._create_controls_tab(notebook)
        self._create_audio_tab(notebook)
        self._create_visual_tab(notebook)
        self._create_prompts_tab(notebook)
        
        # Create bottom button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Add test buttons on left
        test_frame = ttk.Frame(button_frame)
        test_frame.pack(side=tk.LEFT)
        
        test_api_btn = ttk.Button(test_frame, text="Test API", command=self.test_api)
        test_api_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        test_capture_btn = ttk.Button(test_frame, text="Test Capture", command=self.test_capture)
        test_capture_btn.pack(side=tk.LEFT)
        
        # Add main buttons on right
        main_buttons_frame = ttk.Frame(button_frame)
        main_buttons_frame.pack(side=tk.RIGHT)
        
        cancel_btn = ttk.Button(main_buttons_frame, text="Cancel", command=self.settings_window.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        save_btn = ttk.Button(main_buttons_frame, text="Save", command=self.save_settings)
        save_btn.pack(side=tk.RIGHT)
    
    def _create_api_tab(self, notebook):
        """Create API & Model configuration tab"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="API & Model")
        
        # Create scrollable frame for this tab
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollable components
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Settings content
        content_frame = ttk.Frame(scrollable_frame, padding="10")
        content_frame.pack(fill=tk.BOTH, expand=True)
        content_frame.columnconfigure(1, weight=1)
        
        # OpenAI Settings
        openai_frame = ttk.LabelFrame(content_frame, text="OpenAI Configuration", padding="10")
        openai_frame.pack(fill=tk.X, pady=(0, 20))
        openai_frame.columnconfigure(1, weight=1)
        
        ttk.Label(openai_frame, text="API Key:").grid(row=0, column=0, sticky=tk.W)
        self.api_key_entry = ttk.Entry(openai_frame, show="*", width=20)
        self.api_key_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        self.api_key_entry.insert(0, self.config.get_openai_key())
        
        ttk.Label(openai_frame, text="Model:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.model_var = tk.StringVar(value=self.config.get('OpenAI', 'model', 'gpt-4o'))
        model_combo = ttk.Combobox(openai_frame, textvariable=self.model_var, 
                                  values=["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"])
        model_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(10, 0))
        
        ttk.Label(openai_frame, text="Temperature:").grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        self.temperature_var = tk.DoubleVar(value=float(self.config.get('OpenAI', 'temperature', '0.1')))
        temperature_scale = ttk.Scale(openai_frame, from_=0.0, to=2.0, orient=tk.HORIZONTAL, 
                                    variable=self.temperature_var, length=200)
        temperature_scale.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(10, 0))
        
        # Temperature info label
        temp_info_label = ttk.Label(openai_frame, text="Lower values (0.1-0.3) for consistent coordinates, higher for creative responses", 
                                   font=('Arial', 8, 'italic'))
        temp_info_label.grid(row=3, column=0, columnspan=2, pady=(5, 0))
        
        # Enable mouse wheel scrolling for this tab
        def _on_mousewheel_api(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel_api)
    
    def _create_controls_tab(self, notebook):
        """Create Controls configuration tab"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Controls")
        
        # Settings content
        content_frame = ttk.Frame(tab, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        content_frame.columnconfigure(1, weight=1)
        
        # Hotkey Settings
        hotkey_frame = ttk.LabelFrame(content_frame, text="Hotkey Configuration", padding="10")
        hotkey_frame.pack(fill=tk.X, pady=(0, 20))
        hotkey_frame.columnconfigure(1, weight=1)
        
        ttk.Label(hotkey_frame, text="Record Hotkey:").grid(row=0, column=0, sticky=tk.W)
        self.hotkey_var = tk.StringVar(value=self.config.get_hotkey())
        hotkey_combo = ttk.Combobox(hotkey_frame, textvariable=self.hotkey_var,
                                   values=["ctrl+shift+s", "ctrl+alt+s", "ctrl+shift+a", "alt+shift+s"])
        hotkey_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        ttk.Label(hotkey_frame, text="Stop Speaking Hotkey:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.stop_hotkey_var = tk.StringVar(value=self.config.get_stop_speaking_hotkey())
        stop_hotkey_combo = ttk.Combobox(hotkey_frame, textvariable=self.stop_hotkey_var,
                                        values=["ctrl+shift+x", "ctrl+alt+x", "ctrl+shift+z", "alt+shift+x"])
        stop_hotkey_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(10, 0))
    
    def _create_audio_tab(self, notebook):
        """Create Audio & Speech configuration tab"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Audio & Speech")
        
        # Create scrollable frame for this tab
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollable components
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Settings content
        content_frame = ttk.Frame(scrollable_frame, padding="10")
        content_frame.pack(fill=tk.BOTH, expand=True)
        content_frame.columnconfigure(1, weight=1)
        
        # Audio Settings
        audio_frame = ttk.LabelFrame(content_frame, text="Audio Configuration", padding="10")
        audio_frame.pack(fill=tk.X, pady=(0, 20))
        audio_frame.columnconfigure(1, weight=1)
        
        # Enable/Disable audio recording
        self.audio_enabled_var = tk.BooleanVar(value=self.config.get_audio_recording_enabled())
        audio_enabled_check = ttk.Checkbutton(audio_frame, text="Enable audio recording", variable=self.audio_enabled_var)
        audio_enabled_check.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Add push-to-talk info
        info_label = ttk.Label(audio_frame, text="Push-to-talk: Hold hotkey to record, release to stop", font=('Arial', 9, 'italic'))
        info_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Label(audio_frame, text="Language:").grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.language_var = tk.StringVar(value=self.config.get('Audio', 'language', 'en-US'))
        language_combo = ttk.Combobox(audio_frame, textvariable=self.language_var,
                                     values=["en-US", "en-GB", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-PT", "ru-RU", "tr-TR"])
        language_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(5, 0))
        
        ttk.Label(audio_frame, text="Transcription Service:").grid(row=3, column=0, sticky=tk.W, pady=(5, 0))
        self.transcription_var = tk.StringVar(value=self.config.get('Audio', 'transcription_service', 'google'))
        transcription_combo = ttk.Combobox(audio_frame, textvariable=self.transcription_var,
                                          values=["google", "openai_whisper"], state="readonly")
        transcription_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(5, 0))
        
        # Update combo display values
        def update_transcription_display(event=None):
            value = self.transcription_var.get()
            if value == "google":
                transcription_combo.set("Google Speech Recognition")
            elif value == "openai_whisper":
                transcription_combo.set("OpenAI Whisper")
        
        # Set initial display value
        update_transcription_display()
        
        # Handle selection changes
        def on_transcription_change(event=None):
            display_value = transcription_combo.get()
            if display_value == "Google Speech Recognition":
                self.transcription_var.set("google")
            elif display_value == "OpenAI Whisper":
                self.transcription_var.set("openai_whisper")
        
        transcription_combo.bind('<<ComboboxSelected>>', on_transcription_change)
        transcription_combo.configure(values=["Google Speech Recognition", "OpenAI Whisper"])
        
        # TTS Settings
        tts_frame = ttk.LabelFrame(content_frame, text="Text-to-Speech", padding="10")
        tts_frame.pack(fill=tk.X, pady=(0, 20))
        tts_frame.columnconfigure(1, weight=1)
        
        ttk.Label(tts_frame, text="Speech Rate:").grid(row=0, column=0, sticky=tk.W)
        self.rate_var = tk.StringVar(value=self.config.get('TTS', 'rate', '200'))
        rate_scale = ttk.Scale(tts_frame, from_=50, to=400, orient=tk.HORIZONTAL, variable=self.rate_var)
        rate_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        ttk.Label(tts_frame, text="Volume:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.volume_var = tk.StringVar(value=self.config.get('TTS', 'volume', '0.8'))
        volume_scale = ttk.Scale(tts_frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL, variable=self.volume_var)
        volume_scale.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(10, 0))
        
        ttk.Label(tts_frame, text="TTS Engine:").grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        self.tts_engine_var = tk.StringVar(value=self.config.get_tts_engine())
        tts_engine_combo = ttk.Combobox(tts_frame, textvariable=self.tts_engine_var,
                                       values=["auto", "local", "google"], state="readonly")
        tts_engine_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(10, 0))
        
        # Add info label for TTS engine
        info_tts_label = ttk.Label(tts_frame, text="Auto: Google TTS for non-English, Local for English", 
                                   font=('Arial', 8, 'italic'))
        info_tts_label.grid(row=3, column=0, columnspan=2, pady=(5, 0))
        
        # Enable mouse wheel scrolling for this tab
        def _on_mousewheel_audio(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel_audio)
    
    def _create_visual_tab(self, notebook):
        """Create Visual Features configuration tab"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Visual Features")
        
        # Create scrollable frame for this tab
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollable components
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Settings content
        content_frame = ttk.Frame(scrollable_frame, padding="10")
        content_frame.pack(fill=tk.BOTH, expand=True)
        content_frame.columnconfigure(1, weight=1)
        
        # Response Settings
        response_frame = ttk.LabelFrame(content_frame, text="Response Configuration", padding="10")
        response_frame.pack(fill=tk.X, pady=(0, 20))
        response_frame.columnconfigure(1, weight=1)
        
        # Info label for structured response (always enabled now)
        info_structured_label = ttk.Label(response_frame, 
                                        text="ScreenAsk uses structured responses with point of interest coordinates\nfor precise element detection and visual feedback", 
                                        font=('Arial', 9, 'italic'))
        info_structured_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Example format
        example_label = ttk.Label(response_frame, text="Format: {\"x\": 150, \"y\": 200, \"r\": 100, \"tx\": \"Element description\"}", 
                                font=('Arial', 8, 'italic'), foreground="gray")
        example_label.grid(row=1, column=0, columnspan=2, pady=(0, 0))
        
        # Circle Overlay Settings
        overlay_frame = ttk.LabelFrame(content_frame, text="Circle Overlay Configuration (Experimental)", padding="10")
        overlay_frame.pack(fill=tk.X, pady=(0, 20))
        overlay_frame.columnconfigure(1, weight=1)
        
        # Enable/Disable circle overlay
        self.circle_overlay_enabled_var = tk.BooleanVar(value=self.config.get_circle_overlay_enabled())
        overlay_enabled_check = ttk.Checkbutton(overlay_frame, text="Enable circle overlay at POI location (Experimental)", 
                                               variable=self.circle_overlay_enabled_var)
        overlay_enabled_check.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))
        
        # Color selection
        ttk.Label(overlay_frame, text="Circle Color:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.circle_color_var = tk.StringVar(value=self.config.get_circle_overlay_color())
        color_frame = ttk.Frame(overlay_frame)
        color_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(5, 0))
        
        color_entry = ttk.Entry(color_frame, textvariable=self.circle_color_var, width=10)
        color_entry.grid(row=0, column=0, sticky=tk.W)
        
        # Color preset buttons
        color_presets = [
            ("#00FF00", "Green"),
            ("#FF0000", "Red"),
            ("#0000FF", "Blue"),
            ("#FFFF00", "Yellow"),
            ("#FF00FF", "Magenta"),
            ("#00FFFF", "Cyan")
        ]
        
        for i, (color, name) in enumerate(color_presets):
            btn = ttk.Button(color_frame, text=name, width=8,
                           command=lambda c=color: self.circle_color_var.set(c))
            btn.grid(row=0, column=i+1, padx=(5, 0))
        
        # Alpha (transparency)
        ttk.Label(overlay_frame, text="Transparency:").grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        self.circle_alpha_var = tk.DoubleVar(value=self.config.get_circle_overlay_alpha())
        alpha_scale = ttk.Scale(overlay_frame, from_=0.1, to=1.0, orient=tk.HORIZONTAL, 
                               variable=self.circle_alpha_var, length=200)
        alpha_scale.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(10, 0))
        
        # Duration
        ttk.Label(overlay_frame, text="Duration (seconds):").grid(row=3, column=0, sticky=tk.W, pady=(10, 0))
        self.circle_duration_var = tk.DoubleVar(value=self.config.get_circle_overlay_duration())
        duration_scale = ttk.Scale(overlay_frame, from_=1.0, to=10.0, orient=tk.HORIZONTAL, 
                                  variable=self.circle_duration_var, length=200)
        duration_scale.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(10, 0))
        
        # Animation type
        ttk.Label(overlay_frame, text="Animation:").grid(row=4, column=0, sticky=tk.W, pady=(10, 0))
        self.circle_animation_var = tk.StringVar(value=self.config.get_circle_overlay_animation())
        animation_combo = ttk.Combobox(overlay_frame, textvariable=self.circle_animation_var,
                                      values=["pulse", "fade", "grow", "static"], state="readonly")
        animation_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(10, 0))
        
        # Info label for circle overlay
        info_overlay_label = ttk.Label(overlay_frame, 
                                      text="Shows a colored circle at the point of interest while AI speaks", 
                                      font=('Arial', 8, 'italic'))
        info_overlay_label.grid(row=5, column=0, columnspan=2, pady=(10, 5))
        
        # Debug coordinates option
        self.debug_coords_var = tk.BooleanVar(value=self.config.get_circle_overlay_debug_coords())
        debug_coords_check = ttk.Checkbutton(overlay_frame, text="Show coordinates for debugging", 
                                           variable=self.debug_coords_var)
        debug_coords_check.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # Enable mouse wheel scrolling for this tab
        def _on_mousewheel_visual(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel_visual)
    
    def _create_prompts_tab(self, notebook):
        """Create Prompts configuration tab"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Prompts")
        
        # Create scrollable frame for this tab
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollable components
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Settings content
        content_frame = ttk.Frame(scrollable_frame, padding="10")
        content_frame.pack(fill=tk.BOTH, expand=True)
        content_frame.columnconfigure(1, weight=1)
        
        # Prompt Settings
        prompt_frame = ttk.LabelFrame(content_frame, text="Prompt Configuration", padding="10")
        prompt_frame.pack(fill=tk.X, pady=(0, 20))
        prompt_frame.columnconfigure(1, weight=1)
        
        ttk.Label(prompt_frame, text="System Prompt:").grid(row=0, column=0, sticky=(tk.W, tk.N), pady=(0, 5))
        self.system_prompt_text = tk.Text(prompt_frame, height=4, wrap=tk.WORD)
        self.system_prompt_text.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(0, 10))
        self.system_prompt_text.insert(tk.END, self.config.get('Prompts', 'system_prompt', 
                                                             'You are a helpful AI assistant that analyzes screenshots and provides clear, concise answers.'))
        
        ttk.Label(prompt_frame, text="Prepend Prompt:").grid(row=1, column=0, sticky=(tk.W, tk.N), pady=(0, 5))
        self.prepend_prompt_text = tk.Text(prompt_frame, height=3, wrap=tk.WORD)
        self.prepend_prompt_text.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(0, 10))
        self.prepend_prompt_text.insert(tk.END, self.config.get('Prompts', 'prepend_prompt', ''))
        
        ttk.Label(prompt_frame, text="Append Prompt:").grid(row=2, column=0, sticky=(tk.W, tk.N), pady=(0, 5))
        self.append_prompt_text = tk.Text(prompt_frame, height=3, wrap=tk.WORD)
        self.append_prompt_text.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(0, 0))
        self.append_prompt_text.insert(tk.END, self.config.get('Prompts', 'append_prompt', 
                                                             'Please be specific and helpful in your response.'))
        
        # Help text
        help_label = ttk.Label(prompt_frame, 
                              text="System: Base AI behavior • Prepend: Added before user questions • Append: Added after user questions", 
                              font=('Arial', 8, 'italic'), foreground="gray")
        help_label.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        
        # Enable mouse wheel scrolling for this tab
        def _on_mousewheel_prompts(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel_prompts)
        
    def save_settings(self):
        """Save settings to configuration"""
        # Save OpenAI settings
        self.config.set_openai_key(self.api_key_entry.get())
        self.config.set('OpenAI', 'model', self.model_var.get())
        self.config.set('OpenAI', 'temperature', str(self.temperature_var.get()))
        
        # Save hotkeys
        self.config.set_hotkey(self.hotkey_var.get())
        self.config.set_stop_speaking_hotkey(self.stop_hotkey_var.get())
        
        # Save audio settings
        self.config.set('Audio', 'language', self.language_var.get())
        self.config.set('Audio', 'transcription_service', self.transcription_var.get())
        self.config.set_audio_recording_enabled(self.audio_enabled_var.get())
        
        # Save TTS settings
        self.config.set('TTS', 'rate', self.rate_var.get())
        self.config.set('TTS', 'volume', self.volume_var.get())
        self.config.set_tts_engine(self.tts_engine_var.get())
        
        # Save response settings (structured format is always enabled now)
        self.config.set_structured_format_enabled(True)
        
        # Save circle overlay settings
        self.config.set_circle_overlay_enabled(self.circle_overlay_enabled_var.get())
        self.config.set_circle_overlay_color(self.circle_color_var.get())
        self.config.set_circle_overlay_alpha(self.circle_alpha_var.get())
        self.config.set_circle_overlay_duration(self.circle_duration_var.get())
        self.config.set_circle_overlay_animation(self.circle_animation_var.get())
        self.config.set_circle_overlay_debug_coords(self.debug_coords_var.get())
        
        # Save prompt settings
        self.config.set('Prompts', 'system_prompt', self.system_prompt_text.get('1.0', tk.END).strip())
        self.config.set('Prompts', 'prepend_prompt', self.prepend_prompt_text.get('1.0', tk.END).strip())
        self.config.set('Prompts', 'append_prompt', self.append_prompt_text.get('1.0', tk.END).strip())
        
        # Update handlers with fresh config
        self.openai_handler.setup_client()
        self.tts_handler.setup_voice()
        self.tts_handler.refresh_voice_settings()
        
        # Update main app components
        if self.main_app:
            # Reload config for all handlers
            self.main_app.config.load_config()
            self.main_app.openai_handler.setup_client()
            self.main_app.tts_handler.refresh_voice_settings()
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
            # Use the press and release methods for testing
            threading.Thread(target=self._test_capture_sequence, daemon=True).start()
    
    def _test_capture_sequence(self):
        """Test capture sequence with status updates"""
        if self.main_app:
            # Simulate press and immediate release for testing
            self.main_app.handle_hotkey_press()
            # Small delay to show recording status
            time.sleep(0.5)
            self.main_app.handle_hotkey_release()
            
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
        self.stop_hotkey_label.config(text=self.config.get_stop_speaking_hotkey())
    
    def update_recording_status(self, status, color="black"):
        """Update recording/processing status"""
        if hasattr(self, 'recording_status') and self.recording_status:
            try:
                self.recording_status.config(text=status, foreground=color)
                # Force GUI update
                if self.root:
                    self.root.update_idletasks()
            except Exception as e:
                print(f"Error updating recording status: {e}")
    
    def set_status_ready(self):
        """Set status to ready"""
        self.update_recording_status("Ready", "green")
    
    def set_status_recording(self):
        """Set status to recording"""
        self.update_recording_status("🔴 Recording...", "red")
    
    def set_status_processing(self):
        """Set status to processing"""
        self.update_recording_status("⚙️ Processing...", "orange")
    
    def set_status_analyzing(self):
        """Set status to analyzing"""
        self.update_recording_status("🤖 Analyzing...", "blue")
    
    def set_status_speaking(self):
        """Set status to speaking"""
        self.update_recording_status("🔊 Speaking...", "purple")
        
    def on_closing(self):
        """Handle window closing"""
        self.hide_to_tray()
        
    def quit_app(self):
        """Quit the application"""
        if self.root:
            self.root.destroy() 
    
    def load_chat_history(self):
        """Load and display existing chat history"""
        try:
            if self.main_app and hasattr(self.main_app, 'chat_history'):
                # Load from file if it exists
                self.main_app.chat_history.load_from_file()
                # Display all messages
                messages = self.main_app.chat_history.get_all_messages()
                for message in messages:
                    self.add_chat_message(message['sender'], message['message'], message['datetime'])
        except Exception as e:
            print(f"Error loading chat history: {e}")
    
    def add_chat_message(self, sender, message, timestamp=None):
        """Add a message to the chat display"""
        try:
            # Create message frame
            message_frame = tk.Frame(self.chat_scrollable_frame)
            message_frame.pack(fill=tk.X, padx=5, pady=2)
            
            # Get current time if not provided
            if timestamp is None:
                from datetime import datetime
                timestamp = datetime.now().strftime('%H:%M:%S')
            
            if sender == 'user':
                # User message (right aligned, blue)
                msg_frame = tk.Frame(message_frame, bg='#007ACC', relief='raised', bd=1)
                msg_frame.pack(side=tk.RIGHT, anchor='e', padx=(100, 0))
                
                # User label
                user_label = tk.Label(msg_frame, text=f"You ({timestamp})", 
                                    bg='#007ACC', fg='white', font=('Arial', 8, 'bold'))
                user_label.pack(anchor='w', padx=5, pady=(2, 0))
                
                # Message text
                msg_text = tk.Text(msg_frame, wrap=tk.WORD, height=1, width=30,
                                 bg='#007ACC', fg='white', font=('Arial', 10),
                                 relief='flat', bd=0, state='normal')
                msg_text.insert('1.0', message)
                msg_text.configure(state='disabled')
                msg_text.pack(padx=5, pady=(0, 5), fill=tk.BOTH, expand=True)
                
                # Auto-resize text widget based on content
                msg_text.update_idletasks()
                lines = int(msg_text.index('end-1c').split('.')[0])
                msg_text.configure(height=max(2, min(lines, 8)))
                
            else:
                # AI message (left aligned, green)
                msg_frame = tk.Frame(message_frame, bg='#28A745', relief='raised', bd=1)
                msg_frame.pack(side=tk.LEFT, anchor='w', padx=(0, 100))
                
                # AI label
                ai_label = tk.Label(msg_frame, text=f"AI ({timestamp})", 
                                  bg='#28A745', fg='white', font=('Arial', 8, 'bold'))
                ai_label.pack(anchor='w', padx=5, pady=(2, 0))
                
                # Message text
                msg_text = tk.Text(msg_frame, wrap=tk.WORD, height=1, width=40,
                                 bg='#28A745', fg='white', font=('Arial', 10),
                                 relief='flat', bd=0, state='normal')
                msg_text.insert('1.0', message)
                msg_text.configure(state='disabled')
                msg_text.pack(padx=5, pady=(0, 5), fill=tk.BOTH, expand=True)
                
                # Auto-resize text widget based on content
                msg_text.update_idletasks()
                lines = int(msg_text.index('end-1c').split('.')[0])
                msg_text.configure(height=max(2, min(lines, 8)))
            
            # Update scroll region and scroll to bottom
            self.chat_scrollable_frame.update_idletasks()
            self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
            self.chat_canvas.yview_moveto(1.0)
            
        except Exception as e:
            print(f"Error adding chat message: {e}")
    
    def clear_chat_history(self):
        """Clear all chat history"""
        try:
            if self.main_app and hasattr(self.main_app, 'chat_history'):
                self.main_app.chat_history.clear_history()
                
                # Clear the display
                for widget in self.chat_scrollable_frame.winfo_children():
                    widget.destroy()
                
                # Update scroll region
                self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
                
                messagebox.showinfo("Chat History", "Chat history cleared successfully!")
        except Exception as e:
            print(f"Error clearing chat history: {e}")
            messagebox.showerror("Error", f"Failed to clear chat history: {str(e)}")
    
    def update_chat_display(self):
        """Update the chat display with new messages"""
        try:
            if self.main_app and hasattr(self.main_app, 'chat_history'):
                # Get the latest message
                messages = self.main_app.chat_history.get_all_messages()
                
                # Add the most recent message if there are any new ones
                if messages:
                    # Get the count of currently displayed messages
                    current_count = len(self.chat_scrollable_frame.winfo_children())
                    
                    # Add any new messages
                    for i in range(current_count, len(messages)):
                        message = messages[i]
                        # Extract just the time from the datetime string
                        time_part = message['datetime'].split(' ')[1]
                        self.add_chat_message(message['sender'], message['message'], time_part)
        except Exception as e:
            print(f"Error updating chat display: {e}")
    
    def save_chat_history(self):
        """Save chat history to file"""
        try:
            if self.main_app and hasattr(self.main_app, 'chat_history'):
                self.main_app.chat_history.save_to_file()
        except Exception as e:
            print(f"Error saving chat history: {e}")