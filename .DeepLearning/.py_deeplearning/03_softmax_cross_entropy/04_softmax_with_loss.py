"""
原始分数 -> 概率 -> 根据真实标签计算损失
"""
import numpy as np


def softmax(x):
    x = x - np.max(x)
    exp_x = np.exp(x)
    return exp_x / np.sum(exp_x)


def cross_entropy(y, t):
    eps = 1e-7
    return -np.sum(t * np.log(y + eps))

def main():
    logits = np.array([2.0,1.0,0.1])
    t = np.array([1,0,0])

    y = softmax(logits)
    loss = cross_entropy(y,t)

    print("logits.shape =", logits.shape)
    print("y.shape =", y.shape)
    print("t.shape =", t.shape)
    print("logits =", logits)
    print("y =", y)
    print("sum(y) =", np.sum(y))
    print("t =", t)
    print("loss =", loss)


if __name__ == "__main__":
    main()
