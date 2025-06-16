"""
Round-trip latency for the FPGA Conv2D core via UART.
Requires:
  • FPGA programmed with conv2d_top_uart bitstream
  • hw_conv2d.py configured with the correct COM port
"""
import time, numpy as np
from scripts.hw_conv2d import run_conv2d_hw   # adjust import if needed

dummy = np.zeros((28, 28), dtype=np.uint8)
run_conv2d_hw(dummy)        # warm-up

loops = 200
t0 = time.perf_counter()
for _ in range(loops):
    run_conv2d_hw(dummy)
t1 = time.perf_counter()

print(f"UART round-trip {(t1 - t0)*1e3/loops:.2f} ms")
