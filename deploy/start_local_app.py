#!/usr/bin/env python3
"""
BytePay Local Development Server
Starts FastAPI backend with static frontend serving
"""

import os
import sys
import subprocess
import signal
import time
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_DIR = PROJECT_ROOT / "src" / "backend"
FRONTEND_DIR = PROJECT_ROOT / "src" / "frontend"
VENV_DIR = BACKEND_DIR / "venv"

def check_python_version():
    """Ensure Python 3.8+ is being used"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def setup_virtual_environment():
    """Create and setup virtual environment if it doesn't exist"""
    if not VENV_DIR.exists():
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)
    
    # Get the correct python executable from venv
    if os.name == 'nt':  # Windows
        python_exe = VENV_DIR / "Scripts" / "python.exe"
        pip_exe = VENV_DIR / "Scripts" / "pip.exe"
    else:  # Unix/Linux/macOS
        python_exe = VENV_DIR / "bin" / "python"
        pip_exe = VENV_DIR / "bin" / "pip"
    
    return python_exe, pip_exe

def install_dependencies(pip_exe):
    """Install backend dependencies"""
    requirements_file = BACKEND_DIR / "requirements.txt"
    if requirements_file.exists():
        print("📦 Installing backend dependencies...")
        subprocess.run([str(pip_exe), "install", "-r", str(requirements_file)], check=True)
    else:
        print("⚠️  No requirements.txt found")

def check_dev_server():
    """Check if development server file exists"""
    dev_main = BACKEND_DIR / "app" / "main_dev.py"
    if dev_main.exists():
        print("✅ Development server configuration found")
        return True
    else:
        print("❌ Development server file not found")
        return False

def start_server(python_exe):
    """Start the FastAPI server with hypercorn"""
    print("🚀 Starting BytePay local development server...")
    print(f"📁 Backend: {BACKEND_DIR}")
    print(f"📁 Frontend: {FRONTEND_DIR}")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📖 API docs will be available at: http://localhost:8000/docs")
    print("📁 Static files served from: /static/*")
    print("\n👆 Press Ctrl+C to stop the server\n")
    
    # Change to backend directory
    os.chdir(BACKEND_DIR)
    
    # Start hypercorn server with development main
    try:
        subprocess.run([
            str(python_exe), "-m", "hypercorn",
            "app.main:app",
            "--bind", "0.0.0.0:8000",
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 Shutting down server...")
    sys.exit(0)

def main():
    """Main function to start the local development server"""
    print("🎯 BytePay Local Development Server")
    print("=" * 40)
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Check Python version
        check_python_version()
        
        # Setup virtual environment
        python_exe, pip_exe = setup_virtual_environment()
        
        # Install dependencies
        install_dependencies(pip_exe)
        
        # Check development server exists
        if not check_dev_server():
            print("❌ Development server configuration missing")
            sys.exit(1)
        
        # Start the server
        start_server(python_exe)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()