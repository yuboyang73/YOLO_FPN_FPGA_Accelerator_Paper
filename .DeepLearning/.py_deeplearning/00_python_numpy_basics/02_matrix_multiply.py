import numpy as np
'''
X.shape = (N, D)
W.shape = (D, H)
Y.shape = (N, H)
用numpy数组实现矩阵乘法运算，把每个样本的D个输入特征，组合成H个输出特征
例：
32 张图片
每张图片 784 个像素
通过一层权重 W
变成每张图片 10 个类别得分
'''
# X.shape = (2,3)
# 2个样本，每个样本3个特征
X = np.array([
    [1,2,3],
    [4,5,6]
])

# W.shape = (3,2)
# 3个输入特征，2个输出神经元
W = np.array([
    [10,20],
    [30,40],
    [50,60]
])

#Y.shape = (2,2)
Y = X @ W

print("X:")
print(X)
print("X.shape:", X.shape)

print("W:")
print(W)
print("W.shape:", W.shape)

print("Y = X @ W:")
print(Y)
print("Y.shape:", Y.shape)

'''
用for循环方法来实现
'''

# X.shape = (2,3)
# 2个样本，每个样本3个特征
X = np.array([
    [1,2,3],
    [4,5,6]
])

# W.shape = (3,2)
# 3个输入特征，2个输出神经元
W = np.array([
    [10,20],
    [30,40],
    [50,60]
])

N = X.shape[0] #样本数2
D = X.shape[1] #输入特征数3
H = W.shape[1] #输出神经元数2

Y = np.zeros((N,H))

for n in range(N):
    for h in range(H):
        total = 0
        for d in range(D):
            total += X[n,d] * W[d,n]
        Y[n,h] = total

print(Y)
