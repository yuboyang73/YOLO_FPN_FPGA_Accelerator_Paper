#include "streaming_frontend_axis.h"

void streaming_frontend_axis(
    hls::stream<axis_data_t> &input_stream,
    const data_t weights[OUTPUT_CHANNELS][INPUT_CHANNELS]
                      [KERNEL_SIZE][KERNEL_SIZE],
    hls::stream<axis_data_t> &output_stream) {
#pragma HLS INTERFACE axis port=input_stream
#pragma HLS INTERFACE axis port=output_stream
#pragma HLS INTERFACE ap_memory port=weights
#pragma HLS INTERFACE ap_ctrl_hs port=return
#pragma HLS INLINE off

    // Partial sums are kept only for one output-channel tile. The full input
    // and output feature maps are never materialized on chip.
    static accum_t partial[OUTPUT_PARALLEL][IMAGE_HEIGHT][IMAGE_WIDTH];
#pragma HLS ARRAY_PARTITION variable=partial complete dim=1

    for (int output_tile = 0; output_tile < OUTPUT_TILES; ++output_tile) {
        // Clear the partial sums for this output-channel tile.
        for (int output_channel = 0;
             output_channel < OUTPUT_PARALLEL; ++output_channel) {
            for (int row = 0; row < IMAGE_HEIGHT; ++row) {
                for (int col = 0; col < IMAGE_WIDTH; ++col) {
                    partial[output_channel][row][col] = 0;
                }
            }
        }

        // The stream protocol for one tile is NCHW: all pixels of input
        // channel 0, followed by channel 1, and so on. The complete frame is
        // replayed for every output tile, which replaces a large frame buffer.
        for (int input_channel = 0;
             input_channel < INPUT_CHANNELS; ++input_channel) {
            data_t line_buf[2][PADDED_WIDTH];
            data_t window[KERNEL_SIZE][KERNEL_SIZE];
            data_t weight_tile[OUTPUT_PARALLEL][KERNEL_SIZE][KERNEL_SIZE];
#pragma HLS ARRAY_PARTITION variable=line_buf complete dim=1
#pragma HLS ARRAY_PARTITION variable=window complete dim=0
#pragma HLS ARRAY_PARTITION variable=weight_tile complete dim=0

            for (int row = 0; row < 2; ++row) {
                for (int col = 0; col < PADDED_WIDTH; ++col) {
                    line_buf[row][col] = 0;
                }
            }

            for (int row = 0; row < KERNEL_SIZE; ++row) {
                for (int col = 0; col < KERNEL_SIZE; ++col) {
                    window[row][col] = 0;
                }
            }

            // Fetch one input-channel slice of weights before streaming its
            // feature plane. This avoids multi-port reads from the external
            // weight memory inside the II=1 window loop.
            for (int output_channel = 0;
                 output_channel < OUTPUT_PARALLEL; ++output_channel) {
                for (int kernel_row = 0;
                     kernel_row < KERNEL_SIZE; ++kernel_row) {
                    for (int kernel_col = 0;
                         kernel_col < KERNEL_SIZE; ++kernel_col) {
                        weight_tile[output_channel][kernel_row][kernel_col] =
                            weights[output_tile * OUTPUT_PARALLEL +
                                    output_channel][input_channel]
                                   [kernel_row][kernel_col];
                    }
                }
            }

            // Scan a zero-padded plane. At padded coordinate (row, col), the
            // current 3x3 window is complete when row and col are >= 2. Its
            // output coordinate is (row-2, col-2).
            for (int row = 0; row < IMAGE_HEIGHT + 2; ++row) {
                for (int col = 0; col < PADDED_WIDTH; ++col) {
#pragma HLS PIPELINE II=1
                    data_t pixel = 0;
                    if (row >= 1 && row <= IMAGE_HEIGHT &&
                        col >= 1 && col <= IMAGE_WIDTH) {
                        pixel = input_stream.read();
                    }

                    const data_t previous_row0 = line_buf[0][col];
                    const data_t previous_row1 = line_buf[1][col];

                    window[0][0] = window[0][1];
                    window[0][1] = window[0][2];
                    window[0][2] = previous_row0;
                    window[1][0] = window[1][1];
                    window[1][1] = window[1][2];
                    window[1][2] = previous_row1;
                    window[2][0] = window[2][1];
                    window[2][1] = window[2][2];
                    window[2][2] = pixel;

                    line_buf[0][col] = previous_row1;
                    line_buf[1][col] = pixel;

                    if (row >= 2 && col >= 2) {
                        const int output_row = row - 2;
                        const int output_col = col - 2;

                        for (int output_channel = 0;
                             output_channel < OUTPUT_PARALLEL;
                             ++output_channel) {
#pragma HLS UNROLL
                            accum_t window_sum = 0;
                            for (int kernel_row = 0;
                                 kernel_row < KERNEL_SIZE; ++kernel_row) {
                                for (int kernel_col = 0;
                                     kernel_col < KERNEL_SIZE; ++kernel_col) {
#pragma HLS UNROLL
                                    window_sum +=
                                        accum_t(window[kernel_row][kernel_col]) *
                                        accum_t(weight_tile[output_channel]
                                                   [kernel_row][kernel_col]);
                                }
                            }
                            partial[output_channel][output_row][output_col] +=
                                window_sum;
                        }
                    }
                }
            }
        }

        // Emit one completed output tile in OCHW order.
        for (int output_channel = 0;
             output_channel < OUTPUT_PARALLEL; ++output_channel) {
            for (int row = 0; row < IMAGE_HEIGHT; ++row) {
                for (int col = 0; col < IMAGE_WIDTH; ++col) {
                    output_stream.write(
                        axis_data_t(partial[output_channel][row][col]));
                }
            }
        }
    }
}
