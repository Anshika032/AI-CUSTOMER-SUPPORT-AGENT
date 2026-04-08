import subprocess
import sys
import time


def main():
    api_process = subprocess.Popen([
        sys.executable,
        "-m",
        "uvicorn",
        "api:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8000",
    ])

    time.sleep(2)

    try:
        subprocess.run([
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app.py",
        ], check=True)
    finally:
        api_process.terminate()


if __name__ == "__main__":
    main()
