# scripts/hw_conv2d.py
"""
UART bridge for FPGA Conv2D core.

• Uses 8-N-1 at 115 200 baud by default.
• The serial port is opened lazily the first time run_conv2d_hw() is called.
• Set environment variable  FPGA_PORT=COM5   (or /dev/ttyUSB0) if needed.
"""

import os, time, numpy as np
try:
    import serial
except ImportError:
    raise ImportError("pyserial not installed.  pip install pyserial")

PORT = os.getenv("FPGA_PORT", "COM3")   # change here or set env-var
BAUD = 115_200
_ser = None                             # will be opened on first use

def _ensure_open():
    global _ser
    if _ser is None:
        try:
            _ser = serial.Serial(PORT, BAUD, timeout=2)
            time.sleep(0.1)             # allow FPGA UART to settle
        except serial.SerialException as e:
            raise RuntimeError(f"UART '{PORT}' unavailable: {e}") from None

def run_conv2d_hw(img28: np.ndarray) -> np.ndarray:
    """
    Send a 28×28 uint8 glyph, receive a 26×26 uint8 feature-map.

    Raises RuntimeError on UART timeout or port error.
    """
    if img28.shape != (28, 28):
        raise ValueError("img28 must be 28×28")

    _ensure_open()

    _ser.write(img28.astype(np.uint8).tobytes())   # 784 bytes
    out = _ser.read(26 * 26)                       # expect 676 bytes
    if len(out) != 26 * 26:
        raise RuntimeError("UART timeout / incomplete frame")

    return np.frombuffer(out, np.uint8).reshape(26, 26)
