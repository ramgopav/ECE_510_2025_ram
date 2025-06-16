import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# Config
DATASET_PATH = "char_dataset"
BATCH_SIZE = 64
EPOCHS = 5
IMG_SIZE = 28

# Data transforms
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor()
])

# Load dataset
train_data = datasets.ImageFolder(DATASET_PATH, transform=transform)
train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True)

# Get number of classes
num_classes = len(train_data.classes)
print("Classes:", train_data.classes)


class CharCNN(nn.Module):
    def __init__(self):
        super().__init__()
        # ── original layers ─────────────────────────
        self.conv1 = nn.Conv2d(1, 32, 3)      # (28→26)
        self.conv2 = nn.Conv2d(32, 64, 3)     # (26→24)
        self.pool  = nn.MaxPool2d(2)          # (24→12)
        self.fc1   = nn.Linear(64 * 12 * 12, 128)
        self.fc2   = nn.Linear(128, 36)       # 36 classes (0-9A-Z)

    # ── normal full-network forward (software only) ──
    def forward(self, x):
        x = F.relu(self.conv1(x))
        return self._rest(x)

    # ── NEW: skip conv1 because FPGA already produced its output ──
    # expects x shape = (batch, 32, 26, 26)  from run_conv2d_hw()
    def forward_from_conv2(self, x):
        return self._rest(x)

    # ── shared tail of the network ──
    def _rest(self, x):
        x = F.relu(self.conv2(x))
        x = self.pool(x)                       # 64 × 12 × 12
        x = x.view(x.size(0), -1)              # flatten
        x = F.relu(self.fc1(x))
        return self.fc2(x)


# === Training function ===
def train(model):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    print("🚀 Training model...")
    for epoch in range(EPOCHS):
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

        print(f"Epoch {epoch+1} | Loss: {running_loss:.3f} | Accuracy: {100.*correct/total:.2f}%")

    print("✅ Training done!")

# === Only run training when this file is executed directly ===
if __name__ == "__main__":
    model = CharCNN()
    train(model)
    torch.save(model.state_dict(), "model.pth")
    print("✅ Model saved to model.pth")
