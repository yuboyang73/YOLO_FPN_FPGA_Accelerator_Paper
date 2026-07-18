from pathlib import Path
import sys

import torch
from ultralytics import YOLO

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from extract_feature_entropy import (
    collect_images,
    resolve_dataset_split,
    spatial_channel_entropy,
)

MODEL = Path(
    "07_experiments/stage1_algorithm_baseline_pruning/"
    "A1_yolov8n_baseline_100ep/weights/best.pt"
)
DATA = Path("03_dataset/yolo_format/neu_det.yaml")
OUTPUT = SCRIPT_DIR / "all_concat_branch_entropy.txt"
CONCAT_LAYERS = [11, 14, 17, 20]

images = collect_images(resolve_dataset_split(DATA, "val"), limit=64)
model = YOLO(str(MODEL))
modules = model.model.model

records = {}
metadata = {}
current_image = {"path": ""}
seen = set()
handles = []


def make_pre_hook(layer_index):
    def pre_hook(_module, inputs):
        branches = inputs[0]
        source_spec = modules[layer_index].f

        for branch_index, tensor in enumerate(branches):
            key = (current_image["path"], layer_index, branch_index)

            if not current_image["path"] or key in seen:
                continue

            seen.add(key)

            source = source_spec[branch_index]
            source_layer = layer_index - 1 if source == -1 else source
            record_key = (layer_index, branch_index)

            entropy = spatial_channel_entropy(
                tensor,
                bins=256,
                eps=1e-8,
            )

            records.setdefault(record_key, []).append(entropy)
            metadata[record_key] = {
                "source_layer": source_layer,
                "shape": tuple(tensor.shape),
            }

    return pre_hook


for layer_index in CONCAT_LAYERS:
    handle = modules[layer_index].register_forward_pre_hook(
        make_pre_hook(layer_index)
    )
    handles.append(handle)

try:
    for image in images:
        current_image["path"] = str(image)

        model.predict(
            source=str(image),
            imgsz=640,
            device=0,
            save=False,
            verbose=False,
        )
finally:
    for handle in handles:
        handle.remove()


results = []

for (concat_layer, branch_index), entropy_list in records.items():
    values = torch.stack(entropy_list)
    shape = metadata[(concat_layer, branch_index)]["shape"]
    source_layer = metadata[(concat_layer, branch_index)]["source_layer"]

    _, channels, height, width = shape
    mean_entropy = values.mean().item()
    std_entropy = values.mean(dim=1).std(unbiased=False).item()
    activation_elements = channels * height * width

    results.append(
        {
            "concat_layer": concat_layer,
            "branch": branch_index,
            "source_layer": source_layer,
            "shape": shape,
            "samples": len(entropy_list),
            "mean_entropy": mean_entropy,
            "std_entropy": std_entropy,
            "activation_elements": activation_elements,
        }
    )

results.sort(key=lambda item: item["mean_entropy"])

lines = [
    "All YOLOv8n Concat Branch Entropy Results",
    "",
    "Ranking: low entropy to high entropy",
    "",
]

for rank, item in enumerate(results, start=1):
    lines.append(
        f"rank={rank} | "
        f"concat={item['concat_layer']} | "
        f"branch={item['branch']} | "
        f"source_layer={item['source_layer']} | "
        f"shape={item['shape']} | "
        f"samples={item['samples']} | "
        f"mean_entropy={item['mean_entropy']:.6f} | "
        f"std_entropy={item['std_entropy']:.6f} | "
        f"activation_elements={item['activation_elements']}"
    )

OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

print("\n".join(lines))
print(f"\nSaved to: {OUTPUT}")