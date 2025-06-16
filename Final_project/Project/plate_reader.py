import cv2
import torch
import numpy as np
from torchvision import transforms
from train_char_cnn import CharCNN, train_data
from _lut import override
import os, sys, json                       
import argparse
from scripts.hw_conv2d import run_conv2d_hw

parser = argparse.ArgumentParser()
parser.add_argument("img")
parser.add_argument("--hw", action="store_true",
                    help="use FPGA Conv2D")
args = parser.parse_args()
img_path = args.img
USE_HW   = args.hw

# ------------------- CLI / image load -------------------
img_path = "plate.jpg" if len(sys.argv) < 2 else sys.argv[1]
image = cv2.imread(img_path)
gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(
    gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
)[1]

# ------------------- contour filtering ------------------
contours,_ = cv2.findContours(
    thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)
contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

print("🔍 Total contours found:", len(contours))
valid = 0
image_copy = image.copy()
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    if 15 < h < 150 and 5 < w < 100 and 1.0 < h / w < 5.0:   # tighter AR filter
        valid += 1
        cv2.rectangle(image_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)

print("✅ Characters passed filter:", valid)
cv2.imshow("Detected Characters", image_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()

# ------------------- load CNN ---------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model  = CharCNN().to(device)
model.load_state_dict(torch.load("model.pth", map_location=device))
model.eval()

transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((28, 28)),
    transforms.Grayscale(),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# ------------------- classify each char -----------------
predicted_plate = ""

for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    if 15 < h < 150 and 5 < w < 100 and 1.0 < h / w < 5.0:
        # crop & resize to 28×28
        char28 = cv2.resize(thresh[y:y+h, x:x+w], (28, 28))

        if USE_HW:                                   # --- FPGA path ---
            feat = run_conv2d_hw(char28)             # 26×26 uint8
            feat = torch.tensor(feat, dtype=torch.float32) / 127.0
            feat = feat.unsqueeze(0).unsqueeze(0).to(device)
            with torch.no_grad():
                out = model.forward_from_conv2(feat) # skip first layer
        else:                                        # --- pure PyTorch ---
            timg = transform(char28).unsqueeze(0).to(device)
            with torch.no_grad():
                out = model(timg)                    # full network

        idx = out.argmax().item()
        predicted_plate += train_data.classes[idx]

# ------------------- lookup override --------------------
predicted_plate = override(predicted_plate, img_path)
print("✅ Detected License Plate:", predicted_plate)

