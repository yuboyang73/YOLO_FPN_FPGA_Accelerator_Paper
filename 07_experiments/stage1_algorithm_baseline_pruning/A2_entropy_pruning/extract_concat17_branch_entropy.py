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
OUTPUT = SCRIPT_DIR / "concat17_branch_entropy.txt"

images = collect_images(resolve_dataset_split(DATA, "val"), limit=64)
model = YOLO(str(MODEL))
concat17 = model.model.model[17]

records = {0: [], 1: []}
shapes = {}
current_image = {"path": ""}
seen = set()


def pre_hook(_module, inputs):
    branches = inputs[0]

    for branch_index, tensor in enumerate(branches):
        key = (current_image["path"], branch_index)

        if not current_image["path"] or key in seen:
            continue

        seen.add(key)
        shapes[branch_index] = tuple(tensor.shape)

        entropy = spatial_channel_entropy(
            tensor,
            bins=256,
            eps=1e-8,
        )
        records[branch_index].append(entropy)


handle = concat17.register_forward_pre_hook(pre_hook)

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
    handle.remove()


lines = ["Layer 17 Concat Branch Entropy", ""]

for branch_index in (0, 1):
    values = torch.stack(records[branch_index])
    shape = shapes[branch_index]
    _, channels, height, width = shape

    mean_entropy = values.mean().item()
    std_entropy = values.mean(dim=1).std(unbiased=False).item()
    activation_elements = channels * height * width

    source = "layer 16 downsample branch" if branch_index == 0 else "layer 12 skip branch"

    lines.append(
        f"branch={branch_index} | "
        f"source={source} | "
        f"shape={shape} | "
        f"samples={len(records[branch_index])} | "
        f"mean_entropy={mean_entropy:.6f} | "
        f"std_entropy={std_entropy:.6f} | "
        f"activation_elements={activation_elements}"
    )

OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

print("\n".join(lines))
print(f"\nSaved to: {OUTPUT}")