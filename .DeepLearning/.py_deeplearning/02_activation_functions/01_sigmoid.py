"""
激活函数不是改变 shape，而是改变每个元素的数值响应。
"""
import numpy as np

def sigmoid(x):
    return 1/(1 + np.exp(-x))

def main():
    X = np.array([-2.0,-1.0,0.0,1.0,2.0])

    Y = sigmoid(X)

    print("X.shape =", X.shape)
    print("Y.shape =", Y.shape)
    print("X =", X)
    print("Y =", Y)

if __name__ == "__main__":
    main()