# Virtual Camera Controller

## Description
A Virtual Camera Controller is a software-based tool that manipulates, simulates, or enhances video feeds from a camera (real or virtual). It acts as an intermediary between a camera source (e.g., webcam, IP camera) and applications like Zoom, OBS Studio, Microsoft Teams, and other video conferencing or streaming platforms.

🔹 How It Works
Captures a live video feed from a physical or virtual camera.
Applies modifications such as filters, segmentation, background replacement, or blurring.
Redirects the modified video feed to applications as a virtual camera source.
## Requirements
- Python 3.x
- Uvicorn
- FastAPI
- PyVirtualCam
- OpenCV-Python
- Ultralytics

To install the required packages, run:
```
pip install -r requirements.txt
```

## Project Structure
```
.
├── .gitignore
├── engine.py
├── main.py
├── model.py
├── README.md
├── requirements.txt
├── static
│   ├── background.jpeg
│   └── index.html
└── stream_utils.py
```

- `main.py`: The main application file that defines the FastAPI app and its endpoints.
- `engine.py`: Contains the logic for managing video streaming.
- `model.py`: Defines the data models used in the application.
- `stream_utils.py`: Utility functions for streaming operations.
- `static/`: Directory containing static files, including HTML and images.
- `static/index.html`: The front-end interface for controlling the virtual camera.

## How to Run the Project
1. Clone the repository:
   ```
   git clone https://github.com/Vishal2053/Custom-Video-Broadcaster.git
   cd Custom-Video-Broadcaster
   ```
2. Install the requirements:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   uvicorn main:app --host 127.0.0.1 --port 8000
   ```

## Usage Instructions
- Open your web browser and navigate to `http://127.0.0.1:8000`.
- Use the interface to list available camera devices, start streaming, and stop streaming.
- Adjust the FPS and blur strength as needed.
