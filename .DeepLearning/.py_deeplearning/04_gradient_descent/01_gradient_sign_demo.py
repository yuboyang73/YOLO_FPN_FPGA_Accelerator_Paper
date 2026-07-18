"""
理解梯度符号和参数更新方向：
梯度 > 0：参数会变小
梯度 < 0：参数会变大
梯度 = 0：参数不变
"""
import numpy as np


def gradient_descent_step(param,grad,lr=0.1):
    return param - lr * grad


def main():
    param = np.array([2.0,2.0,2.0])
    grad = np.array([0.5,-0.5,0.0])

    new_param = gradient_descent_step(param,grad,lr=0.1)

    print("param.shape =", param.shape)
    print("grad.shape =", grad.shape)
    print("new_param.shape =", new_param.shape)

    print("param =", param)
    print("grad =", grad)
    print("new_param =", new_param)


if __name__ == "__main__":
    main()