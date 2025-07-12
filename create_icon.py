"""
Icon creation script for ScreenAsk
Generates application icons in multiple formats
"""

from PIL import Image, ImageDraw
import os

def create_icon():
    """Create application icon"""
    # Create a high-resolution icon
    size = 256
    image = Image.new('RGB', (size, size), color='#2196F3')  # Blue background
    draw = ImageDraw.Draw(image)
    
    # Draw screen/monitor shape
    screen_margin = 40
    screen_x1 = screen_margin
    screen_y1 = screen_margin
    screen_x2 = size - screen_margin
    screen_y2 = size - screen_margin - 30
    
    # Screen outline
    draw.rectangle([screen_x1, screen_y1, screen_x2, screen_y2], 
                  fill='#1976D2', outline='#0D47A1', width=4)
    
    # Screen inner area
    inner_margin = 20
    draw.rectangle([screen_x1 + inner_margin, screen_y1 + inner_margin, 
                   screen_x2 - inner_margin, screen_y2 - inner_margin], 
                  fill='#E3F2FD', outline='#1976D2', width=2)
    
    # Screen stand
    stand_width = 40
    stand_height = 20
    stand_x = (size - stand_width) // 2
    stand_y = screen_y2
    draw.rectangle([stand_x, stand_y, stand_x + stand_width, stand_y + stand_height], 
                  fill='#1976D2', outline='#0D47A1', width=2)
    
    # Base
    base_width = 80
    base_height = 8
    base_x = (size - base_width) // 2
    base_y = stand_y + stand_height
    draw.rectangle([base_x, base_y, base_x + base_width, base_y + base_height], 
                  fill='#0D47A1')
    
    # AI symbol (eye-like shape in center)
    center_x = size // 2
    center_y = (screen_y1 + screen_y2) // 2
    
    # Outer circle
    circle_radius = 30
    draw.ellipse([center_x - circle_radius, center_y - circle_radius,
                 center_x + circle_radius, center_y + circle_radius],
                fill='#FF9800', outline='#F57C00', width=3)
    
    # Inner circle (pupil)
    inner_radius = 15
    draw.ellipse([center_x - inner_radius, center_y - inner_radius,
                 center_x + inner_radius, center_y + inner_radius],
                fill='#2196F3', outline='#1976D2', width=2)
    
    # Highlight
    highlight_radius = 6
    highlight_x = center_x - 8
    highlight_y = center_y - 8
    draw.ellipse([highlight_x - highlight_radius, highlight_y - highlight_radius,
                 highlight_x + highlight_radius, highlight_y + highlight_radius],
                fill='#FFFFFF')
    
    return image

def save_icons():
    """Save icons in multiple formats and sizes"""
    print("Creating ScreenAsk icons...")
    
    # Create main icon
    icon = create_icon()
    
    # Save as PNG
    icon.save('screenask_icon.png', 'PNG')
    print("✓ Created screenask_icon.png")
    
    # Create ICO file with multiple sizes
    sizes = [16, 32, 48, 64, 128, 256]
    icons = []
    
    for size in sizes:
        resized = icon.resize((size, size), Image.Resampling.LANCZOS)
        icons.append(resized)
    
    # Save as ICO
    icon.save('screenask_icon.ico', format='ICO', sizes=[(s, s) for s in sizes])
    print("✓ Created screenask_icon.ico")
    
    # Save small PNG for tray
    tray_icon = icon.resize((64, 64), Image.Resampling.LANCZOS)
    tray_icon.save('tray_icon.png', 'PNG')
    print("✓ Created tray_icon.png")
    
    print("Icons created successfully!")

if __name__ == "__main__":
    save_icons() 