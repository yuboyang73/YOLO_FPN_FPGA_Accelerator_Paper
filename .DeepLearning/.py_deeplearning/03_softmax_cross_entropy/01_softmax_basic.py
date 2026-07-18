"""
Softmax 把一组分数 logits 变成概率分布。
"""
import numpy as np


def softmax(x):
    exp_x = np.exp(x)
    return exp_x / np.sum(exp_x)

def main():
    X = np.array([2.0,1.0,0.1])

    Y = softmax(X)

    print("X.shape =", X.shape)
    print("Y.shape =", Y.shape)
    print("X =", X)
    print("Y =", Y)
    print("sum(Y) =", np.sum(Y))


if __name__ == "__main__":
    main()