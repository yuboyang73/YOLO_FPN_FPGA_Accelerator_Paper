#ifndef STREAMING_FRONTEND_H
#define STREAMING_FRONTEND_H

#include <ap_fixed.h>

static const int INPUT_CHANNELS = 64;
static const int OUTPUT_CHANNELS = 64;
static const int IMAGE_HEIGHT = 40;
static const int IMAGE_WIDTH = 40;
static const int KERNEL_SIZE = 3;
static const int BUFFER_ROWS = KERNEL_SIZE - 1;
static const int VALID_ROWS = IMAGE_HEIGHT - KERNEL_SIZE + 1;
static const int VALID_COLS = IMAGE_WIDTH - KERNEL_SIZE + 1;
static const int VALID_WINDOWS = VALID_ROWS * VALID_COLS;

// Q8.8 data with convergent rounding and saturation. AP_RND_CONV
// matches the round-to-nearest-even behavior used by the Golden export.
typedef ap_fixed<16, 8, AP_RND_CONV, AP_SAT> data_t;

// Wide accumulator: 24 integer bits and 16 fractional bits. This is
// sufficient for the sum of 64 x 3 x 3 Q8.8 products.
typedef ap_fixed<40, 24, AP_RND_CONV, AP_SAT> accum_t;

void streaming_frontend(
    const data_t input[INPUT_CHANNELS][IMAGE_HEIGHT][IMAGE_WIDTH],
    const data_t weights[OUTPUT_CHANNELS][INPUT_CHANNELS]
                      [KERNEL_SIZE][KERNEL_SIZE],
    data_t output[OUTPUT_CHANNELS][IMAGE_HEIGHT][IMAGE_WIDTH]);

#endif
