# Entropy-Guided FPN Branch Pruning for YOLOv8n-Based Industrial Defect Detection: A Stage-I Experimental Study

> Conference-style Markdown draft.  
> This draft is written as a Stage-I experimental paper section and can later be merged into a full FPGA/HLS acceleration paper.  
> Figure positions are explicitly marked with textual placeholders. Replace the placeholders with final figures before submission.

---

## Abstract

Feature pyramid networks (FPNs) improve the multi-scale detection ability of modern object detectors, but their cross-layer feature fusion introduces additional intermediate feature-map storage and data movement. This overhead is particularly relevant for future field-programmable gate array (FPGA) deployment, where on-chip memory and external memory bandwidth are limited. This paper presents a Stage-I experimental study on entropy-guided FPN branch pruning for a YOLOv8n-based industrial defect detector. The proposed analysis captures intermediate feature maps from FPN/PAN fusion branches and estimates their spatial information entropy to identify candidate branches with relatively low activation diversity. A YOLOv8n baseline was trained on the NEU-DET defect dataset and compared with entropy-guided pruning, random pruning, and L1-norm pruning under the same pruning budget. The entropy-pruned model removed the Layer-6-to-Concat-11 branch and achieved 0.765 mAP@0.5 after 50 epochs of fine-tuning, compared with 0.759 for the baseline. However, the average random-pruning result was 0.7653 mAP@0.5, indicating that the current experiment supports the feasibility and interpretability of entropy-guided pruning but does not establish a clear accuracy advantage over random pruning. Finally, a quantized Q8.8 golden input, output, and weight set was exported from the fine-tuned entropy-pruned model to support subsequent HLS-based streaming convolution verification.

## Keywords

YOLOv8n; feature pyramid network; branch pruning; information entropy; industrial defect detection; FPGA; HLS; golden data.

---

## I. Introduction

Industrial surface defect detection requires accurate and efficient visual perception under constrained deployment conditions. Lightweight object detectors such as YOLO-family models are attractive for this task because they provide a practical balance between accuracy and computational cost. However, the feature pyramid network (FPN) and path aggregation network (PAN) components used in these detectors introduce multi-scale feature fusion through upsampling, downsampling, skip connections, and channel-wise concatenation. These operations improve detection performance, but they also increase the amount of intermediate feature-map storage and cross-layer data movement.

For GPU-based inference, this additional data movement is often hidden by a high-bandwidth memory hierarchy. In contrast, FPGA-based edge deployment must explicitly manage on-chip buffers, off-chip memory access, and streaming dataflow. Therefore, a branch that is useful from an accuracy perspective may still be expensive from a hardware perspective if it requires large feature maps to be preserved and reused across distant layers. This observation motivates a hardware-aware analysis of FPN branches before implementing the detector in high-level synthesis (HLS).

This paper reports the first-stage experiment of a larger YOLO/FPN FPGA acceleration workflow. The objective of this stage is not to implement the complete detector in hardware, but to determine whether selected FPN fusion branches can be removed while maintaining detection accuracy close to the baseline. The resulting pruned model then provides a stable software reference for the subsequent HLS implementation of a representative 3×3 convolution operator.

[Figure placeholder: Fig. 1. Overall Stage-I workflow, showing baseline training, FPN branch entropy measurement, pruning strategy comparison, and golden data export for HLS verification.]

The main contributions of this Stage-I study are as follows:

1. An activation-entropy-based procedure is used to analyze the information distribution of YOLOv8n FPN/PAN fusion branches.
2. A pruned YOLOv8n topology is constructed by removing one selected FPN skip branch and reconfiguring the subsequent fusion block.
3. Entropy-guided pruning is compared with random pruning and L1-norm pruning using mAP, parameter count, and GFLOPs.
4. Quantized Q8.8 golden data are exported from the fine-tuned pruned model to support the next-stage HLS implementation.

The remainder of this paper is organized as follows. Section II reviews related work categories. Section III describes the entropy-guided pruning method and the golden data export procedure. Section IV reports the experimental setup and pruning ablation results. Section V discusses the evidence boundary and limitations. Section VI concludes the Stage-I study.

---

## II. Related Work

### A. Lightweight Object Detection

Lightweight object detection aims to reduce computation and memory overhead while preserving detection accuracy. YOLO-family detectors are widely used in real-time and embedded perception because they combine convolutional backbones, multi-scale feature fusion, and dense detection heads in an efficient architecture. YOLOv8n is a compact variant suitable for resource-constrained settings. In this study, YOLOv8n is selected as the baseline detector because it provides a manageable model size while retaining FPN/PAN fusion structures that are relevant for hardware-oriented analysis.

> Citation placeholder: add YOLOv8 / Ultralytics citation here.

### B. Feature Pyramid Fusion and Hardware Cost

FPN and PAN structures improve detection across object scales by combining semantic information from deeper layers with spatial information from shallower layers. This is commonly achieved by upsampling, downsampling, and concatenating feature maps from different stages. Although such fusion is beneficial for detection accuracy, it can increase feature-map storage requirements and data movement. For FPGA deployment, these intermediate feature streams must be scheduled through on-chip buffers or off-chip memory, making FPN fusion a meaningful target for algorithm-hardware co-design.

> Citation placeholder: add FPN / PANet citations here.

### C. Network Pruning

Network pruning removes parameters, channels, layers, or branches to reduce model complexity. Weight-magnitude methods such as L1-norm pruning estimate importance from parameter values, while activation-based methods evaluate feature responses during inference. The entropy-guided strategy in this paper belongs to the activation-analysis category. It estimates the spatial information entropy of feature maps and uses the resulting score to guide branch selection. Unlike pure parameter pruning, this strategy directly observes feature-map distributions at FPN fusion points.

> Citation placeholder: add pruning survey / L1 pruning references here.

### D. FPGA-Oriented CNN Acceleration

FPGA-based CNN accelerators often use fixed-point arithmetic, line buffers, window buffers, and streaming pipelines to improve data reuse and reduce memory traffic. The present Stage-I experiment does not yet implement the hardware accelerator. Instead, it prepares the software-side model and golden data required for later HLS verification. This separation is important: model training and pruning are performed in the deep learning framework, whereas HLS will later implement a fixed inference operator.

> Citation placeholder: add HLS CNN accelerator / line-buffer references here.

---

## III. Methodology

### A. Baseline Detector and Candidate Fusion Branches

The baseline detector is YOLOv8n trained on the NEU-DET industrial defect dataset. The model contains a backbone for feature extraction, a neck for multi-scale feature fusion, and a detection head. The branch-pruning candidates are defined from the input branches of Concat layers in the neck. In the analyzed YOLOv8n topology, four Concat layers were identified:

| Concat Layer | Input Sources | Fusion Role |
|---:|---|---|
| 11 | `[-1, 6]` | Upsampled main path fused with Layer 6 skip feature |
| 14 | `[-1, 4]` | Upsampled main path fused with Layer 4 skip feature |
| 17 | `[-1, 12]` | Downsampled main path fused with Layer 12 feature |
| 20 | `[-1, 9]` | Downsampled main path fused with Layer 9 feature |

Among these candidates, skip branches are especially relevant for hardware-oriented pruning because they require earlier feature maps to be retained and later reused. Removing such a branch can simplify feature-flow scheduling and reduce intermediate data movement, provided that accuracy remains acceptable after fine-tuning.

### B. Entropy-Based Branch Scoring

For the \(k\)-th candidate branch, let its activation feature map be:

$$
X^{(k)} \in \mathbb{R}^{C_k \times H_k \times W_k},
$$

where \(C_k\), \(H_k\), and \(W_k\) denote the number of channels, height, and width, respectively. For each channel \(c\), the spatial activation values are normalized and discretized into a 256-bin histogram. The probability mass of bin \(b\) is denoted as \(p_c(b)\). The spatial entropy of channel \(c\) is computed as:

$$
H_c^{(k)} = -\sum_{b=0}^{255} p_c(b)\log_2(p_c(b)+\epsilon),
$$

where \(\epsilon\) is a small constant used for numerical stability. The branch-level entropy is obtained by averaging the channel entropy values:

$$
\bar{H}^{(k)} = \frac{1}{C_k}\sum_{c=1}^{C_k} H_c^{(k)}.
$$

The entropy score is used as an activation-distribution indicator rather than a standalone proof of branch redundancy. The final pruning decision also considers the structural role of each branch in the YOLOv8n FPN/PAN topology.

### C. Entropy Measurement Results

Forward hooks were registered to capture the input tensors of the Concat layers. The branch entropy ranking is shown in Table I.

**Table I. Branch Entropy Ranking of YOLOv8n FPN/PAN Fusion Inputs**

| Rank | Concat | Branch | Source Layer | Shape | Mean Entropy | Activation Elements |
|---:|---:|---:|---:|---|---:|---:|
| 1 | 20 | 0 | 19 | \(1\times128\times20\times20\) | 5.580449 | 51,200 |
| 2 | 17 | 0 | 16 | \(1\times64\times40\times40\) | 5.685125 | 102,400 |
| 3 | 11 | 1 | 6 | \(1\times128\times40\times40\) | 5.792360 | 204,800 |
| 4 | 14 | 1 | 4 | \(1\times64\times80\times80\) | 6.070816 | 409,600 |
| 5 | 14 | 0 | 13 | \(1\times128\times80\times80\) | 6.265172 | 819,200 |
| 6 | 17 | 1 | 12 | \(1\times128\times40\times40\) | 6.265172 | 204,800 |
| 7 | 11 | 0 | 10 | \(1\times256\times40\times40\) | 6.412962 | 409,600 |
| 8 | 20 | 1 | 9 | \(1\times256\times20\times20\) | 6.412962 | 102,400 |

Based on the entropy ranking and the structural role of the branches, the Layer-6-to-Concat-11 skip branch was selected for entropy-guided pruning.

[Figure placeholder: Fig. 2. FPN topology before and after entropy-guided pruning. Use `09_论文图片/Figure2_FPN_Topology_Before_After.pdf` or `09_论文图片/Figure2_FPN_Topology_Before_After.svg`. The figure should highlight that the Layer-6 skip branch connected to Concat-11 is removed.]

### D. Pruned Topology Construction

The original Concat-11 layer receives two inputs:

```yaml
Before: [[-1, 6], 1, Concat, [1]]
```

After pruning, the Layer-6 input is removed:

```yaml
After: [[-1], 1, Concat, [1]]
```

The modified topology was rebuilt and validated with a forward pass. The entropy-pruned model contains 2,995,634 parameters and 8.1 GFLOPs under the unified model-summary procedure. Compatible weights were transferred from the trained baseline checkpoint, with 354 out of 355 items loaded successfully. The model was then fine-tuned for 50 epochs.

### E. Golden Data Export for HLS Verification

To prepare the following HLS stage, a representative 3×3 convolution operator was exported from the fine-tuned entropy-pruned model:

```text
model.model[12].m[0].cv1.conv
```

This operator is a raw convolution before BatchNorm and SiLU activation. Its tensor dimensions are:

| Tensor | Shape | Layout |
|---|---|---|
| Input | \(1\times64\times40\times40\) | NCHW |
| Output | \(1\times64\times40\times40\) | NCHW |
| Weight | \(64\times64\times3\times3\) | OIHW |

The exported tensors were quantized into signed Q8.8 fixed-point format with nearest rounding and saturation range \([-32768,32767]\). The exported files are:

```text
golden_input.txt
golden_output.txt
weights.txt
export_metadata.txt
```

The captured output exactly matched the floating-point replay before quantization, with a captured-output-versus-float-replay MSE of 0. The Q8.8 output had a float-replay MSE of \(1.996489590965\times10^{-4}\), and no input, output, or weight saturation was observed. In the next HLS stage, the hardware output should be compared with `golden_output.txt`; this HLS-to-golden comparison is separate from the float-to-Q8.8 quantization error.

[Figure placeholder: Fig. 3. Golden data export pipeline. Show entropy-pruned YOLOv8n checkpoint → selected 3×3 convolution → Q8.8 quantization → golden_input.txt, golden_output.txt, and weights.txt → HLS C simulation input.]

---

## IV. Experimental Setup and Results

### A. Dataset and Training Configuration

The experiments were conducted on the NEU-DET industrial defect dataset, which contains six defect categories:

```text
crazing, inclusion, patches, pitted_surface, rolled-in_scale, scratches
```

All pruning strategies used the same dataset configuration and evaluation protocol. The input image size was 640. The baseline YOLOv8n model was trained for 100 epochs, and each pruned model was fine-tuned for 50 epochs after compatible weight transfer.

**Table II. Dataset Summary**

| Item | Value |
|---|---|
| Dataset | NEU-DET |
| Number of classes | 6 |
| Classes | crazing, inclusion, patches, pitted_surface, rolled-in_scale, scratches |
| Input image size | 640 |
| Train/validation/test split | TBD: fill from final dataset script or YAML |
| Evaluation metrics | mAP@0.5, mAP@0.5:0.95, parameters, GFLOPs |

> TODO: Before submission, fill the exact train/validation/test split and image/instance counts from the dataset preparation record.

### B. Baseline Result

The YOLOv8n baseline achieved 0.759 mAP@0.5 and 0.447 mAP@0.5:0.95. Under the unified model-summary procedure, the baseline contained 3,012,018 parameters and 8.2 GFLOPs. This baseline was used as the reference for all pruning experiments.

### C. Pruning Ablation

The entropy-guided strategy was compared with two control strategies:

1. Random pruning: three different branches were removed in separate runs, and the mean and sample standard deviation were reported.
2. L1-norm pruning: the branch with the smallest raw L1 sum in the corresponding receiving convolution weight slice was selected.

**Table III. Pruning Strategy Ablation**

| Pruning Strategy | Branches Pruned | mAP@0.5 | ΔmAP@0.5 | mAP@0.5:0.95 | Parameters | GFLOPs |
|---|---|---:|---:|---:|---:|---:|
| Baseline YOLOv8n | 0 | 0.759 | 0.000 | 0.447 | 3,012,018 | 8.2 |
| Random Pruning, mean of 3 runs | 1 | 0.7653 ± 0.0021 | +0.0063 | 0.4410 ± 0.0026 | 2,983,346 | 8.1 |
| L1-Norm Pruning | L4 to C14 | 0.763 | +0.004 | 0.438 | 3,007,922 | 8.1 |
| Entropy-Guided Pruning | L6 to C11 | 0.765 | +0.006 | 0.440 | 2,995,634 | 8.1 |

The random-pruning runs are shown in Table IV.

**Table IV. Random-Pruning Runs**

| Run | Branch Removed | mAP@0.5 | mAP@0.5:0.95 | Parameters |
|---|---|---:|---:|---:|
| Run 1 | L9 to C20 | 0.767 | 0.442 | 2,946,482 |
| Run 2 | L4 to C14 | 0.763 | 0.438 | 3,007,922 |
| Run 3 | L12 to C17 | 0.766 | 0.443 | 2,995,634 |

[Figure placeholder: Fig. 4. Bar chart comparing mAP@0.5 and mAP@0.5:0.95 among baseline, random pruning, L1-norm pruning, and entropy-guided pruning. Use error bars for the random-pruning mean.]

### D. Result Interpretation

All pruned variants maintained mAP@0.5 close to the baseline under the evaluated setting. The entropy-guided model achieved 0.765 mAP@0.5, which is slightly higher than the baseline value of 0.759. However, its mAP@0.5:0.95 decreased from 0.447 to 0.440, indicating a small reduction under the stricter localization metric.

The random-pruning baseline achieved an average mAP@0.5 of 0.7653, with a sample standard deviation of 0.0021. This result is comparable to the entropy-guided result. Therefore, the current experiment supports the feasibility and interpretability of entropy-guided branch selection, but it does not provide strong evidence that entropy-guided pruning is more accurate than random pruning under the current pruning budget.

The L1-norm strategy selected the L4-to-C14 branch, which coincided with the topology of Random Run 2. Its trained checkpoint and validation result were reused because the architecture, initialization, seed, and fine-tuning configuration were identical. This reuse avoids redundant training but should be explicitly noted in the final paper.

The GFLOPs values are rounded to one decimal place by the model-summary tool. Therefore, the apparent change from 8.2 to 8.1 GFLOPs should be interpreted cautiously rather than as a large computational reduction.

---

## V. Discussion

### A. What the Stage-I Results Support

The Stage-I results support three bounded conclusions.

First, a selected FPN skip branch can be removed from YOLOv8n while maintaining mAP@0.5 close to the baseline after fine-tuning. This suggests that the evaluated FPN topology contains some tolerance to branch-level simplification.

Second, activation entropy provides an interpretable way to inspect branch feature distributions. Even though the current accuracy advantage over random pruning is not established, the entropy ranking helps convert branch selection from manual inspection into a measurable procedure.

Third, the pruned model can serve as a stable source for golden data export. The selected 3×3 convolution has fixed tensor dimensions and Q8.8 reference files, enabling the next-stage HLS implementation to be evaluated through deterministic input/output comparison.

### B. What the Stage-I Results Do Not Prove

The current evidence does not prove that entropy-guided pruning is statistically superior to random pruning. The entropy-guided mAP@0.5 value is 0.765, while the three-run random-pruning mean is 0.7653. The difference is smaller than the random-pruning sample standard deviation. Therefore, the final manuscript should avoid claims such as “entropy pruning significantly outperforms random pruning.”

The current evidence also does not prove full-system hardware acceleration. The exported golden data only prepares the software reference for a raw 3×3 convolution operator. Actual acceleration, latency, initiation interval, LUT/FF/DSP/BRAM utilization, and C/RTL co-simulation results must be obtained in the next HLS stage.

### C. Implications for the Next HLS Stage

The next stage should implement the selected 3×3 convolution operator using HLS C/C++ with fixed-point arithmetic, line buffering, window buffering, and pipelining. The correctness criterion should be:

$$
\mathrm{MSE}(Y_{\mathrm{HLS}}, Y_{\mathrm{golden}}) \leq 10^{-6},
$$

where \(Y_{\mathrm{golden}}\) is the quantized output stored in `golden_output.txt`. This comparison should not be confused with the float-to-Q8.8 quantization error measured during golden data export.

[Figure placeholder: Fig. 5. Planned Stage-II HLS verification flow. Show golden_input.txt and weights.txt feeding HLS C simulation, HLS output compared with golden_output.txt, followed by C synthesis and C/RTL co-simulation.]

---

## VI. Conclusion

This paper presented a Stage-I experimental study on entropy-guided FPN branch pruning for YOLOv8n-based industrial defect detection. The method captured intermediate FPN/PAN branch activations, computed histogram-based spatial entropy scores, and selected the Layer-6-to-Concat-11 skip branch for pruning. After compatible weight transfer and 50 epochs of fine-tuning, the entropy-pruned model achieved 0.765 mAP@0.5 and 0.440 mAP@0.5:0.95, while reducing the parameter count from 3,012,018 to 2,995,634 under the unified model-summary procedure. Random pruning achieved a comparable mean mAP@0.5 of 0.7653, so the current result should be interpreted as evidence of feasibility and interpretability rather than clear accuracy superiority.

The Stage-I experiment also exported Q8.8 golden input, output, and weight files for a raw 3×3 convolution operator in the fine-tuned entropy-pruned model. These files establish the software reference required for the subsequent HLS streaming-convolution implementation. Future work will focus on fixed-point HLS design, line-buffer and window-buffer data reuse, pipeline optimization, and resource/latency evaluation on the target FPGA platform.

---

## Acknowledgment

TODO: Add funding, lab, supervisor, or institutional acknowledgments if required by the target conference.

---

## References

> Do not leave these as placeholders in the final submission. Replace each item with the complete citation in the required conference format.

[1] TODO: Ultralytics YOLOv8 official reference or documentation citation.

[2] TODO: Original Feature Pyramid Network paper citation.

[3] TODO: PANet or YOLO neck-related feature-fusion citation.

[4] TODO: NEU-DET dataset citation.

[5] TODO: Network pruning survey citation.

[6] TODO: L1-norm or weight-magnitude pruning citation.

[7] TODO: FPGA-based CNN acceleration / HLS streaming architecture citation.

[8] TODO: Line buffer / window buffer CNN accelerator citation.

---

## Appendix A. Evidence Files Used in This Draft

| Evidence | Path |
|---|---|
| Stage-I process summary | `10_论文写作/阶段一实验全流程整理.md` |
| Pruning ablation table | `08_results/stage1_Table2_pruning_ablation.md` |
| Entropy ranking | `07_experiments/stage1_algorithm_baseline_pruning/A2_entropy_pruning/all_concat_branch_entropy.txt` |
| Entropy-pruned YAML | `07_experiments/stage1_algorithm_baseline_pruning/A2_entropy_pruning/yolov8n_entropy_pruned.yaml` |
| Entropy build report | `07_experiments/stage1_algorithm_baseline_pruning/A2_entropy_pruning/entropy_pruned_build_report.txt` |
| Random-pruning summary | `07_experiments/stage1_algorithm_baseline_pruning/A3_random_pruning/A3_random_summary.txt` |
| L1 pruning record | `07_experiments/stage1_algorithm_baseline_pruning/A4_l1_pruning/A4_l1_result_record.txt` |
| Model complexity report | `07_experiments/stage1_algorithm_baseline_pruning/model_complexity_report.txt` |
| FPN topology figure | `09_论文图片/Figure2_FPN_Topology_Before_After.svg` |
| Golden export completion record | `07_experiments/stage1_algorithm_baseline_pruning/B1_golden_export/B1_completion_record.txt` |

