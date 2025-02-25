import subprocess
import sys
import time
import webbrowser


# Function to start the FastAPI backend
def start_backend():
    print("Starting FastAPI backend...")
    backend_process = subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
    return backend_process

# Function to start the Streamlit frontend
def start_frontend():
    print("Starting Streamlit frontend...")
    time.sleep(3)  # Wait for backend to start
    frontend_process = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "frontend/app.py"])
    return frontend_process

if __name__ == "__main__":
    backend_process = start_backend()
    time.sleep(5)  # Ensure backend is up before frontend starts
    frontend_process = start_frontend()
    
    # Open Streamlit app in browser
    webbrowser.open("http://localhost:8501")

    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("Shutting down...")
        backend_process.terminate()
        frontend_process.terminate()