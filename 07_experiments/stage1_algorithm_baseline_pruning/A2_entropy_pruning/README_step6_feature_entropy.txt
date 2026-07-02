# Stage 1 Step 6 - Feature Entropy Measurement

Purpose:
Compute channel-wise spatial entropy for YOLOv8n FPN/PAN fusion-refinement
layers. This step measures information content only. It does not prune or modify
the model.

Use environment:
conda activate yolo_fpga

Run from project root:
cd D:\.YOLO_FPN_FPGA_Accelerator_Paper

Default command:
python 07_experiments\stage1_algorithm_baseline_pruning\A2_entropy_pruning\extract_feature_entropy.py

Default checkpoint:
07_experiments/stage1_algorithm_baseline_pruning/A1_yolov8n_baseline_100ep/weights/best.pt

Default data yaml:
03_dataset/yolo_format/neu_det.yaml

Default hook layers:
12, 15, 18, 21

Default inspected split:
val

Default image count:
64

Output files:
entropy_ranking.csv
entropy_summary.txt

Entropy definition:
For each channel c of feature map X, normalize values to [0, 1], estimate a
256-bin histogram p_c(b), then compute:

H_c = -sum_b p_c(b) * log2(p_c(b) + eps)

Layer-level entropy:
H_bar = mean_c(H_c)

Pass criteria:
The script should produce one summary row for each of layers 12, 15, 18, and 21.
Each row should include shape, sample count, mean_entropy, std_entropy,
activation_elements, and cost_entropy_ratio.

Interpretation:
Low entropy means the feature layer may contain less spatial information.
High activation_elements means the feature layer has higher hardware movement
cost. Candidate pruning decisions should consider both values:

low entropy + high hardware cost = stronger pruning candidate
high entropy + high hardware cost = not a first pruning candidate
low entropy + small-object sensitive layer = prune carefully

Next step:
Review entropy_ranking.csv, then decide candidate pruning layers or branches.
