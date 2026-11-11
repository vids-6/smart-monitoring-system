"""Inspect the two model files without modifying them. Prints architecture facts and embedded metadata.
Usage: python verification/inspect_models.py [--write-metadata results/detection/training]"""
import sys, os, json, hashlib, zipfile
import torch, torchvision
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DET = os.path.join(ROOT, "models", "detector", "best.pt")
CLS = os.path.join(ROOT, "models", "classifier", "grocery_classifier_1143.zip")
def sha256(p):
    h = hashlib.sha256(); h.update(open(p, "rb").read()); return h.hexdigest()
print("best.pt sha256:", sha256(DET))
ck = torch.load(DET, map_location="cpu", weights_only=False)   # Ultralytics checkpoint (pickled model object)
m = ck["model"] if ck.get("model") is not None else ck["ema"]
info = {
    "ultralytics_version_saved": ck.get("version"), "date": ck.get("date"),
    "epoch_index_saved": ck.get("epoch"), "epochs_completed": len(ck["train_results"]["epoch"]) if ck.get("train_results") else None,
    "optimizer_state_present": ck.get("optimizer") is not None, "best_fitness": ck.get("best_fitness"),
    "names": getattr(m, "names", None), "nc": m.yaml.get("nc"), "width_multiple": m.yaml.get("width_multiple"),
    "depth_multiple": m.yaml.get("depth_multiple"), "parameters": int(sum(p.numel() for p in m.parameters())),
    "train_metrics": ck.get("train_metrics"), "license": ck.get("license"),
}
print(json.dumps(info, indent=2, default=str))
print("\ngrocery_classifier_1143.zip sha256:", sha256(CLS))
sd = torch.load(CLS, map_location="cpu", weights_only=True)
print("type:", type(sd).__name__, "| tensors:", len(sd), "| non-tensor entries:", [k for k, v in sd.items() if not hasattr(v, "shape")])
net = torchvision.models.resnet18(weights=None, num_classes=sd["fc.weight"].shape[0])
print("ResNet18 strict load:", net.load_state_dict(sd, strict=True), "| classes:", sd["fc.weight"].shape[0])
if len(sys.argv) > 2 and sys.argv[1] == "--write-metadata":
    out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    json.dump(info, open(os.path.join(out, "best_pt_checkpoint_metadata.json"), "w"), indent=2, default=str)
    tr = ck["train_results"]; keys = list(tr.keys())
    with open(os.path.join(out, "best_pt_embedded_train_results.csv"), "w") as f:
        f.write(",".join(keys) + "\n")
        for i in range(len(tr["epoch"])): f.write(",".join(str(tr[k][i]) for k in keys) + "\n")
    import yaml
    yaml.safe_dump(ck["train_args"], open(os.path.join(ROOT, "configs", "best_pt_train_args.yaml"), "w"), sort_keys=False)
    print("metadata written")
