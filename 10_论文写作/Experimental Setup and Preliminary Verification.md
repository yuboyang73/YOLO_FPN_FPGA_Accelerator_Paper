# Experimental Setup and Preliminary Verification

## Hardware and Software Environment

The preliminary experiments were conducted to establish a reproducible software-to-hardware verification flow for the proposed FPGA-oriented feature pyramid acceleration study. The software environment was configured with Anaconda and a dedicated `yolo_fpga` environment. The installed PyTorch runtime was verified as `torch 2.12.1+cu126`, with CUDA support enabled and one CUDA-capable device detected. This confirms that the local deep learning environment can execute GPU-backed model validation and dataset preparation tasks.

The hardware synthesis environment was based on Xilinx Vitis HLS 2022.2 targeting the Zynq-7000 device `xc7z020-clg400-1`. The HLS toolchain was verified through a matrix multiplication design, including C simulation, C synthesis, and C/RTL co-simulation. The C/RTL co-simulation was executed using Vivado XSIM, and the generated Verilog RTL passed the reference testbench.

## Dataset and YOLO Runtime Sanity Check

The NEU-DET dataset was prepared for YOLO-format experiments as an early sanity check for the object detection pipeline. The archived raw dataset contains 1,800 images and 1,800 annotations. The converted YOLO dataset contains 1,260 training images, 360 validation images, and 180 test images, with matching label counts for each split. A minimal YOLO inference run was also recorded using `bus.jpg`, and validation artifacts such as precision-recall curves and confusion matrices were generated.

These results indicate that the data preparation and detection runtime are operational. However, the Stage 0 evidence is used only as an environment and workflow validation step; quantitative detector accuracy and FPN pruning results are reserved for the later baseline and ablation stages.

## C++ and Python Convolution Consistency

To verify numerical consistency between a software reference and a C++ implementation, a 3x3 convolution was implemented using standard nested loops and array indexing. The Python reference generated the same input feature map, convolution kernel, bias term, and output tensor. The C++ output was compared against the Python reference output element by element.

For the 5x5 input feature map and 3x3 kernel used in this preliminary test, both implementations produced a 3x3 output tensor. The measured mean squared error was `0`, and the maximum absolute error was `0`, satisfying the Stage 0 acceptance criterion of `MSE < 1e-15`. This result establishes a basic numerical validation workflow for later C++ and HLS operator development.

## HLS Matrix Multiplication Verification

A 4x4 matrix multiplication kernel was synthesized and verified using Vitis HLS. The testbench multiplied an input matrix by an identity matrix and checked whether the output matched the original input matrix. The C simulation passed, indicating functional correctness at the C++ behavior level.

The design was then synthesized to RTL with the top function `matrix_mult`. The synthesis report showed an estimated clock period of `6.912 ns` under a `10.00 ns` target clock. The top-level latency was estimated as `69` cycles, with an interval of `70` cycles. The synthesized design used `0` BRAM_18K, `6` DSP blocks, `869` flip-flops, and `793` LUTs. The loop-level report indicated that the `Row_Col` loop was pipelined, with an achieved initiation interval of `4`.

C/RTL co-simulation was performed for the generated Verilog implementation. The reported co-simulation status was `Pass`, with a measured Verilog latency of `620` cycles. This result confirms that the generated RTL implementation preserves the behavior of the C++ model for the matrix multiplication sanity test.

## Relevance to the Proposed Accelerator

The Stage 0 experiments do not yet evaluate the final FPN acceleration architecture. Instead, they establish the minimum reproducible path required for the subsequent stages: GPU-backed YOLO experimentation, C++ numerical verification, and HLS-based RTL generation and co-simulation. This workflow will be reused when migrating the target FPN fusion and 3x3 convolution operator from algorithm-level validation to streaming hardware implementation.

## Evidence Summary

| Item | Evidence | Status |
| --- | --- | --- |
| PyTorch/CUDA environment | `torch 2.12.1+cu126`, CUDA available, one CUDA device detected | Verified |
| YOLO dataset preparation | 1,260 train, 360 validation, and 180 test images with matching labels | Verified |
| Minimal YOLO runtime | `runs/detect/predict/bus.jpg` and validation curves generated | Verified |
| C++ vs. Python 3x3 convolution | `MSE = 0`, `MaxAbsError = 0` | Verified |
| HLS C synthesis | Vitis HLS 2022.2 report targeting `xc7z020-clg400-1` | Verified |
| HLS C/RTL co-simulation | Verilog co-simulation status `Pass` | Verified |

## Limitations

This preliminary stage verifies toolchain availability and basic functional consistency only. It does not yet provide final YOLO baseline accuracy, entropy-guided FPN pruning results, end-to-end accelerator throughput, or energy-efficiency measurements. These results should be reported in the later experimental sections after the corresponding algorithmic and hardware optimization stages are completed.0
