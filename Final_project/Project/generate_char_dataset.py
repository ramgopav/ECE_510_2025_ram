import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm

# Set output path
output_dir = "char_dataset"
os.makedirs(output_dir, exist_ok=True)

# Characters: A-Z + 0-9
classes = [chr(i) for i in range(65, 91)] + [str(i) for i in range(10)]  # A-Z + 0-9
image_size = 28
images_per_class = 500

# Use PIL to render fonts
font_paths = [
    "arial.ttf",  # Default font
    "times.ttf",
    "cour.ttf",
    "comic.ttf"
]

def generate_char_image(char, font_path):
    img = Image.new('L', (image_size, image_size), color=255)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(font_path, size=24)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), char, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((image_size - w) / 2, (image_size - h) / 2), char, fill=0, font=font)
    
    # Convert to numpy + small random rotation
    np_img = np.array(img)
    angle = np.random.uniform(-15, 15)
    M = cv2.getRotationMatrix2D((image_size/2, image_size/2), angle, 1)
    rotated = cv2.warpAffine(np_img, M, (image_size, image_size), borderValue=255)
    return rotated

print("Generating synthetic character dataset...")
for char in tqdm(classes):
    class_dir = os.path.join(output_dir, char)
    os.makedirs(class_dir, exist_ok=True)
    
    for i in range(images_per_class):
        font_path = np.random.choice(font_paths)
        img = generate_char_image(char, font_path)
        cv2.imwrite(os.path.join(class_dir, f"{char}_{i}.png"), img)

print("✅ Dataset ready!")
