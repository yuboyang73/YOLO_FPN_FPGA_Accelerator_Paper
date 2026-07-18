"""
SGD 参数更新。
Stochastic Gradient Descent = 随机梯度下降
W = W - lr * dW
b = b - lr * db
区别是：SGD 通常用一个 batch 或 mini-batch 算出来的梯度来更新参数，而不是每次都用完整数据集。
"""
import numpy as np
from sympy.physics.vector.printing import params


def sgd_update(params, grads, lr =0.1):
    for key in params:
        params[key] = params[key] - lr * grads[key]

def main():
    params = {
        "W": np.array([1.0,2.0,3.0]),
        "b":np.array([0.5]),
    }

    grads = {
        "W":np.array([0.1,-0.2,0.3]),
        "b":np.array([0.4])
    }

    print("Before update:")
    print("W =", params["W"])
    print("b =", params["b"])

    sgd_update(params, grads, lr=0.1)

    print("After update:")
    print("W =", params["W"])
    print("b =", params["b"])


if __name__ == "__main__":
    main()

