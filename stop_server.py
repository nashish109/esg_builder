#!/usr/bin/env python3
"""
Stop script for ESG Builder FastAPI backend.
"""

import os
import platform
import subprocess
import sys

def stop_server():
    """Stop the running FastAPI server."""
    system = platform.system().lower()

    if system == "windows":
        # On Windows, use taskkill to kill gunicorn/python processes
        try:
            # Kill gunicorn processes
            result = subprocess.run(
                ["taskkill", "/F", "/IM", "gunicorn.exe", "/T"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("Gunicorn server stopped successfully.")
            else:
                print("No gunicorn processes found or failed to stop.")

            # Also try to kill python processes running run_server.py
            # This is more complex, but for simplicity, we can skip or use a different approach
        except FileNotFoundError:
            print("taskkill not found. Please manually stop the server.")
            return

    else:
        # On Unix-like systems (Linux, macOS)
        try:
            # Find and kill gunicorn processes
            result = subprocess.run(
                ["pkill", "-f", "gunicorn"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("Gunicorn server stopped successfully.")
            else:
                print("No gunicorn processes found or failed to stop.")
        except FileNotFoundError:
            print("pkill not found. Please manually stop the server.")
            return

    print("If the server is still running, you may need to manually stop it.")
    print("On Windows: Use Task Manager or run 'taskkill /F /IM python.exe' (be careful, this kills all Python processes)")
    print("On Linux/macOS: Use 'pkill -f gunicorn' or 'pkill -f run_server.py'")

if __name__ == "__main__":
    stop_server()