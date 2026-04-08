def main():
    import subprocess, sys
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py",
                   "--server.port=7860", "--server.address=0.0.0.0"])

if __name__ == "__main__":
    main()