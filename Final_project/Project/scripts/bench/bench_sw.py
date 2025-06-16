"""
End-to-end software latency:
  OpenCV preprocessing + full PyTorch CNN + lookup override
"""
import glob, time
import plate_reader  # assumes plate_reader.py exposes process(img_path)

images = sorted(glob.glob("data/Cars*.jpg"))
t0 = time.perf_counter()
for img in images:
    plate_reader.process(img)          # returns plate string
t1 = time.perf_counter()

ms_per = (t1 - t0) * 1000 / len(images)
print(f"SW pipeline: {len(images)} images → {ms_per:.1f} ms / image")
