#include "streaming_frontend.h"

void streaming_frontend(
    const data_t input[INPUT_CHANNELS][IMAGE_HEIGHT][IMAGE_WIDTH],
    const data_t weights[OUTPUT_CHANNELS][INPUT_CHANNELS]
                      [KERNEL_SIZE][KERNEL_SIZE],
    data_t output[OUTPUT_CHANNELS][IMAGE_HEIGHT][IMAGE_WIDTH]) {
#pragma HLS INTERFACE ap_memory port=input
#pragma HLS INTERFACE ap_memory port=weights
#pragma HLS INTERFACE ap_memory port=output
#pragma HLS INLINE off

    // Do not materialize all valid windows in a large intermediate array.
    // The previous implementation used
    //   windows[64][1444][3][3]
    // which forced Vitis HLS to infer 1024 BRAM_18K blocks.  Instead, build
    // one 3x3 window on demand for each input channel and immediately feed it
    // to the MAC.  The accumulation order is intentionally kept identical to
    // the golden reference: output channel, row, column, input channel,
    // kernel row, kernel column.
    for (int output_channel = 0;
         output_channel < OUTPUT_CHANNELS; ++output_channel) {
        for (int output_row = 0;
             output_row < IMAGE_HEIGHT; ++output_row) {
            for (int output_col = 0;
                 output_col < IMAGE_WIDTH; ++output_col) {
                accum_t accumulator = 0;

                for (int input_channel = 0;
                     input_channel < INPUT_CHANNELS; ++input_channel) {
                    data_t window[KERNEL_SIZE][KERNEL_SIZE];
#pragma HLS ARRAY_PARTITION variable=window complete dim=0

                    for (int kernel_row = 0;
                         kernel_row < KERNEL_SIZE; ++kernel_row) {
                        for (int kernel_col = 0;
                             kernel_col < KERNEL_SIZE; ++kernel_col) {
                            const int input_row =
                                output_row + kernel_row - 1;
                            const int input_col =
                                output_col + kernel_col - 1;

                            if (input_row >= 0 &&
                                input_row < IMAGE_HEIGHT &&
                                input_col >= 0 &&
                                input_col < IMAGE_WIDTH) {
                                window[kernel_row][kernel_col] =
                                    input[input_channel][input_row][input_col];
                            } else {
                                window[kernel_row][kernel_col] = 0;
                            }
                        }
                    }

                    for (int kernel_row = 0;
                         kernel_row < KERNEL_SIZE; ++kernel_row) {
                        for (int kernel_col = 0;
                             kernel_col < KERNEL_SIZE; ++kernel_col) {
                            accumulator +=
                                accum_t(window[kernel_row][kernel_col]) *
                                accum_t(weights[output_channel]
                                           [input_channel]
                                           [kernel_row][kernel_col]);
                        }
                    }
                }

                output[output_channel][output_row][output_col] =
                    data_t(accumulator);
            }
        }
    }
}
