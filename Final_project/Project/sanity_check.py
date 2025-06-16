import torch, numpy as np
from train_char_cnn import CharCNN

model = CharCNN().eval()
print("full :", model(torch.randn(1, 1, 28, 28)).shape)
print("skip :", model.forward_from_conv2(
                torch.randn(1, 32, 26, 26)).shape)
