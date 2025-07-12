# Structured Response Feature

This document describes the structured response feature in ScreenAsk, which provides AI responses in a structured JSON format with point of interest (POI) coordinates, radius, and text data.

## Overview

ScreenAsk uses structured responses by default to provide detailed, actionable data that includes:

1. **Point of Interest Coordinates** - X,Y coordinates of the most relevant screen element
2. **Radius** - Size of the POI area for visual highlighting
3. **Response Text** - The actual text to be spoken by TTS

This structured approach enables precise element detection and visual feedback through experimental circle overlay features.

## Format

The structured response uses the following JSON format:
```json
{
  "x": 150,
  "y": 200, 
  "r": 100,
  "tx": "Login form detected at center of screen"
}
```

And can be exported in your requested format:
```
x:150,y:200,r:100,tx="Login form detected at center of screen"
```

## Configuration

### Settings Interface

ScreenAsk now features a modern tabbed settings interface with five main sections:

1. **API & Model** - OpenAI configuration and model settings
2. **Controls** - Hotkey configuration
3. **Audio & Speech** - Audio recording and TTS settings
4. **Visual Features** - Response configuration and experimental circle overlay
5. **Prompts** - System, prepend, and append prompt customization

### Accessing Settings

1. Run ScreenAsk
2. Right-click the system tray icon and select "Settings", or
3. Double-click the tray icon to show the main window, then click "Settings"
4. Navigate through the tabs to configure different aspects
5. Click "Save" to apply changes

### Configuration File

The system automatically manages `settings.ini` with the following relevant sections:

```ini
[Response]
structured_format = true  # Always enabled

[CircleOverlay]
enabled = true
color = #00FF00
alpha = 0.7
duration = 4.0
animation = pulse
debug_coords = false
```

## Usage

### Basic Usage

1. Configure your OpenAI API key in the "API & Model" tab
2. Set your preferred hotkeys in the "Controls" tab
3. Use the hotkey to capture and analyze a screen
4. The AI will respond with structured JSON data
5. The text portion will be spoken via TTS
6. POI data is available for applications and visual feedback

### Accessing POI Data

```python
# From main ScreenAsk application
poi_data = app.get_current_poi_data()
if poi_data:
    # Full structured data
    x = poi_data['x']
    y = poi_data['y'] 
    radius = poi_data['radius']
    text = poi_data['text']
    
    # User's requested format
    user_format = app.get_poi_in_user_format()
    # Returns: x:150,y:200,r:100,tx="Login form detected"
    
    # JSON format
    json_format = app.get_poi_as_json()
```

### Circle Overlay Integration (Experimental)

The experimental circle overlay feature provides visual feedback:

```python
poi_data = app.get_current_poi_data()
if poi_data:
    # Circle appears automatically at POI location
    center_x = poi_data['x']
    center_y = poi_data['y']
    radius = poi_data['radius']
    
    # While TTS speaks the text
    text_to_speak = poi_data['text']
    
    # System handles circle animation automatically
    # Configure appearance in "Visual Features" tab
```

## API Reference

### ScreenAskApp Methods

- `get_current_poi_data()` - Returns full POI data dictionary
- `get_poi_in_user_format()` - Returns data in x:10,y:50,r:300,tx="text" format
- `get_poi_as_json()` - Returns data as JSON string
- `test_circle_at_coordinates(x, y, radius)` - Test circle overlay at specific coordinates
- `test_coordinate_accuracy()` - Test coordinate accuracy with multiple positions
- `clear_coordinate_cache()` - Clear cached coordinates for fresh detection
- `hide_current_circle()` - Hide current circle overlay

### POIHandler Methods

- `set_current_poi(x, y, radius, text)` - Set POI data
- `get_current_poi()` - Get current POI data
- `get_poi_coordinates()` - Get (x, y) tuple
- `get_poi_radius()` - Get radius value
- `get_poi_text()` - Get text value
- `export_poi_data(format)` - Export in different formats ('json', 'simple', 'coordinates_only')
- `get_poi_history()` - Get history of POIs
- `has_poi()` - Check if POI exists
- `is_poi_recent(max_age_seconds)` - Check if POI is recent

## Testing

To test the structured response and experimental circle overlay features:

1. **Configure Settings:**
   - Run ScreenAsk
   - Open Settings (right-click tray icon or double-click to show main window)
   - Configure OpenAI API key in "API & Model" tab
   - Optionally enable circle overlay in "Visual Features" tab (marked as Experimental)
   - Customize circle appearance, animation, and duration
   - Save settings

2. **Test with Screenshot:**
   - Use the configured hotkey to capture and analyze a screenshot
   - The AI will return structured JSON data (always enabled)
   - If circle overlay is enabled, a circle will appear at the POI location
   - The text portion will be spoken via TTS

3. **Verify Console Output:**
   - Check console for structured response parsing
   - Look for coordinate validation (✅ within bounds, 📍 region detection)
   - Monitor circle overlay position confirmation
   - Check for any error messages

4. **Test Window Toggle:**
   - Double-click the tray icon to show/hide the main window
   - Use "Test API" and "Test Capture" buttons in settings

## File Structure

Core files:
- `poi_handler.py` - POI data management
- `circle_overlay.py` - Experimental visual circle overlay system
- `STRUCTURED_RESPONSE_README.md` - This documentation

Modified files:
- `openai_handler.py` - Enhanced structured response with improved POI detection
- `main.py` - POI handler and circle overlay integration
- `config.py` - Response and circle overlay configuration
- `main_gui.py` - Complete tabbed settings interface redesign
- `tray_handler.py` - Double-click window toggle functionality
- `settings_template.ini` - Updated configuration template

## Current Features

### Always-On Structured Responses
- Structured JSON responses are now mandatory for consistent POI detection
- Enhanced AI prompts for precise coordinate calculation
- Improved icon and taskbar element detection
- Coordinate validation and screen region analysis

### Experimental Circle Overlay
- Visual feedback showing POI location while AI speaks
- Multiple animation types: pulse, fade, grow, static
- Customizable color, transparency, duration
- Debug mode for coordinate verification
- Labeled as "Experimental" in UI

### Enhanced Settings Interface
- Modern tabbed interface with 5 logical sections
- Individual scrolling per tab for better organization
- Always-visible action buttons (Test API, Test Capture, Save, Cancel)
- Improved user experience with cleaner layout

### Improved Coordinate Accuracy
- Reduced default radius from 50-300 to 25-100 pixels
- Enhanced AI visual detection with specific instructions
- Icon-specific examples in prompts (Spotify, Chrome, file manager)
- Coordinate smoothing threshold reduced from 100px to 50px

## System Requirements

- Windows 10/11 (primary support)
- Python 3.8+
- OpenAI API key with GPT-4o access
- Audio input device (if using voice input)
- Screen resolution: tested on 2560x1440, supports various resolutions

## Troubleshooting

### Common Issues

1. **Structured responses not parsing correctly**
   - Check console output for JSON parsing errors
   - Verify OpenAI API key is configured in "API & Model" tab
   - Ensure model supports vision (gpt-4o, gpt-4o-mini, etc.)

2. **POI coordinates seem inaccurate**
   - Coordinates use screen coordinate system (0,0 at top-left)
   - Check console for coordinate validation messages
   - Use debug mode in circle overlay settings
   - Try `test_coordinate_accuracy()` method for testing

3. **Circle overlay not appearing**
   - Verify "Enable circle overlay" is checked in "Visual Features" tab
   - Check that POI coordinates are within screen bounds
   - Look for error messages in console output
   - Try different animation types or colors

4. **TTS voice setup errors**
   - Check for "Error setting up TTS voice" messages
   - Verify TTS engine selection in "Audio & Speech" tab
   - Try different TTS engines (auto, local, google)

5. **Window toggle not working**
   - Ensure main window was created successfully
   - Check for double-click event registration
   - Try right-click menu "Open" option as alternative

### Debug Features

- **Console Logging**: Detailed output for all operations
- **Coordinate Validation**: Automatic bounds checking with visual indicators
- **Screen Region Detection**: Shows relative position (top-left, bottom-center, etc.)
- **Circle Overlay Debug**: Optional coordinate display
- **API Testing**: Built-in API connection testing
- **Capture Testing**: Built-in screenshot capture testing

### Performance Notes

- Structured responses may take slightly longer due to enhanced AI analysis
- Circle overlay uses minimal system resources
- Coordinate caching reduces redundant AI requests
- Background operation maintains low CPU usage

## Examples

### Application Icon Detection
```
Input: "Spotify ikonu nerede" (Where is the Spotify icon?)
Output: {"x": 1220, "y": 1390, "r": 50, "tx": "Spotify ikonu ekranın alt kısmında, görev çubuğunda yer alıyor."}
Console: 📍 POI is in bottom-center region of screen
```

### Window Location
```
Input: "ScreenAsk penceresi nerede" (Where is the ScreenAsk window?)
Output: {"x": 1220, "y": 390, "r": 100, "tx": "ScreenAsk penceresi ekranın sol üst kısmında yer alıyor."}
Console: 📍 POI is in top-center region of screen
```

### Button Identification
```
Input: "Submit button nerede?" (Where is the submit button?)
Output: {"x": 500, "y": 600, "r": 80, "tx": "Submit button found at bottom-right of form"}
Console: ✅ POI coordinates are within screen bounds
```

## Future Enhancements

The structured format and POI system are designed for extensibility:
- Multiple POI points per response
- Different POI types and classifications
- Confidence scores for coordinate accuracy
- Action suggestions based on element type
- Enhanced animation and visual feedback options
- Integration with automation tools

## Support

For issues or questions about the structured response feature:
1. Check console output for detailed error messages
2. Use built-in "Test API" and "Test Capture" buttons
3. Verify configuration in the tabbed settings interface
4. Ensure OpenAI API key is properly configured with vision model access
5. Test coordinate accuracy with debug features

The structured response system provides a robust foundation for AI-powered screen analysis with precise element detection and visual feedback capabilities. 