"""
Extract YOLOv8n FPN/PAN hook tensor shapes for Stage 1 entropy analysis.

This script verifies that the selected fusion-refinement layers can be hooked
before computing feature-map entropy. It records tensor shapes only; it does not
save full feature tensors.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

import torch
import yaml
from ultralytics import YOLO


DEFAULT_MODEL = (
    "07_experiments/stage1_algorithm_baseline_pruning/"
    "A1_yolov8n_baseline_100ep/weights/best.pt"
)
DEFAULT_DATA = "03_dataset/yolo_format/neu_det.yaml"
DEFAULT_OUTPUT_DIR = "07_experiments/stage1_algorithm_baseline_pruning/A2_entropy_pruning"
DEFAULT_LAYERS = [12, 15, 18, 21]
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}


def resolve_dataset_split(data_yaml: Path, split: str) -> Path:
    with data_yaml.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    root = Path(data.get("path", "")).expanduser()
    if not root.is_absolute():
        root = (data_yaml.parent / root).resolve()

    split_value = data.get(split)
    if split_value is None:
        raise KeyError(f"Split '{split}' is not defined in {data_yaml}")

    split_path = Path(split_value).expanduser()
    if not split_path.is_absolute():
        split_path = root / split_path

    return split_path.resolve()


def collect_images(image_dir: Path, limit: int) -> list[Path]:
    if not image_dir.exists():
        raise FileNotFoundError(f"Image split directory does not exist: {image_dir}")

    images = sorted(
        p for p in image_dir.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES
    )
    if not images:
        raise FileNotFoundError(f"No images found under: {image_dir}")
    return images[:limit]


def tensor_shape(value: Any) -> str:
    if isinstance(value, torch.Tensor):
        return "x".join(str(dim) for dim in value.shape)
    if isinstance(value, (list, tuple)):
        return ";".join(tensor_shape(item) for item in value)
    return type(value).__name__


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Path to YOLO checkpoint.")
    parser.add_argument("--data", default=DEFAULT_DATA, help="Path to YOLO data yaml.")
    parser.add_argument("--split", default="val", choices=["train", "val", "test"])
    parser.add_argument("--layers", nargs="+", type=int, default=DEFAULT_LAYERS)
    parser.add_argument("--limit", type=int, default=8, help="Number of images to inspect.")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--device", default="0", help="Ultralytics device argument.")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    model_path = Path(args.model)
    data_yaml = Path(args.data)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    image_dir = resolve_dataset_split(data_yaml, args.split)
    images = collect_images(image_dir, args.limit)

    model = YOLO(str(model_path))
    modules = model.model.model

    records: list[dict[str, str]] = []
    current_image = {"path": ""}
    handles = []

    def make_hook(layer_idx: int):
        def hook(_module: torch.nn.Module, _inputs: Any, output: Any) -> None:
            records.append(
                {
                    "image": current_image["path"],
                    "layer": str(layer_idx),
                    "module": modules[layer_idx].__class__.__name__,
                    "shape": tensor_shape(output),
                }
            )

        return hook

    for layer_idx in args.layers:
        if layer_idx < 0 or layer_idx >= len(modules):
            raise IndexError(f"Layer index {layer_idx} is outside model range 0-{len(modules)-1}")
        handles.append(modules[layer_idx].register_forward_hook(make_hook(layer_idx)))

    try:
        for image_path in images:
            current_image["path"] = str(image_path)
            model.predict(
                source=str(image_path),
                imgsz=args.imgsz,
                device=args.device,
                save=False,
                verbose=False,
            )
    finally:
        for handle in handles:
            handle.remove()

    csv_path = output_dir / "hook_tensor_shapes.csv"
    txt_path = output_dir / "hook_tensor_shapes.txt"

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["image", "layer", "module", "shape"])
        writer.writeheader()
        writer.writerows(records)

    with txt_path.open("w", encoding="utf-8") as f:
        f.write("YOLOv8n FPN/PAN Hook Tensor Shape Record\n\n")
        f.write(f"model: {model_path.as_posix()}\n")
        f.write(f"data: {data_yaml.as_posix()}\n")
        f.write(f"split: {args.split}\n")
        f.write(f"image_dir: {image_dir}\n")
        f.write(f"layers: {', '.join(str(layer) for layer in args.layers)}\n")
        f.write(f"image_count: {len(images)}\n\n")
        for record in records:
            f.write(
                f"image={record['image']} | layer={record['layer']} | "
                f"module={record['module']} | shape={record['shape']}\n"
            )

    print(f"[OK] Hook records written to: {csv_path}")
    print(f"[OK] Text summary written to: {txt_path}")
    print(f"[OK] Images inspected: {len(images)}")
    print(f"[OK] Hook layers: {args.layers}")


if __name__ == "__main__":
    main()
