#include "streaming_frontend.h"

#include <cmath>
#include <cstddef>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>

static const char *GOLDEN_DIR =
    "D:/.YOLO_FPN_FPGA_Accelerator_Paper/07_experiments/"
    "stage1_algorithm_baseline_pruning/B1_golden_export/";

static bool read_values(const char *path, data_t *buffer,
                        std::size_t count) {
    std::ifstream file(path, std::ios::in);
    if (!file.is_open()) {
        std::cerr << "[ERROR] Cannot open: " << path << std::endl;
        return false;
    }

    for (std::size_t i = 0; i < count; ++i) {
        double value = 0.0;
        if (!(file >> value)) {
            std::cerr << "[ERROR] Not enough values in " << path
                      << " at index " << i << std::endl;
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
    static data_t output[OUTPUT_CHANNELS][IMAGE_HEIGHT][IMAGE_WIDTH];

    const std::size_t input_count =
        static_cast<std::size_t>(INPUT_CHANNELS) *
        IMAGE_HEIGHT * IMAGE_WIDTH;
    const std::size_t weight_count =
        static_cast<std::size_t>(OUTPUT_CHANNELS) *
        INPUT_CHANNELS * KERNEL_SIZE * KERNEL_SIZE;
    const std::size_t output_count =
        static_cast<std::size_t>(OUTPUT_CHANNELS) *
        IMAGE_HEIGHT * IMAGE_WIDTH;

    if (!read_values(std::string(GOLDEN_DIR).append("golden_input.txt").c_str(),
                     &input[0][0][0], input_count) ||
        !read_values(std::string(GOLDEN_DIR).append("weights.txt").c_str(),
                     &weights[0][0][0][0], weight_count) ||
        !read_values(
            std::string(GOLDEN_DIR).append("golden_output.txt").c_str(),
            &golden_output[0][0][0], output_count)) {
        return 1;
    }

    std::cout << "[TB] Input values: " << input_count << std::endl;
    std::cout << "[TB] Weight values: " << weight_count << std::endl;
    std::cout << "[TB] Golden output values: " << output_count << std::endl;
    std::cout << "[TB] Starting streaming_frontend..." << std::endl;

    streaming_frontend(input, weights, output);

    double squared_error = 0.0;
    double max_error = 0.0;

    for (std::size_t i = 0; i < output_count; ++i) {
        const double actual = (&output[0][0][0])[i].to_double();
        const double expected = (&golden_output[0][0][0])[i].to_double();
        const double error = actual - expected;

        squared_error += error * error;
        if (std::fabs(error) > max_error) {
            max_error = std::fabs(error);
        }
    }

    const double mse = squared_error /
                       static_cast<double>(output_count);

    std::cout << std::setprecision(12)
              << "MSE: " << mse << std::endl
              << "Max absolute error: " << max_error << std::endl;

    if (mse <= 1.0e-6) {
        std::cout << "[PASS] Streaming Conv matches golden_output.txt"
                  << std::endl;
        return 0;
    }

    std::cout << "[FAIL] Streaming Conv MSE exceeds 1e-6"
              << std::endl;
    return 1;
}
