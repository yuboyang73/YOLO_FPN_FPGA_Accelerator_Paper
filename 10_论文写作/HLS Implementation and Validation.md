# HLS Implementation and Validation

## 4.4 Experimental Setup

The hardware-oriented experiments were conducted using Vitis HLS 2022.2 with an XC7Z020-CLG400-1 target device. The synthesis clock constraint was set to 5 ns, corresponding to a nominal operating frequency of 200 MHz. The evaluated operator processes a 64-channel feature map with a spatial size of 40 x 40 using 3 x 3 kernels, unit stride, and zero padding. Feature-map values and weights were represented using signed Q8.8 fixed-point values implemented with `ap_fixed<16,8>`.

The exported tensors from the algorithmic stage were used as the reference data. The testbench loaded 102,400 input values, 36,864 weight values, and 102,400 golden output values. A wider fixed-point accumulator was used to reduce intermediate overflow and preserve the reference quantization behavior.

## 4.4.1 Functional Verification

The Line Buffer row-shifting logic, the 3 x 3 Window Buffer sliding behavior, and the three-state controller were first validated independently. The complete fixed-point convolution frontend and the folded AXI4-Stream top function were then compared with the exported golden output.

| Test | Input values | Weight values | Golden output values | MSE | Maximum absolute error |
|---|---:|---:|---:|---:|---:|
| Streaming convolution frontend | 102,400 | 36,864 | 102,400 | 0 | 0 |
| Folded AXI4-Stream frontend | 102,400 per replayed frame | 36,864 | 102,400 | 0 | 0 |

The folded AXI testbench replays the input frame four times because the output channels are processed as four tiles of 16 channels. The C-level result is numerically identical to the golden reference for the evaluated configuration. This result establishes functional equivalence, but it does not by itself establish cycle-level throughput or timing closure.

## 4.4.2 Folded AXI4-Stream Line/Window Dataflow

The redesigned AXI4-Stream top function is `streaming_frontend_axis`. It connects 16-bit `input_stream_TDATA` and `output_stream_TDATA` ports with the corresponding `TVALID` and `TREADY` handshake signals. The weight tensor remains connected through an `ap_memory` interface.

The datapath uses a two-row Line Buffer and a 3 x 3 Window Buffer while scanning each zero-padded input plane. Partial sums are retained on chip. To limit the number of parallel multipliers, the 64 output channels are folded into four tiles, each containing 16 output channels. After one tile is completed, the input frame is replayed for the next tile. This is a genuine streaming spatial datapath, but it is a folded architecture rather than a single-pass all-output-channel pipeline.

## 4.4.3 HLS Synthesis Results

Table 3 summarizes the current folded AXI4-Stream synthesis result.

| Metric | Estimate |
|---|---:|
| Target clock period | 5.00 ns |
| Estimated clock period | 6.138 ns |
| Estimated maximum frequency | 162.91 MHz |
| Latency | 1,392,966 cycles |
| Interval | 1,392,967 cycles |
| BRAM_18K | 80 / 280 |
| DSP | 144 / 220 |
| FF | 54,501 / 106,400 |
| LUT | 38,432 / 53,200 |

The folded architecture reduces the estimated BRAM usage to 80 blocks because it does not allocate full-frame input and output staging buffers. However, the estimated clock period is 6.138 ns, which does not meet the 5 ns constraint. The result should therefore be treated as an intermediate architecture result rather than a timing-closed implementation.

## 4.4.4 Pipeline and Initiation-Interval Analysis

The source contains explicit pipeline directives for the padded scan, line-buffer/window update, partial-sum update, and output-emission loops. The synthesis reports show an achieved II of 2 for the reported pipelined loop groups, with a target II of 1. The current evidence therefore does not support a claim of II=1 or line-rate operation.

The remaining bottleneck is the scheduling and dependency structure of the parallel partial-sum update together with the associated memory accesses and adder tree. Further work should separate accumulation stages, balance the reduction tree, and refine array partitioning and data types before claiming II=1.

## 4.4.5 C/RTL Co-simulation Status

C/RTL co-simulation was attempted with XSim after the folded redesign. Vitis HLS generated the C/RTL testbench and started Verilog simulation. The run did not complete within approximately five minutes and was stopped to avoid leaving the simulator running indefinitely. No valid co-simulation PASS/FAIL completion record was produced, so no C/RTL PASS claim is made.

A reduced-size C/RTL smoke-test configuration is required before repeating the full 64-channel experiment. The smoke test should preserve the same Line Buffer, Window Buffer, partial-sum, and AXI handshake structure while reducing the spatial and channel dimensions. After the smoke test completes, the full configuration should be rerun.

## 4.4.6 Reproducibility Record

The main implementation and evidence files are:

- `07_experiments/stage2_hls_streaming_accelerator/streaming_frontend_axis.cpp`
- `07_experiments/stage2_hls_streaming_accelerator/streaming_frontend_axis.h`
- `07_experiments/stage2_hls_streaming_accelerator/tb_streaming_frontend_axis.cpp`
- `07_experiments/stage2_hls_streaming_accelerator/stage2_streaming_frontend_axis_folded_synthesis_report.txt`
- `D:/.HLS/streaming_frontend_core/streaming_frontend_core/solution1/csim/report/streaming_frontend_axis_csim.log`
- `D:/.HLS/streaming_frontend_core/streaming_frontend_core/solution1/syn/report/streaming_frontend_axis_csynth.rpt`

The reported results are HLS estimates and C-level functional verification results. Board-level latency, throughput, power, post-place-and-route timing, and a completed C/RTL co-simulation were not established in this stage.
