# ScreenAsk - AI-Powered Screen Analyzer

ScreenAsk is a Windows background application that captures screenshots and analyzes them using OpenAI's GPT-4 Vision API, combined with voice input and text-to-speech responses.

## Features

- 🖥️ **Screenshot Capture**: Capture entire screen with global hotkey
- 🎤 **Voice Input**: Record and transcribe your questions using speech-to-text
- 🤖 **AI Analysis**: Analyze screenshots with OpenAI GPT-4 Vision
- 🔊 **Text-to-Speech**: Hear responses spoken aloud
- 📱 **System Tray**: Background operation with system tray icon
- ⚙️ **Configurable**: Customizable hotkeys, audio settings, and more

## Requirements

- Windows 10/11
- Python 3.7 or higher
- OpenAI API key
- Microphone for voice input
- Internet connection

### Why Virtual Environment?

This project uses a virtual environment to:
- Isolate dependencies from your system Python
- Prevent conflicts with other Python projects
- Ensure consistent package versions
- Make installation and cleanup easier

## Installation

### Method 1: Automatic Setup with Virtual Environment (Recommended)

1. **Download or clone this repository**
2. **Run the setup script**:
   ```bash
   python setup.py
   ```
3. **Follow the on-screen instructions**
4. **Run the application**:
   ```bash
   # Option 1: Double-click run_screenask_venv.bat
   # Option 2: Run in PowerShell
   .\run_screenask_venv.ps1
   # Option 3: Manual
   venv\Scripts\python.exe main.py
   ```

### Method 2: Manual Installation with Virtual Environment

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment**:
   ```bash
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

### Method 3: System-wide Installation (Not Recommended)

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python main.py
   ```

## Configuration

### OpenAI API Key

1. Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Open ScreenAsk and go to **Settings**
3. Enter your API key in the **OpenAI Configuration** section
4. Click **Save**

### Hotkey Configuration

- Default hotkey: `Ctrl+Shift+S`
- Change in Settings → Hotkey Configuration
- Available combinations:
  - `Ctrl+Shift+S`
  - `Ctrl+Alt+S`
  - `Ctrl+Shift+A`
  - `Alt+Shift+S`

## Usage

### Basic Usage

1. **Start the application**: 
   - Double-click `run_screenask_venv.bat`, or
   - Run `venv\Scripts\python.exe main.py`, or
   - Activate venv first: `venv\Scripts\activate` then `python main.py`
2. **Configure settings**: Set your OpenAI API key and preferences
3. **Use the hotkey**: Press your configured hotkey (default: `Ctrl+Shift+S`)
4. **Speak your question**: When prompted, speak your question clearly
5. **Listen to the response**: The AI will analyze the screenshot and speak the response

### Virtual Environment Management

- **Activate**: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
- **Deactivate**: `deactivate` (when virtual environment is active)
- **Update packages**: `pip install --upgrade -r requirements.txt`
- **Remove environment**: Delete the `venv` folder

### System Tray

- **Right-click** the tray icon for menu options:
  - **Open**: Show main window
  - **Settings**: Open settings dialog
  - **About**: Show application information
  - **Exit**: Quit the application
- **Double-click** the tray icon to show the main window

### Main Window

- **Status section**: Shows OpenAI API status and current hotkey
- **Test API**: Verify OpenAI connection
- **Test Capture**: Test the screenshot and analysis process
- **Settings**: Configure all application settings
- **Hide to Tray**: Minimize to system tray

## Settings

### OpenAI Configuration
- **API Key**: Your OpenAI API key
- **Model**: AI model to use (default: gpt-4-vision-preview)
- **Max Tokens**: Maximum response length

### Hotkey Configuration
- **Hotkey**: Global hotkey combination

### Audio Configuration
- **Record Duration**: How long to record audio (1-30 seconds)
- **Language**: Speech recognition language

### Text-to-Speech
- **Speech Rate**: How fast to speak responses
- **Volume**: TTS volume level

## Troubleshooting

### Common Issues

1. **"OpenAI API not configured"**
   - Solution: Add your OpenAI API key in Settings

2. **"Failed to capture screenshot"**
   - Solution: Check screen permissions and try again

3. **"Could not understand audio"**
   - Solution: Speak clearly, check microphone, ensure quiet environment

4. **"Hotkey not working"**
   - Solution: Try a different hotkey combination, check if another app is using it

5. **"Audio recording failed"**
   - Solution: Check microphone permissions, ensure microphone is connected

### System Requirements

- **Microphone**: Required for voice input
- **Internet**: Required for OpenAI API and speech recognition
- **Permissions**: May need admin permissions for global hotkeys

## File Structure

```
ScreenAsk/
├── main.py                    # Main application entry point
├── config.py                  # Configuration management
├── tray_handler.py            # System tray functionality
├── main_gui.py                # Main GUI window
├── hotkey_handler.py          # Global hotkey detection
├── screenshot_handler.py      # Screenshot capture
├── audio_handler.py           # Audio recording and transcription
├── openai_handler.py          # OpenAI API integration
├── tts_handler.py             # Text-to-speech functionality
├── create_icon.py             # Icon generation script
├── requirements.txt           # Python dependencies
├── setup.py                   # Setup script with venv
├── run_screenask_venv.bat     # Windows batch runner (created by setup)
├── run_screenask_venv.ps1     # PowerShell runner (created by setup)
├── run_screenask.bat          # Simple batch runner (legacy)
├── README.md                  # This file
├── settings.ini               # Configuration file (created automatically)
├── venv/                      # Virtual environment (created by setup)
└── Icons/                     # Application icons (created by setup)
    ├── screenask_icon.png
    ├── screenask_icon.ico
    └── tray_icon.png
```

## Security and Privacy

- **Local Processing**: Audio transcription uses Google Speech Recognition
- **API Calls**: Screenshots and text are sent to OpenAI for analysis
- **Data Storage**: Only configuration settings are stored locally
- **No Persistence**: Screenshots and audio are not saved permanently

## Dependencies

- `pystray` - System tray functionality
- `Pillow` - Image processing
- `keyboard` - Global hotkey detection
- `PyQt5` - GUI framework
- `pyaudio` - Audio recording
- `SpeechRecognition` - Speech-to-text
- `pyttsx3` - Text-to-speech
- `openai` - OpenAI API client
- `pyautogui` - Screenshot capture

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please respect OpenAI's usage policies when using this application.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the configuration settings
3. Ensure all dependencies are installed correctly

## Version History

- **v1.0.0**: Initial release with core functionality
  - Screenshot capture
  - Voice input transcription
  - OpenAI GPT-4 Vision integration
  - Text-to-speech responses
  - System tray operation
  - Configurable settings

---

**Note**: This application requires an OpenAI API key and will incur costs based on OpenAI's pricing for GPT-4 Vision API usage. 