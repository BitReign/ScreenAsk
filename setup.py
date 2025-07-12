"""
ScreenAsk Setup Script
This script helps install dependencies and set up the application.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing requirements: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 7:
        print(f"✓ Python version {version.major}.{version.minor} is compatible")
        return True
    else:
        print(f"✗ Python version {version.major}.{version.minor} is not compatible. Requires Python 3.7+")
        return False

def create_desktop_shortcut():
    """Create a desktop shortcut (Windows only)"""
    if sys.platform != "win32":
        print("Desktop shortcut creation only available on Windows")
        return False
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "ScreenAsk.lnk")
        target = os.path.join(os.getcwd(), "main.py")
        wDir = os.getcwd()
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{target}"'
        shortcut.WorkingDirectory = wDir
        shortcut.IconLocation = sys.executable
        shortcut.save()
        
        print("✓ Desktop shortcut created")
        return True
    except ImportError:
        print("✗ Cannot create desktop shortcut - winshell not available")
        return False
    except Exception as e:
        print(f"✗ Error creating desktop shortcut: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 50)
    print("         ScreenAsk Setup Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    # Install requirements
    if not install_requirements():
        input("Press Enter to exit...")
        return
    
    # Optional: Create desktop shortcut
    print("\nOptional: Create desktop shortcut?")
    create_shortcut = input("Create desktop shortcut? (y/n): ").lower().strip()
    if create_shortcut in ['y', 'yes']:
        create_desktop_shortcut()
    
    print("\n" + "=" * 50)
    print("         Setup Complete!")
    print("=" * 50)
    print("To run ScreenAsk:")
    print("  1. Run: python main.py")
    print("  2. Configure your OpenAI API key in Settings")
    print("  3. Use the default hotkey Ctrl+Shift+S to capture")
    print("\nFor help, see README.md")
    print("=" * 50)
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    main() 