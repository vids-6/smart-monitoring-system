"""Extract image outputs embedded in a notebook to files: <prefix>_cellNN_K.<ext>"""
import json, sys, base64, os
nb_path, out_dir, prefix = sys.argv[1:4]
os.makedirs(out_dir, exist_ok=True)
nb = json.load(open(nb_path)); n = 0
for ci, c in enumerate(nb["cells"]):
    k = 0
    for o in c.get("outputs", []):
        for mime, ext in (("image/png", "png"), ("image/jpeg", "jpg")):
            if mime in o.get("data", {}):
                d = o["data"][mime]; d = "".join(d) if isinstance(d, list) else d
                fn = os.path.join(out_dir, f"{prefix}_cell{ci:02d}_{k}.{ext}")
                open(fn, "wb").write(base64.b64decode(d)); k += 1; n += 1
                break
print(nb_path, "->", n, "images")
