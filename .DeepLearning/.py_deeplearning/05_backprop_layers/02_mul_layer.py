"""
乘法层的反向传播。
"""
import numpy as np


class MulLayer:
    def __init__(self):
        self.x = None
        self.y = None

    def forward(self, x, y):
        self.x = x
        self.y = y
        out = x * y
        return out

    def backward(self, dout):
        dx = dout * self.y
        dy = dout * self.x
        return dx, dy



def main():
    layer = MulLayer()

    x = np.array([2.0,3.0])
    y = np.array([10.0,20.0])

    out = layer.forward(x,y)
    dx,dy = layer.backward(np.array([1.0,1.0]))

    print("x.shape =", x.shape)
    print("y.shape =", y.shape)
    print("out.shape =", out.shape)
    print("x =", x)
    print("y =", y)
    print("out =", out)
    print("dx =", dx)
    print("dy =", dy)


if __name__ == "__main__":
    main()