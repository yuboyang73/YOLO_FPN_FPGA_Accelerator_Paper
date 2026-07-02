#include <iostream>
#include <fstream>
#include <iomanip>
#include <cstdlib>

using namespace std;

// =========================
// Basic configuration
// =========================
const int H = 5;
const int W = 5;
const int K = 3;
const int STRIDE = 1;
const int PADDING = 0;

const int OH = (H + 2 * PADDING - K) / STRIDE + 1;
const int OW = (W + 2 * PADDING - K) / STRIDE + 1;

// =========================
// Load 5x5 input matrix
// =========================
void load_input(const char* filename, double x[H][W]) {
    ifstream fin(filename);

    if (!fin) {
        cerr << "Error: cannot open " << filename << endl;
        exit(1);
    }

    for (int i = 0; i < H; i++) {
        for (int j = 0; j < W; j++) {
            fin >> x[i][j];
        }
    }

    fin.close();
}

// =========================
// Load 3x3 weight matrix
// =========================
void load_weight(const char* filename, double w[K][K]) {
    ifstream fin(filename);

    if (!fin) {
        cerr << "Error: cannot open " << filename << endl;
        exit(1);
    }

    for (int i = 0; i < K; i++) {
        for (int j = 0; j < K; j++) {
            fin >> w[i][j];
        }
    }

    fin.close();
}

// =========================
// Load bias
// =========================
double load_bias(const char* filename) {
    ifstream fin(filename);

    if (!fin) {
        cerr << "Error: cannot open " << filename << endl;
        exit(1);
    }

    double bias;
    fin >> bias;

    fin.close();
    return bias;
}

// =========================
// 3x3 convolution
// padding = 0 in this experiment
// =========================
void conv3x3(
    double x[H][W],
    double w[K][K],
    double bias,
    double y[OH][OW]
) {
    for (int oh = 0; oh < OH; oh++) {
        for (int ow = 0; ow < OW; ow++) {
            double acc = bias;

            for (int kh = 0; kh < K; kh++) {
                for (int kw = 0; kw < K; kw++) {
                    int ih = oh * STRIDE + kh;
                    int iw = ow * STRIDE + kw;

                    acc += x[ih][iw] * w[kh][kw];
                }
            }

            y[oh][ow] = acc;
        }
    }
}

// =========================
// Main function
// =========================
int main() {
    double input[H][W];
    double weight[K][K];
    double output[OH][OW];

    load_input("input.txt", input);
    load_weight("weight.txt", weight);
    double bias = load_bias("bias.txt");

    conv3x3(input, weight, bias, output);

    ofstream fout("cpp_output.txt");

    if (!fout) {
        cerr << "Error: cannot write cpp_output.txt" << endl;
        return 1;
    }

    fout << setprecision(17);

    cout << "========== C++ Output ==========" << endl;
    cout << "Output shape: " << OH << " x " << OW << endl;
    cout << endl;

    for (int i = 0; i < OH; i++) {
        for (int j = 0; j < OW; j++) {
            printf("cpp_output[%d][%d] = %.17g\n", i, j, output[i][j]);

            fout << output[i][j];
            if (j != OW - 1) {
                fout << " ";
            }
        }
        fout << "\n";
    }

    fout.close();

    cout << "================================" << endl;
    cout << "File generated: cpp_output.txt" << endl;

    return 0;
}