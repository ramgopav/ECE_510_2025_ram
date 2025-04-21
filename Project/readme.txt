# License Plate Character Recognition (CNN + OpenCV)

This is my final project for a custom AI/ML hardware acceleration pipeline. The goal was to create a system that can recognize the characters on a license plate using a trained CNN model and process real-world plate images using OpenCV. Eventually, this ties into a hardware convolution accelerator written in Verilog.

---

## 🚀 Project Overview

I built a full pipeline that:
- Generates synthetic character images (A–Z, 0–9)
- Trains a CNN model from scratch using PyTorch
- Detects and segments characters from real plate images using OpenCV
- Classifies each character to reconstruct the full plate string
- Includes a Verilog-based hardware accelerator for `conv2d` (CNN layer)

---

## 🧱 Folder Structure

license_plate_project/ ├── char_dataset/ # Synthetic dataset (A–Z, 0–9) ├── plate.jpg # Test image for license plate (cropped) ├── model.pth # Trained CNN model ├── generate_char_dataset.py # Script to create character dataset ├── train_char_cnn.py # CNN training (LeNet-style) ├── plate_reader.py # Main pipeline: image -> characters -> prediction ├── conv2d.sv # Basic convolution in Verilog ├── conv2d_sliding.sv # Sliding window CNN-style convolution ├── testbenches/ # Verilog testbenches



---

## 🧠 How It Works

### 1. Synthetic Dataset
I generated clean character images using OpenCV and saved them into folders for each label (0–9, A–Z).

### 2. CNN Training
I trained a simple CNN (similar to LeNet) using PyTorch to classify 36 characters. The model reached >99% accuracy on synthetic data.

### 3. License Plate Reader
Using OpenCV:
- Convert image to grayscale
- Threshold and invert
- Find contours and filter for character-like shapes
- Sort them left to right
- Classify each character using the trained CNN

Example output:
✅ Detected License Plate: ABC1234


### 4. Hardware Acceleration (Optional)
To explore hardware-software co-design, I wrote a `conv2d` accelerator in Verilog to simulate CNN behavior. This will be integrated into a chiplet-style hardware project using tools like Icarus Verilog and OpenLane.

---

## 📸 Example Plate Images

Tested with:
- `ADL-D21` (Colorado)
- `ABC-1234` (Pennsylvania)

Still not able to print The output predicted plate string using real contour detection.

---

## 🔧 How to Run

### 1. Install dependencies
```bash
pip install torch torchvision opencv-python

2. Generate dataset (optional if you already have it)
python generate_char_dataset.py

3. Train the CNN
python train_char_cnn.py

4. Run the license plate recognition
python plate_reader.py


🛠 Future Work
Integrate Verilog module into an end-to-end hardware co-simulation

Add automatic plate detection (e.g., YOLO or Haar cascade)

Improve robustness on real-world noisy images
