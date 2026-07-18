# Baseline and Pruning Ablation

## Experimental Setup

The algorithm-side evaluation was conducted on the NEU-DET dataset using a YOLOv8n detector with six defect categories. The baseline model was trained for 100 epochs at an input resolution of 640 × 640 with a batch size of 16. The pruning variants were initialized by transferring compatible weights from the trained baseline and were fine-tuned for 50 epochs under the same data configuration. The reported model complexity values were recomputed with a unified model-information procedure.

## Results

Table 1 summarizes the baseline and pruning results under the evaluated setting.

| Pruning Strategy | Branches Pruned | mAP@0.5 | mAP@0.5:0.95 | Parameters | GFLOPs |
|---|---:|---:|---:|---:|---:|
| Baseline YOLOv8n | 0 | 0.759 | 0.447 | 3,012,018 | 8.2 |
| Random Pruning, mean of three runs | 1 | 0.7653 ± 0.0021 | 0.4410 ± 0.0026 | 2,983,346 | 8.1 |
| L1-Norm Pruning | L4 to C14 | 0.763 | 0.438 | 3,007,922 | 8.1 |
| Entropy-Guided Pruning | L6 to C11 | 0.765 | 0.440 | 2,995,634 | 8.1 |

All pruned variants retained baseline-level mAP@0.5 in the current evaluation. However, the entropy-guided result is comparable to the random-pruning mean and does not establish a clear accuracy advantage over random pruning. The rounded GFLOPs values should also be interpreted cautiously because the reported difference is small.

## Evidence Boundary and Pending Reconciliation

The final pruning branch and its decision rule should be stated consistently. The branch-level entropy record identifies the L6-to-C11 branch, whereas the earlier fusion-refinement analysis selected layer 18 as a hardware-aware candidate. The exact selection rule connecting these analyses must be documented before submission.

In addition, the entropy fine-tuning `results.csv` records a maximum mAP@0.5 of 0.76405 and mAP@0.5:0.95 of 0.43882, while the consolidated table reports 0.765 and 0.440. An independent validation record for the checkpoint corresponding to the consolidated table should be added, or the table should be updated to match the archived log.

Therefore, the current results support the feasibility of the pruning pipeline and the preparation of HLS golden data, but they should not yet be used to claim superiority of entropy pruning over random pruning.
