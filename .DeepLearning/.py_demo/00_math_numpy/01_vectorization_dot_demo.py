import numpy as np

def non_vectorized_dot(w,x,b):
    '''
    非向量化写法：使用 for 循环手动计算

     数学公式：
        z = w1 * x1 + w2 * x2 + ... + wn * xn + b
    '''

    z = 0

    for i in range(len(w)):
        z += w[i] * x[i]
    z += b

    return z

def vectorized_dot(w,x,b):
    '''
    向量化写法：使用Numpy一次性完成点积计算

    数学公式：
        z = w^T x + b
    '''

    z = np.dot(w,x) + b

    return z

def matrix_form_dot(w,x,b):
    '''
    矩阵形式写法：显示展示w.T @ x

    注意:
        w 和 x 原本是一维数组
        为了展示 w^T x，需要先把它们变成列向量
    '''

    w_col = w.reshape(-1,1) # shape : (n,1)
    x_col = x.reshape(-1,1) # shape : (n,1)

    z = np.dot(w_col.T,x_col) + b # shape:(1,1)

    return z[0][0]

if __name__ == "__main__":
    print("演示z = w^T x + b 的非向量化、向量化和矩阵形式机选\n")

    # 输入特征数量为4
    # w 表示权重向量
    w = np.array([0.5,-1.2,3.0,2.1])

    # x 表示输入特征向量
    x = np.array([2.0,1.5,-0.5,3.0])

    #b 表示偏置 bias
    b = 0.8

    #法一：循环
    z1 = non_vectorized_dot(w,x,b)
    #法二：向量化
    z2 = vectorized_dot(w,x,b)
    #法三：矩阵计算
    z3 = matrix_form_dot(w,x,b)

    print("w =",w)
    print("x =",x)
    print("b =",b)

    print("\n计算结果：")
    print("非向量化结果 z1 =", z1)
    print("向量化结果   z2 =", z2)
    print("矩阵形式结果 z3 =", z3)

    print("\n结果一致性检查：")
    print("z1 == z2:", np.isclose(z1, z2))
    print("z2 == z3:", np.isclose(z2, z3))

    print("\n数学展开：")
    print("z = 0.5*2.0 + (-1.2)*1.5 + 3.0*(-0.5) + 2.1*3.0 + 0.8")