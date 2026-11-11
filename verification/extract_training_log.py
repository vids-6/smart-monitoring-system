"""Extract the YOLOv8 training log printed in notebooks/detection/03_Dataset_Exploration.ipynb (cell 14)
and parse the per-epoch validation rows into CSV. Values are copied from the log, not recomputed."""
import json, re, sys, csv
nb_path, log_out, csv_out = sys.argv[1:4]
nb = json.load(open(nb_path))
cell = nb["cells"][14]
text = "".join("".join(o.get("text", "")) for o in cell["outputs"])
text = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", text)
open(log_out, "w").write(text)
rows, epoch = [], None
for line in text.splitlines():
    m = re.match(r"\s+(\d+)/(\d+)\s+\S+G\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", line)
    if m: epoch = (int(m.group(1)), float(m.group(3)), float(m.group(4)), float(m.group(5)))
    m = re.match(r"\s+all\s+(\d+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", line)
    if m and epoch:
        rows.append([epoch[0], *epoch[1:], *m.groups()]); epoch = None
with open(csv_out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["epoch", "train_box_loss", "train_cls_loss", "train_dfl_loss", "val_images", "val_instances", "precision", "recall", "mAP50", "mAP50_95"])
    w.writerows(rows)
print(len(rows), "epoch rows parsed")
