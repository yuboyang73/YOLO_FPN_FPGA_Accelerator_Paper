```cpp
$env:Path = "D:\msys64\ucrt64\bin;" + $env:Path
```

test.cpp文件中的"xxx.h"必须是完整的路径

**流程**

```cpp
C Simulation
    ↓
C Synthesis
    ↓
C/RTL Cosimulation
    ↓
Status: PASS这几步分别在做什么
```

```cpp
先证明 C++ 算法对
再证明 C++ 能变成硬件
再证明变出来的硬件也对
最后得到通过结论
```

```cpp
.h 文件：声明接口 / 定义公共参数
.cpp 文件：实现算法 / 写 HLS 要综合的核心函数
test.cpp 文件：构造输入 / 调用函数 / 检查输出
```

```cpp
testbench 输入 A、B
        ↓
运行 C++ matrix_mult 得到参考输出
        ↓
运行 Verilog RTL matrix_mult 得到硬件输出
        ↓
比较两者是否一致
```

| 参数 / 指标     | 你报告中的位置         | 含义                       | 和算法的关系                       | 在硬件中的功能                      |
| --------------- | ---------------------- | -------------------------- | ---------------------------------- | ----------------------------------- |
| `Top Function`  | `matrix_mult`          | 被综合成硬件 IP 的函数     | 指定哪个算法函数变成硬件           | 决定 RTL 顶层模块                   |
| `Target device` | `xc7z020-clg400-1`     | 目标 FPGA 型号             | 决定资源上限                       | 决定 LUT / FF / DSP / BRAM 可用数量 |
| `Clock period`  | 例如 `10 ns`           | 目标时钟周期               | 影响单周期能完成多少逻辑           | 决定目标频率，如 10 ns = 100 MHz    |
| `RTL`           | `Verilog`              | HLS 输出的硬件描述语言     | C++ 被翻译后的硬件结果             | 后续给 Vivado 综合/实现使用         |
| `Latency`       | 你报告里约 `67 cycles` | 一次函数执行需要多少周期   | 由循环次数、流水线、资源调度决定   | 衡量单次计算延迟                    |
| `II`            | Initiation Interval    | 两次连续计算之间的启动间隔 | 受循环依赖、数组端口、资源冲突影响 | 衡量流水线吞吐能力                  |
| `LUT`           | Synthesis Report       | 查找表资源                 | 与控制逻辑、加法、选择器有关       | 实现组合逻辑                        |
| `FF`            | Synthesis Report       | 触发器资源                 | 与寄存器、流水线级数有关           | 存储状态和中间数据                  |
| `DSP`           | Synthesis Report       | 乘法/乘加资源              | 与乘法数量有关                     | 实现高速乘法和 MAC                  |
| `BRAM`          | Synthesis Report       | 片上块 RAM                 | 与数组缓存、Buffer 有关            | 存储输入、权重、中间特征            |