import cv2
import torch
import numpy as np
from torchvision import transforms
from train_char_cnn import CharCNN, train_data

# Load and preprocess the image
image = cv2.imread("plate.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

print("🔍 Total contours found:", len(contours))

valid = 0  # Count of characters that pass the filter
image_copy = image.copy()

# Draw debug rectangles
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    if h > 15 and w > 5 and h < 150 and w < 100:
        valid += 1
        cv2.rectangle(image_copy, (x, y), (x+w, y+h), (0, 255, 0), 2)

print("✅ Characters passed filter:", valid)

cv2.imshow("Detected Characters", image_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Load model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CharCNN().to(device)
model.load_state_dict(torch.load("model.pth", map_location=device))
model.eval()

transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((28, 28)),
    transforms.Grayscale(),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

output_str = ""

# Classify each valid character
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    if h > 15 and w > 5 and h < 150 and w < 100:
        char_img = thresh[y:y+h, x:x+w]
        char_img = cv2.copyMakeBorder(char_img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=0)
        char_img = transform(char_img).unsqueeze(0).to(device)

        with torch.no_grad():
            pred = model(char_img)
            idx = pred.argmax().item()
            output_str += train_data.classes[idx]

print("✅ Detected License Plate:", output_str)
