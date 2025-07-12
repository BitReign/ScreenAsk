"""
ScreenAsk Setup Script
This script creates a virtual environment and installs dependencies.
"""

import subprocess
import sys
import os
import venv

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 7:
        print(f"✓ Python version {version.major}.{version.minor} is compatible")
        return True
    else:
        print(f"✗ Python version {version.major}.{version.minor} is not compatible. Requires Python 3.7+")
        return False

def create_virtual_environment():
    """Create a virtual environment"""
    venv_path = "venv"
    
    if os.path.exists(venv_path):
        print("✓ Virtual environment already exists")
        return venv_path
    
    try:
        print("Creating virtual environment...")
        venv.create(venv_path, with_pip=True)
        print("✓ Virtual environment created successfully")
        return venv_path
    except Exception as e:
        print(f"✗ Error creating virtual environment: {e}")
        return None

def get_venv_python(venv_path):
    """Get the Python executable path in the virtual environment"""
    if sys.platform == "win32":
        return os.path.join(venv_path, "Scripts", "python.exe")
    else:
        return os.path.join(venv_path, "bin", "python")

def get_venv_pip(venv_path):
    """Get the pip executable path in the virtual environment"""
    if sys.platform == "win32":
        return os.path.join(venv_path, "Scripts", "pip.exe")
    else:
        return os.path.join(venv_path, "bin", "pip")

def install_requirements(venv_path):
    """Install required packages in virtual environment"""
    pip_path = get_venv_pip(venv_path)
    
    print("Installing required packages in virtual environment...")
    try:
        subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])
        print("✓ All requirements installed successfully")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing requirements: {e}")
        return False

def create_run_script(venv_path):
    """Create a run script that uses the virtual environment"""
    python_path = get_venv_python(venv_path)
    
    # Windows batch file
    batch_content = f"""@echo off
echo Starting ScreenAsk...
"{python_path}" main.py
pause
"""
    
    with open("run_screenask_venv.bat", "w") as f:
        f.write(batch_content)
    
    print("✓ Created run_screenask_venv.bat")
    
    # PowerShell script
    ps_content = f"""# ScreenAsk PowerShell Runner
Write-Host "Starting ScreenAsk..."
& "{python_path}" main.py
Read-Host "Press Enter to exit..."
"""
    
    with open("run_screenask_venv.ps1", "w") as f:
        f.write(ps_content)
    
    print("✓ Created run_screenask_venv.ps1")

def create_desktop_shortcut(venv_path):
    """Create a desktop shortcut (Windows only)"""
    if sys.platform != "win32":
        print("Desktop shortcut creation only available on Windows")
        return False
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "ScreenAsk.lnk")
        target = get_venv_python(venv_path)
        wDir = os.getcwd()
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.Arguments = f'"{os.path.join(wDir, "main.py")}"'
        shortcut.WorkingDirectory = wDir
        shortcut.IconLocation = os.path.join(wDir, "screenask_icon.ico") if os.path.exists("screenask_icon.ico") else target
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
    print("=" * 60)
    print("         ScreenAsk Setup Script with Virtual Environment")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    # Create virtual environment
    venv_path = create_virtual_environment()
    if not venv_path:
        input("Press Enter to exit...")
        return
    
    # Install requirements
    if not install_requirements(venv_path):
        input("Press Enter to exit...")
        return
    
    # Create run scripts
    create_run_script(venv_path)
    
    # Optional: Create desktop shortcut
    print("\nOptional: Create desktop shortcut?")
    create_shortcut = input("Create desktop shortcut? (y/n): ").lower().strip()
    if create_shortcut in ['y', 'yes']:
        create_desktop_shortcut(venv_path)
    
    print("\n" + "=" * 60)
    print("         Setup Complete!")
    print("=" * 60)
    print("Virtual environment created at: ./venv")
    print("\nTo run ScreenAsk:")
    print("  Option 1: Double-click run_screenask_venv.bat")
    print("  Option 2: Run run_screenask_venv.ps1 in PowerShell")
    print(f"  Option 3: Manual: {get_venv_python(venv_path)} main.py")
    print("\nTo activate the virtual environment manually:")
    if sys.platform == "win32":
        print("  venv\\Scripts\\activate")
    else:
        print("  source venv/bin/activate")
    print("\nNext steps:")
    print("  1. Run the application using one of the methods above")
    print("  2. Configure your OpenAI API key in Settings")
    print("  3. Use the default hotkey Ctrl+Shift+S to capture")
    print("\nFor help, see README.md")
    print("=" * 60)
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    main() 