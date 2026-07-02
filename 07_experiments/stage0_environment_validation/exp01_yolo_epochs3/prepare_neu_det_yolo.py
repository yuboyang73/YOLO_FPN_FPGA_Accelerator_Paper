import argparse
import random
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import Counter, defaultdict

try:
    from PIL import Image
except ImportError:
    Image = None


CLASS_NAMES = [
    "crazing",
    "inclusion",
    "patches",
    "pitted_surface",
    "rolled-in_scale",
    "scratches",
]

CLASS_ALIASES = {
    "crazing": "crazing",
    "inclusion": "inclusion",
    "patches": "patches",
    "pitted_surface": "pitted_surface",
    "pitted surface": "pitted_surface",
    "pitted-surface": "pitted_surface",
    "rolled-in_scale": "rolled-in_scale",
    "rolled-in scale": "rolled-in_scale",
    "rolled_in_scale": "rolled-in_scale",
    "rolledinscale": "rolled-in_scale",
    "scratches": "scratches",
    "scratch": "scratches",
}


def normalize_class_name(name: str) -> str:
    name = name.strip().lower()
    name = name.replace("_", "_").replace("-", "-")
    if name in CLASS_ALIASES:
        return CLASS_ALIASES[name]
    raise ValueError(f"Unknown class name in XML: {name}")


def find_dirs(src: Path):
    xml_files = list(src.rglob("*.xml"))
    image_files = []
    for ext in ["*.jpg", "*.jpeg", "*.png", "*.bmp"]:
        image_files.extend(src.rglob(ext))

    if not xml_files:
        raise FileNotFoundError(f"No XML files found under: {src}")

    if not image_files:
        raise FileNotFoundError(f"No image files found under: {src}")

    return xml_files, image_files


def build_image_index(image_files):
    index = {}
    for img in image_files:
        index[img.stem] = img
    return index


def get_image_size_from_xml(root):
    size_node = root.find("size")
    if size_node is None:
        return None, None

    width_node = size_node.find("width")
    height_node = size_node.find("height")

    if width_node is None or height_node is None:
        return None, None

    width = int(float(width_node.text))
    height = int(float(height_node.text))
    return width, height


def get_image_size(image_path: Path, xml_root):
    width, height = get_image_size_from_xml(xml_root)

    if width and height:
        return width, height

    if Image is None:
        raise RuntimeError(
            "XML does not contain image size and Pillow is not installed. "
            "Please install it with: pip install pillow"
        )

    with Image.open(image_path) as im:
        width, height = im.size

    return width, height


def voc_bbox_to_yolo(xmin, ymin, xmax, ymax, img_w, img_h):
    x_center = ((xmin + xmax) / 2.0) / img_w
    y_center = ((ymin + ymax) / 2.0) / img_h
    width = (xmax - xmin) / img_w
    height = (ymax - ymin) / img_h

    return x_center, y_center, width, height


def parse_xml_to_yolo(xml_path: Path, image_path: Path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    img_w, img_h = get_image_size(image_path, root)

    labels = []
    class_counter = Counter()

    for obj in root.findall("object"):
        name_node = obj.find("name")
        bbox_node = obj.find("bndbox")

        if name_node is None or bbox_node is None:
            continue

        cls_name = normalize_class_name(name_node.text)
        cls_id = CLASS_NAMES.index(cls_name)

        xmin = float(bbox_node.find("xmin").text)
        ymin = float(bbox_node.find("ymin").text)
        xmax = float(bbox_node.find("xmax").text)
        ymax = float(bbox_node.find("ymax").text)

        xmin = max(0.0, min(xmin, img_w - 1))
        ymin = max(0.0, min(ymin, img_h - 1))
        xmax = max(0.0, min(xmax, img_w - 1))
        ymax = max(0.0, min(ymax, img_h - 1))

        if xmax <= xmin or ymax <= ymin:
            print(f"[WARNING] Invalid bbox skipped in {xml_path.name}: {xmin}, {ymin}, {xmax}, {ymax}")
            continue

        x, y, w, h = voc_bbox_to_yolo(xmin, ymin, xmax, ymax, img_w, img_h)

        if not all(0.0 <= v <= 1.0 for v in [x, y, w, h]):
            print(f"[WARNING] Out-of-range bbox skipped in {xml_path.name}: {x}, {y}, {w}, {h}")
            continue

        labels.append(f"{cls_id} {x:.6f} {y:.6f} {w:.6f} {h:.6f}")
        class_counter[cls_name] += 1

    return labels, class_counter


def split_dataset(items, train_ratio, val_ratio, test_ratio, seed):
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6

    random.seed(seed)
    random.shuffle(items)

    n = len(items)
    n_train = int(n * train_ratio)
    n_val = int(n * val_ratio)

    train_items = items[:n_train]
    val_items = items[n_train:n_train + n_val]
    test_items = items[n_train + n_val:]

    return train_items, val_items, test_items


def make_dirs(out: Path):
    for split in ["train", "val", "test"]:
        (out / "images" / split).mkdir(parents=True, exist_ok=True)
        (out / "labels" / split).mkdir(parents=True, exist_ok=True)


def write_yaml(out: Path):
    yaml_text = f"""path: {out.as_posix()}

train: images/train
val: images/val
test: images/test

names:
  0: crazing
  1: inclusion
  2: patches
  3: pitted_surface
  4: rolled-in_scale
  5: scratches
"""
    (out / "neu_det.yaml").write_text(yaml_text, encoding="utf-8")


def validate_yolo_dataset(out: Path):
    print("\n========== VALIDATION ==========")

    total_images = 0
    total_labels = 0
    total_boxes = 0
    class_counter = Counter()
    errors = []

    for split in ["train", "val", "test"]:
        img_dir = out / "images" / split
        label_dir = out / "labels" / split

        images = []
        for ext in ["*.jpg", "*.jpeg", "*.png", "*.bmp"]:
            images.extend(img_dir.glob(ext))

        labels = list(label_dir.glob("*.txt"))

        total_images += len(images)
        total_labels += len(labels)

        print(f"{split}: images={len(images)}, labels={len(labels)}")

        image_stems = {p.stem for p in images}
        label_stems = {p.stem for p in labels}

        missing_labels = image_stems - label_stems
        extra_labels = label_stems - image_stems

        if missing_labels:
            errors.append(f"{split}: missing labels for {len(missing_labels)} images")

        if extra_labels:
            errors.append(f"{split}: extra labels without images: {len(extra_labels)}")

        for label_file in labels:
            lines = label_file.read_text(encoding="utf-8").strip().splitlines()

            for line_id, line in enumerate(lines, start=1):
                parts = line.strip().split()

                if len(parts) != 5:
                    errors.append(f"{label_file}: line {line_id} does not have 5 fields")
                    continue

                cls_id = int(parts[0])
                vals = list(map(float, parts[1:]))

                if not (0 <= cls_id < len(CLASS_NAMES)):
                    errors.append(f"{label_file}: invalid class id {cls_id}")

                if not all(0.0 <= v <= 1.0 for v in vals):
                    errors.append(f"{label_file}: bbox value out of [0,1] at line {line_id}: {vals}")

                class_counter[CLASS_NAMES[cls_id]] += 1
                total_boxes += 1

    print(f"\nTotal images: {total_images}")
    print(f"Total label files: {total_labels}")
    print(f"Total boxes: {total_boxes}")

    print("\nClass distribution:")
    for name in CLASS_NAMES:
        print(f"  {name}: {class_counter[name]}")

    if errors:
        print("\n[FAILED] Validation errors found:")
        for e in errors[:20]:
            print("  -", e)
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more errors")
        raise RuntimeError("Dataset validation failed.")
    else:
        print("\n[PASSED] Dataset structure and YOLO labels are valid.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", type=str, required=True, help="Path to original NEU-DET folder")
    parser.add_argument("--out", type=str, required=True, help="Output YOLO-format folder")
    parser.add_argument("--train", type=float, default=0.7)
    parser.add_argument("--val", type=float, default=0.2)
    parser.add_argument("--test", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    src = Path(args.src).resolve()
    out = Path(args.out).resolve()

    print(f"Source folder: {src}")
    print(f"Output folder: {out}")

    xml_files, image_files = find_dirs(src)
    image_index = build_image_index(image_files)

    print(f"Found XML files: {len(xml_files)}")
    print(f"Found image files: {len(image_files)}")

    items = []
    missing_images = []

    for xml_path in xml_files:
        stem = xml_path.stem
        if stem not in image_index:
            missing_images.append(xml_path)
            continue
        items.append((xml_path, image_index[stem]))

    if missing_images:
        print(f"[WARNING] XML files without matching images: {len(missing_images)}")
        for p in missing_images[:10]:
            print("  ", p.name)

    if not items:
        raise RuntimeError("No matched image-XML pairs found.")

    make_dirs(out)

    train_items, val_items, test_items = split_dataset(
        items,
        args.train,
        args.val,
        args.test,
        args.seed
    )

    split_map = {
        "train": train_items,
        "val": val_items,
        "test": test_items,
    }

    global_counter = Counter()

    for split, split_items in split_map.items():
        print(f"\nProcessing {split}: {len(split_items)} samples")

        for xml_path, img_path in split_items:
            labels, counter = parse_xml_to_yolo(xml_path, img_path)
            global_counter.update(counter)

            dst_img = out / "images" / split / img_path.name
            dst_label = out / "labels" / split / f"{img_path.stem}.txt"

            shutil.copy2(img_path, dst_img)
            dst_label.write_text("\n".join(labels) + "\n", encoding="utf-8")

    write_yaml(out)
    validate_yolo_dataset(out)

    print("\nDone.")
    print(f"YOLO dataset saved to: {out}")
    print(f"YAML file: {out / 'neu_det.yaml'}")


if __name__ == "__main__":
    main()