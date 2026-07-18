#ifndef STREAMING_FRONTEND_AXIS_H
#define STREAMING_FRONTEND_AXIS_H

#include <hls_stream.h>

#include "streaming_frontend.h"

// One Q8.8 value is transferred per AXI4-Stream beat.
typedef data_t axis_data_t;

// The input frame is replayed once for each output-channel tile. Each tile
// computes OUTPUT_PARALLEL output channels in parallel. The replay is the
// channel-folding mechanism that avoids a full input-frame buffer.
static const int OUTPUT_PARALLEL = 16;
static const int OUTPUT_TILES = OUTPUT_CHANNELS / OUTPUT_PARALLEL;
static const int PADDED_WIDTH = IMAGE_WIDTH + 2;

void streaming_frontend_axis(
    hls::stream<axis_data_t> &input_stream,
    const data_t weights[OUTPUT_CHANNELS][INPUT_CHANNELS]
                      [KERNEL_SIZE][KERNEL_SIZE],
    hls::stream<axis_data_t> &output_stream);

#endif
