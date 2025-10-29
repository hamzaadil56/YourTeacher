#!/usr/bin/env python3
"""
Script to run the YourTeacher Streamlit application
"""

import subprocess
import sys
import os


def main():
    """Run the Streamlit application"""
    print("🎓 Starting YourTeacher - AI Learning System")
    print("=" * 50)

    # Check if streamlit is installed
    try:
        import streamlit
        print("✅ Streamlit is available")
    except ImportError:
        print("❌ Streamlit not found. Installing...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "streamlit"])
        print("✅ Streamlit installed successfully")

    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(script_dir, "streamlit_app.py")

    print(f"📂 Running app from: {app_path}")
    print("🌐 Opening browser...")
    print("💡 Use Ctrl+C to stop the server")
    print("=" * 50)

    # Run streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", app_path,
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")


if __name__ == "__main__":
    main()
