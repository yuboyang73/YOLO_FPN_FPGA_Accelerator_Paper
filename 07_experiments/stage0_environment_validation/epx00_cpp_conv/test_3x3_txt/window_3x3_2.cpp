#include <fstream>
#include <iostream>
using namespace std;

// data_t 用来模拟硬件设计中的像素数据类型。
// 现在先用 int，后续做 HLS 时可以替换成 ap_int、ap_uint 或 fixed-point 类型。
typedef int data_t;

const int IMG_H = 5;// 本例用 5x5 小图像模拟输入特征图/像素流。
const int IMG_W = 5;
const int K = 3;// K = 3 表示卷积窗口和卷积核大小都是 3x3。

// 将 3x3 窗口整体向左移动一列，并把新的右侧列写入窗口。
// 例如：
// 原窗口: [a b c]    新列: [x]    移动后: [b c x]
//         [d e f]          [y]            [e f y]
//         [g h i]          [z]            [h i z]
// 这个函数模拟硬件卷积中 window buffer 的横向滑动过程。
void shift_window_3x3(data_t window[K][K], data_t new_col[K]) {
    for (int r = 0; r < K; r++) {
        // 每一行的第 1 列丢弃，第 2、3 列依次左移。
        window[r][0] = window[r][1];
        window[r][1] = window[r][2];

        // 最右侧补入新的像素列。
        window[r][2] = new_col[r];
    }
}

// 对当前 3x3 窗口执行一次卷积乘加运算。
// 数学形式：
// y = sum(window[r][c] * kernel[r][c]), r,c = 0..2
// 这里没有做 padding、stride、bias、激活函数，只模拟最核心的 3x3 MAC。
int conv_3x3(data_t window[K][K], data_t kernel[K][K]) {
    int sum = 0;
    for (int r = 0; r < K; r++) {
        for (int c = 0; c < K; c++) {
            // 当前窗口像素与卷积核权重逐点相乘，然后累加。
            sum += window[r][c] * kernel[r][c];
        }
    }
    return sum;
}

// 为每一行扫描的起始位置装载第一个 3x3 窗口。
// top_row 表示窗口左上角所在的图像行号。
// 由于每一行扫描开始时窗口列号为 0，所以这里读取 image[top_row..top_row+2][0..2]。
void load_first_window(data_t image[IMG_H][IMG_W], data_t window[K][K], int top_row) {
    for (int r = 0; r < K; r++) {
        for (int c = 0; c < K; c++) {
            window[r][c] = image[top_row + r][c];
        }
    }
}

// 打印当前 3x3 窗口内容，便于观察左移之后窗口内部数据是否正确。
void print_window(data_t window[K][K]) {
    for (int r = 0; r < K; r++) {
        for (int c = 0; c < K; c++) {
            cout << window[r][c] << " ";
        }
        cout << endl;
    }
}

// 从 txt 文件读取像素流。
// pixel_stream.txt 中的数字按行优先顺序排列：
// 第 1 行对应图像第 0 行，第 2 行对应图像第 1 行，以此类推。
// 在真实硬件中，这部分可以理解为从 AXI-Stream 或外部存储连续读入像素。
bool read_pixel_stream(const char* file_name, data_t image[IMG_H][IMG_W]) {
    ifstream fin(file_name);
    if (!fin) {
        cout << "Cannot open pixel stream file: " << file_name << endl;
        return false;
    }

    for (int r = 0; r < IMG_H; r++) {
        for (int c = 0; c < IMG_W; c++) {
            // 按顺序读入每个像素，并放入二维图像缓存，方便软件仿真观察。
            if (!(fin >> image[r][c])) {
                cout << "Pixel stream data is not enough." << endl;
                return false;
            }
        }
    }

    return true;
}

int main() {
    // image 保存从 txt 中读入的 5x5 像素数据。
    // window 是当前参与卷积计算的 3x3 滑动窗口。
    data_t image[IMG_H][IMG_W];
    data_t window[K][K];

    // 示例卷积核：Sobel 横向梯度核，用于检测左右方向的像素变化。
    // 这里只是任意举例，后续可以替换成普通 CNN 卷积层中的权重。
    data_t kernel[K][K] = {
        {1, 0, -1},
        {2, 0, -2},
        {1, 0, -1}
    };

    // 从当前运行目录读取像素流文件。
    // Code Runner 当前配置会先 cd 到 cpp 所在目录，所以这里直接写文件名即可。
    if (!read_pixel_stream("pixel_stream.txt", image)) {
        return 1;
    }

    cout << "Kernel:" << endl;
    print_window(kernel);
    cout << "================" << endl;

    // 外层循环控制窗口的纵向位置。
    // 对 5x5 图像做 3x3 valid convolution 时，top 可取 0、1、2，共 3 行输出。
    for (int top = 0; top <= IMG_H - K; top++) {
        // 每换到新的一行输出，先装载该行最左侧的 3x3 窗口。
        load_first_window(image, window, top);

        cout << "Window at row " << top << ", col 0:" << endl;
        print_window(window);
        cout << "Conv result = " << conv_3x3(window, kernel) << endl;
        cout << "--------" << endl;

        // 内层循环控制窗口的横向滑动。
        // col 表示要补入窗口最右侧的新图像列号。
        // 对 5x5 图像和 3x3 窗口来说，col = 3、4，分别得到输出列 1、2。
        for (int col = K; col < IMG_W; col++) {
            data_t new_col[K];

            // 从图像中取出当前窗口需要新增的最右侧一列。
            // 例如 top=0,col=3 时，新列为 image[0][3], image[1][3], image[2][3]。
            for (int r = 0; r < K; r++) {
                new_col[r] = image[top + r][col];
            }

            // 窗口左移一列，并把 new_col 填入窗口最右侧。
            shift_window_3x3(window, new_col);

            cout << "After left shift, window at row " << top
                << ", col " << col - K + 1 << ":" << endl;
            print_window(window);

            // 对移动后的窗口立即执行一次 3x3 卷积。
            cout << "Conv result = " << conv_3x3(window, kernel) << endl;
            cout << "--------" << endl;
        }
    }

    return 0;
}
