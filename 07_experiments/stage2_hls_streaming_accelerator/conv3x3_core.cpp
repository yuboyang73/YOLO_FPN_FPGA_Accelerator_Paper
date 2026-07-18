#include "conv3x3_core.h"

#include <cmath>

static long long round_to_even(double value) {
    const double lower = std::floor(value);
    const double fraction = value - lower;

    if (fraction < 0.5) {
        return static_cast<long long>(lower);
    }
    if (fraction > 0.5) {
        return static_cast<long long>(lower + 1.0);
    }

    const long long lower_integer = static_cast<long long>(lower);
    return (lower_integer % 2 == 0) ? lower_integer : lower_integer + 1;
}

void conv3x3_core(
    const data_t input[IN_CHANNELS][IMAGE_HEIGHT][IMAGE_WIDTH],
    const data_t weights[OUT_CHANNELS][IN_CHANNELS][KERNEL_SIZE][KERNEL_SIZE],
    data_t output[OUT_CHANNELS][IMAGE_HEIGHT][IMAGE_WIDTH]) {
#pragma HLS INTERFACE ap_memory port=input
#pragma HLS INTERFACE ap_memory port=weights
#pragma HLS INTERFACE ap_memory port=output
#pragma HLS INLINE off

    for (int oc = 0; oc < OUT_CHANNELS; ++oc) {
        for (int row = 0; row < IMAGE_HEIGHT; ++row) {
            for (int col = 0; col < IMAGE_WIDTH; ++col) {
                double accumulator = 0.0;

                for (int ic = 0; ic < IN_CHANNELS; ++ic) {
                    for (int kr = 0; kr < KERNEL_SIZE; ++kr) {
                        for (int kc = 0; kc < KERNEL_SIZE; ++kc) {
#pragma HLS LOOP_FLATTEN off
                            const int input_row = row + kr - 1;
                            const int input_col = col + kc - 1;

                            if (input_row >= 0 && input_row < IMAGE_HEIGHT &&
                                input_col >= 0 && input_col < IMAGE_WIDTH) {
                                accumulator +=
                                    input[ic][input_row][input_col].to_double() *
                                    weights[oc][ic][kr][kc].to_double();
                            }
                        }
                    }
                }

                // Q8.8 x Q8.8 produces Q16.16. Convert back to Q8.8
                // with symmetric nearest-integer rounding.
                long long scaled = round_to_even(accumulator * 256.0);
                if (scaled > 32767) {
                    scaled = 32767;
                } else if (scaled < -32768) {
                    scaled = -32768;
                }

                output[oc][row][col] = data_t(static_cast<double>(scaled) / 256.0);
            }
        }
    }
}
