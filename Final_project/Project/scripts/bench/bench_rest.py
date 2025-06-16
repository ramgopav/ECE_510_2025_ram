"""
Latency of the CNN *after* the first Conv2D layer
(i.e., layers that still run in PyTorch when FPGA handles layer-1).
"""
import torch, time
from char_cnn import CharCNN

model = CharCNN().eval()
fake_feat = torch.randn(1, 32, 26, 26)   # pretend FPGA output

loops = 1000
t0 = time.perf_counter()
for _ in range(loops):
    with torch.no_grad():
        model.forward_from_conv2(fake_feat)
t1 = time.perf_counter()

print(f"Rest-of-CNN {(t1 - t0)*1e3/loops:.3f} ms")
