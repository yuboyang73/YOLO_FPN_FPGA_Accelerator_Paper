"""
负数不直接变成 0，而是保留一个很小的斜率。
"""
import numpy as np


def leaky_relu(x, alpha=0.01):
    return np.where(x > 0, x, alpha * x)


def main():
    X = np.array([-2.0,-1.0,0.0,1.0,2.0])

    Y = leaky_relu(X)

    print("X.shape =", X.shape)
    print("Y.shape =", Y.shape)
    print("X =", X)
    print("Y =", Y)


if __name__ == "__main__":
    main()