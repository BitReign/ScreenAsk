# ScreenAsk - AI-Powered Screen Analyzer

ScreenAsk is a Windows background application that captures screenshots and analyzes them using OpenAI's GPT-4 Vision API, combined with voice input and text-to-speech responses. Features structured response format with point-of-interest coordinates for advanced integrations and visual feedback.

## Features

- 🖥️ **Screenshot Capture**: Capture entire screen with global hotkey
- 🎤 **Voice Input**: Record and transcribe your questions using speech-to-text
- 🤖 **AI Analysis**: Analyze screenshots with OpenAI GPT-4 Vision
- 🔊 **Text-to-Speech**: Hear responses spoken aloud
- 📍 **Structured Responses**: Always returns POI coordinates and data in JSON format for integrations
- 🎯 **Circle Overlay**: Visual feedback with animated circles at points of interest (Experimental)
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

### Initial Setup

1. **Get your OpenAI API key** from [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Open ScreenAsk** and go to **Settings**
3. **Enter your API key** in the **OpenAI Configuration** section
4. **Configure your preferences** using the settings below
5. **Click Save**

### OpenAI Configuration
- **API Key**: Your OpenAI API key
- **Model**: AI model to use (default: gpt-4o)
- **Max Tokens**: Maximum response length

### Hotkey Configuration
- **Record Hotkey**: Global hotkey combination for capture/recording
- **Stop Speaking Hotkey**: Hotkey to stop TTS immediately

### Audio Configuration
- **Enable Recording**: Toggle push-to-talk audio recording
- **Language**: Speech recognition language
- **Transcription Service**: Google Speech Recognition or OpenAI Whisper

### Text-to-Speech
- **Speech Rate**: How fast to speak responses
- **Volume**: TTS volume level
- **TTS Engine**: Auto, Local (pyttsx3), or Google TTS

### Response Configuration
- **Structured Format**: Always uses JSON response format with POI coordinates
- **Format**: `{"x": 150, "y": 200, "r": 100, "tx": "Response text"}`

### Circle Overlay Configuration (Experimental)
- **Enable Overlay**: Show visual circle at POI location
- **Circle Color**: Customizable color with presets (Green, Red, Blue, Yellow, Magenta, Cyan)
- **Transparency**: Alpha from 0.1 (very transparent) to 1.0 (opaque)
- **Duration**: Display time from 1.0 to 10.0 seconds
- **Animation**: Pulse, Fade, Grow, or Static

### Prompt Configuration
- **System Prompt**: Base AI behavior instructions
- **Prepend Prompt**: Text added before user questions
- **Append Prompt**: Text added after user questions

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

### Advanced Features

#### Structured Responses
ScreenAsk always uses structured responses with POI coordinates for integration with other applications:
- **Returns JSON format**: `{"x": 150, "y": 200, "r": 100, "tx": "Response text"}`
- **Point of Interest data**: X,Y coordinates of relevant screen elements
- **Radius information**: Size of the area for highlighting or animations
- **Extractable text**: Separate text content for TTS or processing

#### Circle Overlay (Experimental)
Enable visual feedback in Settings → Circle Overlay Configuration:
- **Visual confirmation**: See where the AI is "looking" on your screen
- **Customizable appearance**: Choose colors, transparency, and animations
- **Automatic positioning**: Circle appears at AI-detected points of interest
- **Timed display**: Configurable duration from 1-10 seconds

#### Integration with External Applications
Access POI data programmatically:
```python
# Get current POI data
poi_data = app.get_current_poi_data()
if poi_data:
    x, y = poi_data['x'], poi_data['y']
    radius = poi_data['radius']
    text = poi_data['text']
    
    # Use for animations, highlighting, or other integrations
    draw_notification_circle(x, y, radius)
    speak_text(text)
```

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
- **Model**: AI model to use (default: gpt-4o)
- **Max Tokens**: Maximum response length

### Hotkey Configuration
- **Record Hotkey**: Global hotkey combination for capture/recording
- **Stop Speaking Hotkey**: Hotkey to stop TTS immediately

### Audio Configuration
- **Enable Recording**: Toggle push-to-talk audio recording
- **Language**: Speech recognition language
- **Transcription Service**: Google Speech Recognition or OpenAI Whisper

### Text-to-Speech
- **Speech Rate**: How fast to speak responses
- **Volume**: TTS volume level
- **TTS Engine**: Auto, Local (pyttsx3), or Google TTS

### Response Configuration
- **Structured Format**: Enable JSON response format with POI coordinates
- **Format**: `{"x": 150, "y": 200, "r": 100, "tx": "Response text"}`

### Circle Overlay Configuration (Experimental)
- **Enable Overlay**: Show visual circle at POI location
- **Circle Color**: Customizable color with presets (Green, Red, Blue, Yellow, Magenta, Cyan)
- **Transparency**: Alpha from 0.1 (very transparent) to 1.0 (opaque)
- **Duration**: Display time from 1.0 to 10.0 seconds
- **Animation**: Pulse, Fade, Grow, or Static

### Prompt Configuration
- **System Prompt**: Base AI behavior instructions
- **Prepend Prompt**: Text added before user questions
- **Append Prompt**: Text added after user questions

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

6. **"Circle overlay not showing"**
   - Solution: Enable "Circle overlay" in settings (structured format is always enabled)

7. **"Structured response format not working"**
   - Solution: Check console for JSON parsing errors, verify OpenAI API key is configured (structured format is always enabled)

8. **"Invalid JSON response from AI"**
   - Solution: The AI occasionally returns malformed JSON; check console for detailed error messages

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
├── poi_handler.py             # Point of Interest data management
├── circle_overlay.py          # Visual circle overlay system
├── create_icon.py             # Icon generation script
├── requirements.txt           # Python dependencies
├── setup.py                   # Setup script with venv
├── run_screenask_venv.bat     # Windows batch runner (created by setup)
├── run_screenask_venv.ps1     # PowerShell runner (created by setup)
├── run_screenask.bat          # Simple batch runner (legacy)
├── README.md                  # This file
├── STRUCTURED_RESPONSE_README.md  # Structured response documentation
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
- `sounddevice` - Audio recording
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
4. See [STRUCTURED_RESPONSE_README.md](STRUCTURED_RESPONSE_README.md) for detailed information about structured responses and circle overlays

## Version History

- **v1.1.0**: Enhanced with Structured Responses and Visual Feedback
  - Structured JSON response format with POI coordinates
  - Visual circle overlay system with animations
  - Point of Interest (POI) data management
  - Configurable circle colors, transparency, and animations
  - External application integration support
  - Enhanced settings UI with new configuration sections
  - Improved OpenAI response parsing with markdown support

- **v1.0.0**: Initial release with core functionality
  - Screenshot capture
  - Voice input transcription
  - OpenAI GPT-4 Vision integration
  - Text-to-speech responses
  - System tray operation
  - Configurable settings

---

**Note**: This application requires an OpenAI API key and will incur costs based on OpenAI's pricing for GPT-4 Vision API usage. 