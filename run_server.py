#!/usr/bin/env python3
"""
Startup script for ESG Builder FastAPI backend using Gunicorn.
"""

import os
import subprocess
import sys
from pathlib import Path

# Load environment variables from .env file if it exists
env_file = Path('.env')
if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file)

# Import settings to ensure they are loaded
from config.settings import APP_HOST, APP_PORT

def main():
    """Start the FastAPI server using Gunicorn."""
    # Gunicorn command for FastAPI
    cmd = [
        'gunicorn',
        'backend.api.main:app',
        '--bind', f'{APP_HOST}:{APP_PORT}',
        '--workers', '4',
        '--worker-class', 'uvicorn.workers.UvicornWorker',
        '--access-logfile', '-',
        '--error-logfile', '-',
        '--log-level', 'info'
    ]

    print(f"Starting server on {APP_HOST}:{APP_PORT} with Gunicorn...")
    print(f"Command: {' '.join(cmd)}")

    try:
        # Run the command
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()