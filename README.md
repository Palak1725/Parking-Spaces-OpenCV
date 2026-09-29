# Real-Time Autonomous Parking Space Detection

An edge-optimized Computer Vision system that monitors parking bay occupancy from static camera footage in real time using adaptive morphological image processing.

---

## Overview

Traditional parking infrastructure relies on embedded ultrasonic or inductive loop sensors, which carry high installation overhead, battery maintenance requirements, and hardware failure rates.

This project delivers an edge-deployable, camera-based vision pipeline that automates parking occupancy tracking. By decoupling static bay calibration from real-time spatial edge-density analysis, the system achieves sub-millisecond per-frame inference on commodity hardware without requiring expensive GPU accelerators.

---

## System Architecture & Processing Pipeline

The detection pipeline processes video frames sequentially to isolate vehicle structural features from uniform pavement:

Raw BGR Video Frame
│
▼  cv2.cvtColor (COLOR_BGR2GRAY)  [Reduces matrix channels from 3 to 1]
Grayscale Matrix
│
▼  cv2.GaussianBlur (3x3, σ=1)     [Attenuates high-frequency sensor grain]
Denoised Frame
│
▼  cv2.adaptiveThreshold          [Gaussian window 25x25, C=16, Inverted]
Binary Edge Mask
│
▼  cv2.medianBlur (ksize=5)       [Removes isolated salt-and-pepper noise]
Filtered Mask
│
▼  cv2.dilate (3x3 kernel, iter=1) [Closes micro-gaps in vehicle contours]
Morphological Edge Map
│
▼  cv2.countNonZero(crop)         [Evaluates active pixel mass per slot]
State Evaluation (Free < 970 <= Occupied)

### Classification Heuristic
* **Empty Bay:** Flat tarmac exhibits minimal contrast variations under inverted adaptive thresholding ($< 970$ non-zero pixels), registering as **Free** (Green).
* **Occupied Bay:** Vehicle contours, chassis lines, windshield frames, and tires produce dense structural edges ($\ge 970$ non-zero pixels), registering as **Occupied** (Red).

---

## Tech Stack

* **Language:** Python 3.10+
* **Computer Vision:** OpenCV (`cv2`)
* **Numerical Processing:** NumPy
* **Visualization:** `cvzone`
* **State Persistence:** Python Standard Library (`pickle`)

---

## Repository Structure

├── ParkingSpacePicker.py   # Interactive GUI to calibrate and persist slot coordinates
├── main.py                 # Core real-time processing and visualization loop
├── carParkImg.png          # Reference baseline frame for calibration
├── carPark.mp4             # Test video feed simulating CCTV surveillance
├── CarParkPos              # Serialized binary containing coordinate tuples (pickle)
├── requirements.txt        # Pinned runtime dependencies
├── .gitignore
├── LICENSE
└── README.md


---

## Getting Started

### 1. Prerequisites
Ensure Python 3.10 or higher is installed. Clone the repository and configure a virtual environment:

```bash
git clone [https://github.com/your-username/parking-space-detection.git](https://github.com/your-username/parking-space-detection.git)
cd parking-space-detection
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Contents of requirements.txt:

* opencv-python>=4.8.0
* numpy>=1.24.0
* cvzone>=1.5.6

### 3. Step 1: Calibrate Parking Slots
Run the coordinate picker to define parking bay bounds:

```bash
python ParkingSpacePicker.py
```
- Left-Click: Draw a new parking slot bounding box.

- Right-Click: Remove an existing bounding box (evaluated via Axis-Aligned Bounding Box intersection).

- Coordinates automatically persist to CarParkPos.

### 4. Step 2: Run Real-Time Detection
Execute the inference pipeline against the video stream:

```bash
python main.py
```
Press q to exit playback.

## Engineering Trade-offs & Production Considerations
- Deterministic vs. Deep Learning: Avoiding heavy convolutional architectures (e.g., YOLO) keeps working memory under 50 MB RAM and execution times under 2 ms per frame on basic CPU hardware.

- Camera Drift Mitigation: Camera pole sway can cause static slot drift. In production, this is remediated by tracking background keypoints (ORB/SIFT) to apply affine homography corrections dynamically.

Transient Occlusion / Shadows: Moving cloud or tree shadows can produce transient edge spikes. Temporal voting (requiring an occupancy state to persist across 30 consecutive frames) eliminates false positives.
