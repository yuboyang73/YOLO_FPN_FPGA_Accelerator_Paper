"""
学习率 learning rate 对更新幅度的影响。
lr 越大：每次更新步子越大
lr 越小：每次更新步子越小
"""
import numpy as np



def update(param,grad,lr):
    return param - lr * grad

def main():
    param = np.array([2.0])
    grad = np.array([0.5])

    learning_rates = [0.01,0.1,1.0]

    print("param =", param)
    print("grad =", grad)

    for lr in learning_rates:
        new_param = update(param, grad, lr)
        print("lr =", lr, "new_param =", new_param)


if __name__ == "__main__":
    main()