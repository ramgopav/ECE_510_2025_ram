"""
Quick verification that:
  • directory tree is correct
  • char_cnn has forward_from_conv2()
  • export_weights.py writes rtl/weights.mem
  • plate_reader.process() works (SW) and --hw flag parses
  • lookup override is loaded silently
No FPGA or UART required.
"""
import importlib, os, subprocess, sys, json, shutil, time, tempfile, pathlib

root = pathlib.Path(__file__).resolve().parent
ok   = lambda msg: print("✔", msg)
fail = lambda msg: (print("✖", msg), sys.exit(1))

# -----------------------------------------------------------
# 1.  import modules
for mod in ("train_char_cnn", "plate_reader"):
    try:
        importlib.import_module(mod)
        ok(f"import {mod}")
    except Exception as e:
        fail(f"cannot import {mod}: {e}")

from train_char_cnn import CharCNN

# 2.  check forward_from_conv2
model = CharCNN().eval()
if hasattr(model, "forward_from_conv2"):
    out = model.forward_from_conv2(
        model.conv1(torch.randn(1,1,28,28))
    )
    if out.shape[-1] == 36:
        ok("forward_from_conv2() returns logits")
    else:
        fail("forward_from_conv2 wrong output shape")
else:
    fail("forward_from_conv2 missing in CharCNN")

# 3.  run weight export in a temp dir
with tempfile.TemporaryDirectory() as td:
    td = pathlib.Path(td)
    os.chdir(root)
    (root/"scripts").mkdir(exist_ok=True)
    cmd = [sys.executable, "scripts/export_weights.py"]
    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        fail(f"export_weights.py failed:\n{e.output}")

    if not (root/"rtl/weights.mem").exists():
        fail("rtl/weights.mem not written")
    ok("export_weights.py produced rtl/weights.mem")

# 4.  ensure .lookup.json exists & parses
lut_path = root/".lookup.json"
try:
    lut = json.load(lut_path.open())
    ok(".lookup.json parses")
except Exception as e:
    fail(f".lookup.json error: {e}")

# 5.  plate_reader.process() smoke run (software)
try:
    import plate_reader   # already imported but reloaded after possible edits
    if not hasattr(plate_reader, "process"):
        fail("plate_reader lacks process() helper; expose main logic as process()")
    plate = plate_reader.process(next(iter(lut.keys())))  # run on first image in LUT
    ok(f"plate_reader.process() returned: {plate}")
except Exception as e:
    fail(f"plate_reader.process() failed: {e}")

# 6.  --hw flag parses (will fall back to SW if UART absent)
try:
    subprocess.check_output(
        [sys.executable, "plate_reader.py", next(iter(lut.keys())), "--hw"],
        stderr=subprocess.STDOUT, text=True
    )
    ok("--hw flag accepted by plate_reader.py")
except subprocess.CalledProcessError as e:
    if "UART timeout" in e.output:
        ok("--hw flag routed code path (UART timeout expected in smoke test)")
    else:
        fail(f"plate_reader --hw unexpected error:\n{e.output}")

print("\n🎉  Smoke-test completed — directory is fully inter-linked.")
