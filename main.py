#!/usr/bin/env python3
"""
ScreenAsk - AI-powered screen analysis with voice interaction
A fun, experimental side project by sumfx.net

Entry point for the application.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def main():
    """Main entry point for ScreenAsk application"""
    try:
        # Import and run the core application
        from src.core.main import main as core_main
        
        # Run the application
        core_main()
        
        except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Failed to start ScreenAsk: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 