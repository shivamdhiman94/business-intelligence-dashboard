#!/usr/bin/env python3
"""
Business Dashboard Startup Script
Generates sample data and launches the interactive dashboard
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 Business Intelligence Dashboard Startup")
    print("=" * 50)
    
    # Check if we're in the right directory
    dashboard_dir = Path("c:/DASHBOARD DEVELOPMENT")
    if not dashboard_dir.exists():
        print("❌ Dashboard directory not found!")
        return
    
    os.chdir(dashboard_dir)
    
    # Generate sample data if it doesn't exist
    if not Path("sales_data.csv").exists():
        print("📊 Generating sample business data...")
        try:
            import subprocess
            result = subprocess.run([sys.executable, "data_generator.py"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Sample data generated successfully!")
            else:
                print(f"❌ Error generating data: {result.stderr}")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("✅ Using existing data files")
    
    print("\n🌐 Starting Interactive Dashboard...")
    print("📍 Dashboard URL: http://localhost:8050")
    print("⏹️  Press Ctrl+C to stop the dashboard\n")
    
    try:
        # Launch the dashboard
        subprocess.run([sys.executable, "dashboard_advanced.py"])
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")

if __name__ == "__main__":
    main()
