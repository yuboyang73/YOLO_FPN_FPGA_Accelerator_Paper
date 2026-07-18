"""
理解交叉熵的直觉：
真实类别概率越高，loss 越小
真实类别概率越低，loss 越大
"""
import numpy as np


def cross_entropy(y, t):
    eps = 1e-7
    return -np.sum(t * np.log(y + eps))


def main():
    y = np.array([0.7, 0.2, 0.1])
    t = np.array([1, 0, 0])

    loss = cross_entropy(y, t)

    print("y.shape =", y.shape)
    print("t.shape =", t.shape)
    print("y =", y)
    print("t =", t)
    print("loss =", loss)


if __name__ == "__main__":
    main()
