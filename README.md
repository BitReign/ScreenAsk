# ScreenAsk - AI-Powered Screen Analyzer

ScreenAsk is a Windows background application that captures screenshots and analyzes them using OpenAI's GPT-4 Vision API, combined with voice input and text-to-speech responses.

**A fun, experimental side project!** 🎉 Visit us at [sumfx.net](https://sumfx.net)

## Quick Start

1. **Install Dependencies**: `pip install -r requirements.txt`
2. **Run the Application**: `python main.py`
3. **Configure Settings**: Add your OpenAI API key in the settings
4. **Use the Hotkey**: Press `Ctrl+Shift+S` to capture and analyze

## Features

- 🖥️ **Screenshot Capture** with global hotkey
- 🎤 **Voice Input** for questions
- 🤖 **AI Analysis** with OpenAI GPT-4 Vision
- 🔊 **Text-to-Speech** responses
- 📍 **Structured Responses** with POI coordinates
- 🎯 **Circle Overlay** for visual feedback (Experimental)
- 📱 **System Tray** operation

## Project Structure

```
ScreenAsk/
├── main.py                    # Entry point
├── src/                       # Source code
│   ├── core/                  # Core application files
│   ├── handlers/              # Handler classes
│   ├── ui/                    # User interface components
│   └── utils/                 # Utility classes
├── assets/                    # Icons and images
├── scripts/                   # Build and run scripts
├── docs/                      # Documentation
├── config/                    # Configuration templates
└── venv/                      # Virtual environment
```

## Requirements

- Windows 10/11
- Python 3.7+
- OpenAI API key
- Microphone

## Installation Options

### Option 1: Automatic Setup (Recommended)
```bash
python scripts/setup.py
```

### Option 2: Manual Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Option 3: Quick Run Scripts
- Double-click `scripts/run_screenask_venv.bat`
- Or run `scripts/run_screenask_venv.ps1` in PowerShell

## Usage

1. **Start**: Run the application (main window and system tray icon appear)
2. **Configure**: Add your OpenAI API key in Settings
3. **Capture**: Press `Ctrl+Shift+S` (hold and speak your question)
4. **Analysis**: AI analyzes the screenshot and speaks the response
5. **System Tray**: Right-click tray icon to show the menu

## Configuration

Configure the application through **Settings** (5 tabbed sections):
- **API & Model**: OpenAI configuration
- **Controls**: Hotkey settings
- **Audio & Speech**: Audio and TTS settings
- **Visual Features**: Circle overlay (experimental)
- **Prompts**: System prompts

## Documentation

For detailed documentation, installation guides, troubleshooting, and advanced features, see:
- **[Full Documentation](docs/README.md)** - Complete user guide
- **[Structured Responses](docs/STRUCTURED_RESPONSE_README.md)** - Technical details

## Support

1. Check the [troubleshooting section](docs/README.md#troubleshooting)
2. Review configuration settings
3. Ensure all dependencies are installed

## License

This project is open source. Please respect OpenAI's usage policies.

---

**Note**: This application requires an OpenAI API key and will incur costs based on OpenAI's pricing for GPT-4 Vision API usage. 