# Video Proctoring System

This project is a video proctoring system built in Python. It uses computer vision to monitor a candidate during an online interview and flag suspicious activities in real-time.

## Features

This system can detect and flag the following events:
* **Gaze Detection:** Detects if the candidate is not looking at the screen for more than 5 seconds.
* **Absence Detection:** Detects if no face is present in the video frame for more than 10 seconds.
* **Multiple Face Detection:** Detects if more than one face appears in the frame.
* **Unauthorized Item Detection:** Detects forbidden items like:
    * Mobile Phones
    * Books or Paper Notes
* **Event Logging & Reporting:** Logs all flagged events with timestamps and generates a final proctoring report with an integrity score.

## Technology Stack

* **Language:** Python
* **Computer Vision:** OpenCV, MediaPipe
* **Object Detection:** YOLOv8
* **Web App Framework:** Streamlit
* **Data Handling:** Pandas, NumPy

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Aniket-Singh07/Video-Proctoring_System.git](https://github.com/Aniket-Singh07/Video-Proctoring_System.git)
    cd Video-Proctoring-System
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

This project has two main files:

1.  **`main.py` (Full-Featured Local Version)**
    This version runs locally in an OpenCV window and has the best performance. It generates a detailed CSV report upon closing. To run it:
    ```bash
    python main.py
    ```

2.  **`app.py` (Simple Deployed Version)**
    This is a lightweight version for deployment that shows the live video feed. To run it:
    ```bash
    streamlit run app.py
    ```

    ### Project Versions

This repository contains two main executable files for the application:

* **`main.py` (Full-Featured Local Version):** This is the complete project file containing all the real-time AI features, including Focus Detection (Gaze, Absence, Multiple Faces), Object Detection (Phone, Books), and detailed report generation. It is designed to be run locally for the best performance and functionality. **The demo video was recorded using this version.**

* **`app.py` (Deployed Web Version):** This is a lightweight version created specifically to fulfill the "Live Deployed Link" requirement. It showcases the web application structure and live video streaming using Streamlit. To ensure a smooth user experience on standard hardware without a dedicated GPU, the computationally intensive, real-time AI models have been omitted from this deployed version. The complete code and functionality can be reviewed in the `main.py` file and the demo video.
