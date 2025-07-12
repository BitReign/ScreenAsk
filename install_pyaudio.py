"""
PyAudio Installation Script for Windows
This script tries multiple methods to install PyAudio on Windows.
"""

import subprocess
import sys
import platform
import os

def install_with_pip():
    """Try installing PyAudio with pip"""
    print("Trying to install PyAudio with pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyAudio==0.2.11"])
        return True
    except subprocess.CalledProcessError:
        return False

def install_with_pipwin():
    """Try installing PyAudio with pipwin"""
    print("Trying to install PyAudio with pipwin...")
    try:
        # First install pipwin
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pipwin"])
        # Then install PyAudio
        subprocess.check_call([sys.executable, "-m", "pipwin", "install", "pyaudio"])
        return True
    except subprocess.CalledProcessError:
        return False

def install_precompiled_wheel():
    """Try installing from precompiled wheel"""
    print("Trying to install PyAudio from precompiled wheel...")
    
    # Determine Python version and architecture
    python_version = f"{sys.version_info.major}{sys.version_info.minor}"
    arch = "win_amd64" if platform.machine().endswith('64') else "win32"
    
    # Common precompiled wheel URLs
    wheel_urls = [
        f"https://download.lfd.uci.edu/pythonlibs/archived/PyAudio-0.2.11-cp{python_version}-cp{python_version}-{arch}.whl",
        "https://github.com/intxcc/pyaudio_portaudio/releases/download/v0.2.11/PyAudio-0.2.11-cp312-cp312-win_amd64.whl"
    ]
    
    for url in wheel_urls:
        try:
            print(f"Trying wheel: {url}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", url])
            return True
        except subprocess.CalledProcessError:
            continue
    
    return False

def main():
    """Main installation function"""
    print("=" * 50)
    print("PyAudio Installation Script for Windows")
    print("=" * 50)
    
    if platform.system() != "Windows":
        print("This script is designed for Windows only.")
        print("On other systems, try: pip install PyAudio")
        return
    
    print(f"Python version: {sys.version}")
    print(f"Architecture: {platform.machine()}")
    print()
    
    # Try different installation methods
    methods = [
        ("Standard pip", install_with_pip),
        ("Pipwin", install_with_pipwin),
        ("Precompiled wheel", install_precompiled_wheel)
    ]
    
    for method_name, method_func in methods:
        print(f"Method: {method_name}")
        if method_func():
            print(f"✓ PyAudio installed successfully with {method_name}")
            break
        else:
            print(f"✗ {method_name} failed")
    else:
        print("\n" + "=" * 50)
        print("All installation methods failed!")
        print("=" * 50)
        print("Manual installation options:")
        print("1. Install Visual Studio Build Tools")
        print("2. Download PyAudio wheel from:")
        print("   https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio")
        print("3. Install with: pip install downloaded_wheel.whl")
        print("4. Or use Windows Subsystem for Linux (WSL)")
        print("=" * 50)
        return False
    
    # Test the installation
    print("\nTesting PyAudio installation...")
    try:
        import pyaudio
        print("✓ PyAudio imported successfully")
        
        # Test basic functionality
        p = pyaudio.PyAudio()
        print(f"✓ PyAudio initialized - {p.get_device_count()} audio devices found")
        p.terminate()
        
        print("\n✓ PyAudio installation successful!")
        return True
        
    except Exception as e:
        print(f"✗ PyAudio test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    input("Press Enter to exit...")
    sys.exit(0 if success else 1) 