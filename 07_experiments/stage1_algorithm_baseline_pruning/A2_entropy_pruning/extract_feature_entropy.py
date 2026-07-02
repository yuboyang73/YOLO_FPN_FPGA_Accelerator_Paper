"""
Compute feature-map entropy for selected YOLOv8n FPN/PAN layers.

This is Stage 1 Step 6. It measures information entropy only and does not prune
or modify the model. The output is used as evidence for later pruning decisions.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
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
    if limit <= 0:
        return images
    return images[:limit]


def spatial_channel_entropy(feature: torch.Tensor, bins: int, eps: float) -> torch.Tensor:
    """Return entropy per channel for one BCHW feature tensor."""
    if feature.ndim != 4:
        raise ValueError(f"Expected BCHW tensor, got shape {tuple(feature.shape)}")

    x = feature.detach().float().cpu()
    # Treat each image-channel map independently, then average over batch.
    b, c, _h, _w = x.shape
    x = x.reshape(b * c, -1)

    mins = x.min(dim=1, keepdim=True).values
    maxs = x.max(dim=1, keepdim=True).values
    ranges = (maxs - mins).clamp_min(eps)
    x = (x - mins) / ranges
    x = x.clamp(0.0, 1.0)

    entropies = []
    for row in x:
        hist = torch.histc(row, bins=bins, min=0.0, max=1.0)
        prob = hist / hist.sum().clamp_min(eps)
        entropy = -(prob * torch.log2(prob + eps)).sum()
        entropies.append(entropy)

    entropy_tensor = torch.stack(entropies).reshape(b, c)
    return entropy_tensor.mean(dim=0)


def shape_string(value: torch.Tensor) -> str:
    return "x".join(str(dim) for dim in value.shape)


def summarize_layer(records: list[dict[str, Any]]) -> dict[str, Any]:
    channel_entropy = torch.cat([item["channel_entropy"] for item in records], dim=0)
    first = records[0]
    _, channels, height, width = first["shape"]
    activation_elements = channels * height * width
    mean_entropy = float(channel_entropy.mean().item())
    hardware_cost_proxy = activation_elements
    cost_entropy_ratio = hardware_cost_proxy / max(mean_entropy, 1e-8)

    return {
        "layer": first["layer"],
        "module": first["module"],
        "shape": first["shape_str"],
        "samples": len(records),
        "channels": channels,
        "height": height,
        "width": width,
        "activation_elements": activation_elements,
        "mean_entropy": mean_entropy,
        "std_entropy": float(channel_entropy.std(unbiased=False).item()),
        "min_entropy": float(channel_entropy.min().item()),
        "max_entropy": float(channel_entropy.max().item()),
        "hardware_cost_proxy": hardware_cost_proxy,
        "cost_entropy_ratio": cost_entropy_ratio,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Path to YOLO checkpoint.")
    parser.add_argument("--data", default=DEFAULT_DATA, help="Path to YOLO data yaml.")
    parser.add_argument("--split", default="val", choices=["train", "val", "test"])
    parser.add_argument("--layers", nargs="+", type=int, default=DEFAULT_LAYERS)
    parser.add_argument("--limit", type=int, default=64, help="Images to use. Use 0 for all.")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--device", default="0", help="Ultralytics device argument.")
    parser.add_argument("--bins", type=int, default=256)
    parser.add_argument("--eps", type=float, default=1e-8)
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

    layer_records: dict[int, list[dict[str, Any]]] = defaultdict(list)
    seen_pairs: set[tuple[str, int]] = set()
    current_image = {"path": ""}
    handles = []

    def make_hook(layer_idx: int):
        def hook(_module: torch.nn.Module, _inputs: Any, output: Any) -> None:
            if not isinstance(output, torch.Tensor):
                return

            pair = (current_image["path"], layer_idx)
            if pair in seen_pairs:
                return
            seen_pairs.add(pair)

            channel_entropy = spatial_channel_entropy(output, bins=args.bins, eps=args.eps)
            layer_records[layer_idx].append(
                {
                    "image": current_image["path"],
                    "layer": layer_idx,
                    "module": modules[layer_idx].__class__.__name__,
                    "shape": tuple(output.shape),
                    "shape_str": shape_string(output),
                    "channel_entropy": channel_entropy,
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

    summaries = [summarize_layer(layer_records[layer]) for layer in args.layers]
    summaries_by_entropy = sorted(summaries, key=lambda item: item["mean_entropy"])
    for rank, item in enumerate(summaries_by_entropy, start=1):
        item["entropy_rank_low_to_high"] = rank

    ranking_path = output_dir / "entropy_ranking.csv"
    summary_path = output_dir / "entropy_summary.txt"

    fieldnames = [
        "entropy_rank_low_to_high",
        "layer",
        "module",
        "shape",
        "samples",
        "channels",
        "height",
        "width",
        "activation_elements",
        "mean_entropy",
        "std_entropy",
        "min_entropy",
        "max_entropy",
        "hardware_cost_proxy",
        "cost_entropy_ratio",
    ]

    with ranking_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summaries_by_entropy)

    with summary_path.open("w", encoding="utf-8") as f:
        f.write("YOLOv8n FPN/PAN Feature Entropy Summary\n\n")
        f.write(f"model: {model_path.as_posix()}\n")
        f.write(f"data: {data_yaml.as_posix()}\n")
        f.write(f"split: {args.split}\n")
        f.write(f"image_dir: {image_dir}\n")
        f.write(f"image_count: {len(images)}\n")
        f.write(f"layers: {', '.join(str(layer) for layer in args.layers)}\n")
        f.write(f"bins: {args.bins}\n")
        f.write(f"epsilon: {args.eps}\n\n")
        f.write("Entropy ranking, low to high:\n")
        for item in summaries_by_entropy:
            f.write(
                f"rank={item['entropy_rank_low_to_high']} | "
                f"layer={item['layer']} | module={item['module']} | "
                f"shape={item['shape']} | samples={item['samples']} | "
                f"mean_entropy={item['mean_entropy']:.6f} | "
                f"std_entropy={item['std_entropy']:.6f} | "
                f"activation_elements={item['activation_elements']} | "
                f"cost_entropy_ratio={item['cost_entropy_ratio']:.2f}\n"
            )
        f.write("\nInterpretation note:\n")
        f.write(
            "Lower mean entropy indicates a lower-information feature candidate. "
            "A high activation_elements or cost_entropy_ratio value indicates a "
            "larger feature-map movement cost. Pruning decisions should consider "
            "both entropy and hardware cost, and should not be made from entropy "
            "alone.\n"
        )

    print(f"[OK] Entropy ranking written to: {ranking_path}")
    print(f"[OK] Entropy summary written to: {summary_path}")
    print("[OK] Low-to-high entropy ranking:")
    for item in summaries_by_entropy:
        print(
            f"  rank {item['entropy_rank_low_to_high']}: "
            f"layer {item['layer']} ({item['module']}), "
            f"shape={item['shape']}, mean_entropy={item['mean_entropy']:.6f}"
        )


if __name__ == "__main__":
    main()
