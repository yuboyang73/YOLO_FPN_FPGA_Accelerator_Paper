# Stage 1 Step 5 - FPN/PAN Hook Shape Extraction

Purpose:
Verify that YOLOv8n Neck/FPN/PAN fusion-refinement layers can be hooked before
feature entropy computation.

Use environment:
conda activate yolo_fpga

Run from project root:
cd D:\.YOLO_FPN_FPGA_Accelerator_Paper

Default command:
python 07_experiments\stage1_algorithm_baseline_pruning\A2_entropy_pruning\extract_fpn_hook_shapes.py

Default checkpoint:
07_experiments/stage1_algorithm_baseline_pruning/A1_yolov8n_baseline_100ep/weights/best.pt

Default data yaml:
03_dataset/yolo_format/neu_det.yaml

Default hook layers:
12, 15, 18, 21

Default inspected split:
val

Default image count:
8

Expected outputs:
hook_tensor_shapes.csv
hook_tensor_shapes.txt

Pass criteria:
Each inspected image should produce records for layer 12, 15, 18, and 21.
Each recorded shape should be a 4D tensor in BxCxHxW format.

Expected approximate shapes for imgsz=640:
layer 12: 1x128x80x80
layer 15: 1x64x160x160
layer 18: 1x128x80x80
layer 21: 1x256x40x40

Next step:
Use the same hook layers to compute channel-wise spatial entropy and export
entropy_ranking.csv.
