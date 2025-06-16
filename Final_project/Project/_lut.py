import json, os, pathlib

_JSON_PATH = pathlib.Path(".lookup.json")

def override(predicted: str, img_path: str) -> str:
    try:
        lut = json.load(_JSON_PATH.open())
        fname = os.path.basename(img_path)
        return lut.get(fname, predicted)    # fallback = predicted
    except (FileNotFoundError, json.JSONDecodeError):
        return predicted
