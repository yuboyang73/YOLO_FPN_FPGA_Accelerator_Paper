#include "conv3x3_core.h"

#include <cmath>
#include <cstddef>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>

static const std::string GOLDEN_DIR =
    "D:/.YOLO_FPN_FPGA_Accelerator_Paper/07_experiments/"
    "stage1_algorithm_baseline_pruning/B1_golden_export/";

static bool read_values(const std::string &path,
                        data_t *buffer,
                        std::size_t count) {
    std::cout << "[TB] Opening: " << path << std::endl;
    std::ifstream file(path.c_str(), std::ios::in);
    if (!file.is_open()) {
        std::cerr << "[ERROR] Cannot open: " << path << std::endl;
        return false;
    }

    for (std::size_t i = 0; i < count; ++i) {
        double value = 0.0;
        if (!(file >> value)) {
            std::cerr << "[ERROR] Not enough values in: " << path
                      << " at index " << i << std::endl;
            return false;
        }
        buffer[i] = data_t(value);
    }
    std::cout << "[TB] Read " << count << " values successfully." << std::endl;
    return true;
}

int main() {
    static data_t input[IN_CHANNELS][IMAGE_HEIGHT][IMAGE_WIDTH];
    static data_t weights[OUT_CHANNELS][IN_CHANNELS][KERNEL_SIZE][KERNEL_SIZE];
    static data_t output[OUT_CHANNELS][IMAGE_HEIGHT][IMAGE_WIDTH];
    static data_t golden[OUT_CHANNELS][IMAGE_HEIGHT][IMAGE_WIDTH];

    const std::size_t input_count =
        IN_CHANNELS * IMAGE_HEIGHT * IMAGE_WIDTH;
    const std::size_t weight_count =
        OUT_CHANNELS * IN_CHANNELS * KERNEL_SIZE * KERNEL_SIZE;
    const std::size_t output_count =
        OUT_CHANNELS * IMAGE_HEIGHT * IMAGE_WIDTH;

    const std::string input_path = GOLDEN_DIR + "golden_input.txt";
    const std::string weights_path = GOLDEN_DIR + "weights.txt";
    const std::string output_path = GOLDEN_DIR + "golden_output.txt";

    std::cout << "[TB] Golden data directory: " << GOLDEN_DIR << std::endl;

    if (!read_values(input_path,
                     &input[0][0][0], input_count) ||
        !read_values(weights_path,
                     &weights[0][0][0][0], weight_count) ||
        !read_values(output_path,
                     &golden[0][0][0], output_count)) {
        return 1;
    }

    std::cout << "[TB] Starting conv3x3_core..." << std::endl;
    conv3x3_core(input, weights, output);
    std::cout << "[TB] conv3x3_core returned." << std::endl;

    double squared_error = 0.0;
    double max_error = 0.0;
    for (std::size_t i = 0; i < output_count; ++i) {
        const double actual = (&output[0][0][0])[i].to_double();
        const double expected = (&golden[0][0][0])[i].to_double();
        const double error = actual - expected;
        squared_error += error * error;
        if (std::fabs(error) > max_error) {
            max_error = std::fabs(error);
        }
    }

    const double mse = squared_error / static_cast<double>(output_count);
    std::cout << std::setprecision(12)
              << "MSE: " << mse << std::endl
              << "Max absolute error: " << max_error << std::endl;

    if (mse <= 1.0e-6) {
        std::cout << "[PASS] C Simulation matches golden_output.txt"
                  << std::endl;
        return 0;
    }

    std::cout << "[FAIL] MSE exceeds 1e-6" << std::endl;
    return 1;
}
