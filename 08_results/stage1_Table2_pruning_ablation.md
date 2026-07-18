# Table 2: Pruning Strategy Ablation

| Pruning Strategy | Branches Pruned | mAP@0.5 | Delta mAP@0.5 | mAP@0.5:0.95 | Parameters | GFLOPs |
|---|---|---:|---:|---:|---:|---:|
| Baseline YOLOv8n | 0 | 0.759 | 0.000 | 0.447 | 3,012,018 | 8.2 |
| Random Pruning, mean of 3 runs | 1 | 0.7653 +/- 0.0021 | +0.0063 | 0.4410 +/- 0.0026 | 2,983,346 | 8.1 |
| L1-Norm Pruning | L4 to C14 | 0.763 | +0.004 | 0.438 | 3,007,922 | 8.1 |
| Entropy-Guided Pruning | L6 to C11 | 0.764 | +0.005 | 0.439 | 2,995,634 | 8.1 |

## Random Pruning Runs

| Run | Branch Removed | mAP@0.5 | mAP@0.5:0.95 | Parameters |
|---|---|---:|---:|---:|
| Run 1 | L9 to C20 | 0.767 | 0.442 | 2,946,482 |
| Run 2 | L4 to C14 | 0.763 | 0.438 | 3,007,922 |
| Run 3 | L12 to C17 | 0.766 | 0.443 | 2,995,634 |

## Evidence Boundary

All pruned models retained the baseline mAP@0.5 within the evaluated settings. However, the entropy-guided result is approximately equal to the mean random-pruning result and does not demonstrate a clear accuracy advantage over random pruning.

The reported GFLOPs values are rounded to one decimal place by Ultralytics. The apparent reduction from 8.2 to 8.1 GFLOPs should therefore be interpreted cautiously.

The L1-Norm criterion selected the same topology as Random Run 2. Its trained checkpoint and validation results were reused because the architecture, initialization, seed, and fine-tuning configuration were identical.

## Model-Version Note

The archived baseline checkpoint previously reported 3,006,818 parameters and 8.1 GFLOPs. Under the current Ultralytics parser, all final checkpoints were measured using a unified model-information command, yielding 3,012,018 parameters and 8.2 GFLOPs for the baseline. Table 2 uses this unified measurement口径.
