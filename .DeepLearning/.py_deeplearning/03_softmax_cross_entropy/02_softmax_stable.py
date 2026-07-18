"""
数值稳定版 Softmax
"""
import numpy as np

def softmax(x):
    x = x - np.max(x)
    exp_x = np.exp(x)
    return exp_x / np.sum(exp_x)

def main():
    X = np.array([1000.0, 1001.0, 1002.0])

    Y = softmax(X)

    print("X.shape =", X.shape)
    print("Y.shape =", Y.shape)
    print("X =", X)
    print("Y =", Y)
    print("sum(Y) =", np.sum(Y))


if __name__ == "__main__":
    main()