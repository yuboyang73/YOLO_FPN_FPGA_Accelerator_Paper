"""
多个样本同时经过Affine层
"""
import numpy as np

def main():
    X = np.array([
        [1,2,3],
        [4,5,6],
    ])

    W = np.array([
        [10,20],
        [30,40],
        [50,60],
    ])

    b = np.array([1,2])

    Y = X @ W + b

    print("X.shape =", X.shape)
    print("W.shape =", W.shape)
    print("b.shape =", b.shape)
    print("Y.shape =", Y.shape)
    print("Y =")
    print(Y)

if __name__ == "__main__":
    main()