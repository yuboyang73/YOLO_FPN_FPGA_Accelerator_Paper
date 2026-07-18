#ifndef CONV3X3_CORE_H
#define CONV3X3_CORE_H

#include <ap_fixed.h>

static const int IN_CHANNELS = 64;
static const int OUT_CHANNELS = 64;
static const int IMAGE_HEIGHT = 40;
static const int IMAGE_WIDTH = 40;
static const int KERNEL_SIZE = 3;

typedef ap_fixed<16, 8> data_t;

void conv3x3_core(
    const data_t input[IN_CHANNELS][IMAGE_HEIGHT][IMAGE_WIDTH],
    const data_t weights[OUT_CHANNELS][IN_CHANNELS][KERNEL_SIZE][KERNEL_SIZE],
    data_t output[OUT_CHANNELS][IMAGE_HEIGHT][IMAGE_WIDTH]);

#endif
