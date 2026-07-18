"""
现在这个目录开始学反向传播的“局部层”。
也就是：每一层 forward 做一次计算，backward 负责把上游梯度传回去。

"""
import numpy as np


class AddLayer:
    def forward(self, x, y):
        out = x + y
        return out

    def backward(self, dout):
        dx = dout
        dy = dout
        return dx, dy


def main():
    layer = AddLayer()

    x = np.array([2.0, 3.0])
    y = np.array([10.0, 20.0])

    out = layer.forward(x, y)
    dx, dy = layer.backward(np.array([1.0, 1.0]))

    print("x.shape =", x.shape)
    print("y.shape =", y.shape)
    print("out.shape =", out.shape)
    print("x =", x)
    print("y =", y)
    print("out =", out)
    print("dx =", dx)
    print("dy =", dy)

"""
加法层 backward 体现了反向传播的基本模式：
上游梯度 * 本层局部梯度 = 传给前一层的梯度。
这些梯度继续往前传，最后用于计算参数梯度，再由优化器更新参数。
"""



if __name__ == "__main__":
    main()