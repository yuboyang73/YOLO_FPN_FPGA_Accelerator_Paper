"""
Affine层shape检查
"""
import numpy as np

def main():
    X = np.array([
        [1.0,2.0,3.0],
        [4.0,5.0,6.0],
    ])

    W = np.array([
        [0.1,0.2],
        [0.3,0.4],
        [0.5,0.6],
    ])

    b = np.array([0.01,0.02])

    print("X.shape =", X.shape)
    print("W.shape =", W.shape)
    print("b.shape =", b.shape)

    if X.shape[1] != W.shape[0]:
        print("Error: X 的特征数必须等于 W 的输入维度")
        return
    if W.shape[1] != b.shape[0]:
        print("Error: b 的长度必须等于 W 的输出维度")
        return

    Y = X @ W + b

    print("Y.shape =", Y.shape)
    print("Y =")
    print(Y)

if __name__ == "__main__":
    main()

