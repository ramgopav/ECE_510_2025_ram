#!/usr/bin/env python3
"""
export_weights.py
-----------------
Quantises the *first* Conv2D layer of CharCNN to 8-bit fixed-point
and writes:

  • rtl/weights.mem   (32 lines × 9 bytes, hex)
  • scale.npy         (de-scale factor for the rest of the net)

Run this *after every re-train* before re-synthesising FPGA RTL.
"""
import numpy as np, torch, pathlib, os, sys
from train_char_cnn import CharCNN

OUT_DIR = pathlib.Path("rtl")
OUT_DIR.mkdir(exist_ok=True)

# ---- load model ----------------------------------------------------
try:
    state = torch.load("model.pth", map_location="cpu")
except FileNotFoundError:
    sys.exit("❌ model.pth not found. Train first:  python train_char_cnn.py")

model = CharCNN()
model.load_state_dict(state)
w = model.conv1.weight.detach().numpy()     # shape (32,1,3,3)

# ---- symmetric 8-bit quantisation ---------------------------------
abs_max = np.max(np.abs(w))
scale   = 127. / abs_max
w_q     = np.round(w * scale).astype(np.int8)   # −128..127
np.save(OUT_DIR / "scale.npy", np.float32([1/scale]))

# ---- write hex file for $readmemh ---------------------------------
with open(OUT_DIR / "weights.mem", "w") as f:
    for filt in w_q:                       # 32 filters
        line = "".join(f"{(int(v) & 0xFF):02X}" for v in filt.ravel())
        f.write(line + "\n")
print(f"✔  Wrote {OUT_DIR/'weights.mem'}  (32×9 bytes)")
print(f"✔  Wrote {OUT_DIR/'scale.npy'}")

