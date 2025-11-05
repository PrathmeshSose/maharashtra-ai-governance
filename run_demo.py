#!/usr/bin/env python3
"""
Quick demo launcher for Maharashtra AI Governance Platform
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    packages = [
        'streamlit',
        'plotly', 
        'pandas',
        'numpy'
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ {package} installed")
        except:
            print(f"⚠️ {package} installation failed")

def run_dashboard():
    """Launch the dashboard"""
    print("🏛️ Launching Maharashtra AI Governance Platform...")
    print("🌐 Dashboard will open at: http://localhost:8503")
    print("=" * 50)
    
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 
            'working_dashboard.py', 
            '--server.port', '8503',
            '--server.headless', 'true'
        ])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped")

if __name__ == "__main__":
    print("🚀 Setting up Maharashtra AI Governance Platform...")
    install_requirements()
    run_dashboard()