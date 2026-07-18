#include "streaming_frontend_axis.h"

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>

static bool read_values(const char *path, data_t *buffer,
                        std::size_t count) {
    std::ifstream file(path);
    if (!file) {
        std::cerr << "[ERR] Cannot open: " << path << std::endl;
        return false;
    }

    for (std::size_t i = 0; i < count; ++i) {
        double value = 0.0;
        if (!(file >> value)) {
            std::cerr << "[ERR] Not enough values in: " << path << std::endl;
            return false;
        }
        buffer[i] = data_t(value);
    }
    return true;
}

int main() {
    static data_t input[INPUT_CHANNELS][IMAGE_HEIGHT][IMAGE_WIDTH];
    static data_t weights[OUTPUT_CHANNELS][INPUT_CHANNELS]
                         [KERNEL_SIZE][KERNEL_SIZE];
    static data_t golden_output[OUTPUT_CHANNELS][IMAGE_HEIGHT][IMAGE_WIDTH];

    const char *golden_dir =
        "D:/.YOLO_FPN_FPGA_Accelerator_Paper/07_experiments/"
        "stage1_algorithm_baseline_pruning/B1_golden_export/";

    const std::size_t input_count =
        static_cast<std::size_t>(INPUT_CHANNELS) * IMAGE_HEIGHT * IMAGE_WIDTH;
    const std::size_t weight_count =
        static_cast<std::size_t>(OUTPUT_CHANNELS) * INPUT_CHANNELS *
        KERNEL_SIZE * KERNEL_SIZE;
    const std::size_t output_count =
        static_cast<std::size_t>(OUTPUT_CHANNELS) * IMAGE_HEIGHT * IMAGE_WIDTH;

    const std::string input_path = std::string(golden_dir) +
        "golden_input.txt";
    const std::string weights_path = std::string(golden_dir) + "weights.txt";
    const std::string output_path = std::string(golden_dir) +
        "golden_output.txt";

    if (!read_values(input_path.c_str(), &input[0][0][0], input_count) ||
        !read_values(weights_path.c_str(), &weights[0][0][0][0],
                     weight_count) ||
        !read_values(output_path.c_str(), &golden_output[0][0][0],
                     output_count)) {
        return 1;
    }

    hls::stream<axis_data_t> input_stream;
    hls::stream<axis_data_t> output_stream;

    // The frame is replayed once for every output-channel tile.
    for (int output_tile = 0; output_tile < OUTPUT_TILES; ++output_tile) {
        for (int input_channel = 0;
             input_channel < INPUT_CHANNELS; ++input_channel) {
            for (int row = 0; row < IMAGE_HEIGHT; ++row) {
                for (int col = 0; col < IMAGE_WIDTH; ++col) {
                    input_stream.write(input[input_channel][row][col]);
                }
            }
        }
    }

    std::cout << "[TB] Starting folded AXI4-Stream frontend..." << std::endl;
    streaming_frontend_axis(input_stream, weights, output_stream);

    double squared_error = 0.0;
    double max_absolute_error = 0.0;

    for (int output_tile = 0; output_tile < OUTPUT_TILES; ++output_tile) {
        for (int output_channel = 0;
             output_channel < OUTPUT_PARALLEL; ++output_channel) {
            const int absolute_channel =
                output_tile * OUTPUT_PARALLEL + output_channel;
            for (int row = 0; row < IMAGE_HEIGHT; ++row) {
                for (int col = 0; col < IMAGE_WIDTH; ++col) {
                    if (output_stream.empty()) {
                        std::cerr << "[FAIL] Output stream ended early"
                                  << std::endl;
                        return 1;
                    }

                    const double actual = output_stream.read().to_double();
                    const double expected =
                        golden_output[absolute_channel][row][col].to_double();
                    const double error = actual - expected;
                    squared_error += error * error;
                    max_absolute_error =
                        std::max(max_absolute_error, std::fabs(error));
                }
            }
        }
    }

    const double mse = squared_error / static_cast<double>(output_count);
    std::cout << std::setprecision(12);
    std::cout << "MSE: " << mse << std::endl;
    std::cout << "Max absolute error: " << max_absolute_error << std::endl;

    if (!output_stream.empty()) {
        std::cerr << "[FAIL] Output stream contains extra values" << std::endl;
        return 1;
    }
    if (mse > 1e-6) {
        std::cerr << "[FAIL] MSE exceeds 1e-6" << std::endl;
        return 1;
    }

    std::cout << "[PASS] Folded AXI4-Stream frontend matches golden_output.txt"
              << std::endl;
    return 0;
}
