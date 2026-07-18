from pathlib import Path
import sys

import numpy as np
import torch
import torch.nn.functional as F
from ultralytics import YOLO

import cv2
from ultralytics.data.augment import LetterBox

SCRIPT_DIR = Path(__file__).resolve().parent
A2_DIR = SCRIPT_DIR.parent / "A2_entropy_pruning"
sys.path.insert(0, str(A2_DIR))

from extract_feature_entropy import (
    collect_images,
    resolve_dataset_split,
)

MODEL = (
    SCRIPT_DIR.parent
    / "A2_entropy_pruning"
    / "A2_entropy_pruned_finetune_50ep"
    / "weights"
    / "best.pt"
)
DATA = Path("03_dataset/yolo_format/neu_det.yaml")

SCALE = 256.0
QMIN = -32768
QMAX = 32767


def quantize_q8_8(tensor):
    integer = torch.round(tensor * SCALE)
    integer = torch.clamp(integer, QMIN, QMAX)
    quantized = integer / SCALE
    return integer.to(torch.int16), quantized


def save_flat_tensor(path, tensor):
    array = tensor.detach().cpu().numpy().reshape(-1)
    np.savetxt(path, array, fmt="%.8f")


images = collect_images(
    resolve_dataset_split(DATA, "val"),
    limit=1,
)
image_path = images[0]

yolo = YOLO(str(MODEL))
target = yolo.model.model[12].m[0].cv1.conv

captured = {}


def pre_hook(_module, inputs):
    captured["input"] = inputs[0].detach().float().cpu()


def forward_hook(_module, _inputs, output):
    captured["float_output"] = output.detach().float().cpu()


pre_handle = target.register_forward_pre_hook(pre_hook)
forward_handle = target.register_forward_hook(forward_hook)

try:
    image = cv2.imread(str(image_path))

    if image is None:
        raise FileNotFoundError(f"Cannot read image: {image_path}")

    letterbox = LetterBox(
        new_shape=(640, 640),
        auto=False,
        stride=32,
    )
    image = letterbox(image=image)

    image = image[:, :, ::-1]
    image = image.transpose(2, 0, 1).copy()

    input_tensor = torch.from_numpy(image)
    input_tensor = input_tensor.float() / 255.0
    input_tensor = input_tensor.unsqueeze(0)

    yolo.model.eval()

    with torch.no_grad():
        yolo.model(input_tensor)
finally:
    pre_handle.remove()
    forward_handle.remove()

if "input" not in captured or "float_output" not in captured:
    raise RuntimeError("The target convolution tensors were not captured.")

float_input = captured["input"]
float_output = captured["float_output"]
float_weight = target.weight.detach().float().cpu()

if target.bias is not None:
    raise RuntimeError(
        "The unfused target convolution should not contain a bias."
    )

float_replay = F.conv2d(
    float_input,
    float_weight,
    bias=None,
    stride=target.stride,
    padding=target.padding,
    dilation=target.dilation,
    groups=target.groups,
)

input_integer, quantized_input = quantize_q8_8(float_input)
weight_integer, quantized_weight = quantize_q8_8(float_weight)

fixed_output_float = F.conv2d(
    quantized_input,
    quantized_weight,
    bias=None,
    stride=target.stride,
    padding=target.padding,
    dilation=target.dilation,
    groups=target.groups,
)

output_integer, quantized_output = quantize_q8_8(
    fixed_output_float
)

save_flat_tensor(
    SCRIPT_DIR / "golden_input.txt",
    quantized_input,
)
save_flat_tensor(
    SCRIPT_DIR / "golden_output.txt",
    quantized_output,
)
save_flat_tensor(
    SCRIPT_DIR / "weights.txt",
    quantized_weight,
)

captured_replay_mse = F.mse_loss(
    float_replay,
    float_output,
).item()

mse_vs_float = F.mse_loss(
    quantized_output,
    float_replay,
).item()

input_saturation = int(
    ((input_integer == QMIN) | (input_integer == QMAX))
    .sum()
    .item()
)
weight_saturation = int(
    ((weight_integer == QMIN) | (weight_integer == QMAX))
    .sum()
    .item()
)
output_saturation = int(
    ((output_integer == QMIN) | (output_integer == QMAX))
    .sum()
    .item()
)

metadata = f"""B1 Golden Export Metadata

model: {MODEL.as_posix()}
image: {image_path}
target: model.model[12].m[0].cv1.conv
format: signed Q8.8
scale: 256
rounding: nearest
saturation: [{QMIN}, {QMAX}]

input_shape: {tuple(quantized_input.shape)}
output_shape: {tuple(quantized_output.shape)}
weight_shape: {tuple(quantized_weight.shape)}

input_values: {quantized_input.numel()}
output_values: {quantized_output.numel()}
weight_values: {quantized_weight.numel()}

input_saturation_count: {input_saturation}
output_saturation_count: {output_saturation}
weight_saturation_count: {weight_saturation}

captured_output_vs_float_replay_mse: {captured_replay_mse:.12e}
quantized_output_vs_float_replay_mse: {mse_vs_float:.12e}

serialization:
input/output = NCHW contiguous order
weights = OIHW contiguous order

output_boundary:
raw 3x3 convolution output before BatchNorm and SiLU
"""

(SCRIPT_DIR / "export_metadata.txt").write_text(
    metadata,
    encoding="utf-8",
)

print(metadata)
print("[OK] golden_input.txt")
print("[OK] golden_output.txt")
print("[OK] weights.txt")
print("[OK] export_metadata.txt")