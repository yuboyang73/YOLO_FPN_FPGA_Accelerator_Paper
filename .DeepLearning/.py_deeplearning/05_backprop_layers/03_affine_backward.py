"""
Affine 层的反向传播
假设：
X.shape = (N, D)
W.shape = (D, H)
b.shape = (H,)
Y.shape = (N, H)
dout.shape = (N, H)

核心公式：
dX = dout @ W.T
dW = X.T @ dout
db = np.sum(dout, axis=0)
含义：
dX：loss 对输入 X 的梯度
dW：loss 对权重 W 的梯度
db：loss 对 bias b 的梯度

为什么要转置
forward 是 X @ W。
backward 要让 shape 对齐，反向把梯度传回 X 和 W。
"""
import numpy as np


class AffineLayer:
    def __init__(self, W, b):
        self.W = W
        self.b = b
        self.X = None
        self.dW = None
        self.db = None

    def forward(self, X):
        self.X = X
        out = X @ self.W + self.b
        return out

    def backward(self, dout):
        dX = dout @ self.W.T
        self.dW = self.X.T @ dout
        self.db = np.sum(dout, axis=0)
        return dX


def main():
    X = np.array([
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0],
    ])

    W = np.array([
        [0.1, 0.2],
        [0.3, 0.4],
        [0.5, 0.6],
    ])

    b = np.array([0.01, 0.02])

    layer = AffineLayer(W, b)

    out = layer.forward(X)

    dout = np.array([
        [1.0, 1.0],
        [2.0, 2.0],
    ])

    dX = layer.backward(dout)

    print("X.shape =", X.shape)
    print("W.shape =", W.shape)
    print("b.shape =", b.shape)
    print("out.shape =", out.shape)
    print("dout.shape =", dout.shape)
    print("dX.shape =", dX.shape)
    print("dW.shape =", layer.dW.shape)
    print("db.shape =", layer.db.shape)

    print("out =")
    print(out)
    print("dX =")
    print(dX)
    print("dW =")
    print(layer.dW)
    print("db =")
    print(layer.db)


if __name__ == "__main__":
    main()