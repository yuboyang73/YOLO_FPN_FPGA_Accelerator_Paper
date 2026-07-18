# 00 Python NumPy Basics

> 本目录对应深度学习代码学习的第一组：数组 shape、矩阵乘法、bias 广播。

## 1. array shape

文件：

```text
01_array_shape.py
```

核心规则：

```text
X.shape = (N, D)
```

含义：

```text
N = batch 中的样本数
D = 每个样本的输入特征数
```

例子：

```text
X.shape = (4, 3)
```

表示：

```text
4 个样本，每个样本 3 个特征
```

## 2. matrix multiply

文件：

```text
02_matrix_multiply.py
```

核心规则：

```text
(N, D) @ (D, H) = (N, H)
```

对应神经网络：

```text
X.shape = (N, D)
W.shape = (D, H)
Y.shape = (N, H)
```

含义：

```text
X = 一批输入样本
W = 权重矩阵
Y = 每个样本经过这一层后的输出
```

元素级公式：

```text
Y[n, h] = sum over d of X[n, d] * W[d, h]
```

理解方式：

```text
X 的一行 和 W 的一列做点乘，得到 Y 的一个元素。
```

三层循环含义：

```text
n = 第几个样本
h = 第几个输出神经元
d = 当前样本的第几个输入特征
```

## 3. broadcast bias

文件：

```text
03_broadcast_bias.py
```

Affine 层完整形式：

```text
Y = X @ W + b
```

shape 规则：

```text
X.shape = (N, D)
W.shape = (D, H)
b.shape = (H,)
Y.shape = (N, H)
```

偏置的意义：

```text
每个输出神经元有一个偏置。
偏置不是给每个样本单独设置的，而是给每个输出神经元设置的。
```

广播规则：

```text
X @ W =
[[10, 20, 30],
 [40, 50, 60]]

b = [1, 2, 3]

Y = X @ W + b =
[[11, 22, 33],
 [41, 52, 63]]
```

NumPy 会把 `b` 自动加到每一行。

## 4. 易错点

### 4.1 `(2,)` 和 `(1, 2)` 不一样

```python
np.array([1, 2]).shape
```

结果是：

```text
(2,)
```

这是长度为 2 的一维数组。

```python
np.array([[1, 2]]).shape
```

结果是：

```text
(1, 2)
```

这是 1 行 2 列的二维数组。

### 4.2 `W.shape` 看输入特征数，不看 batch size

如果：

```text
X.shape = (32, 10)
```

输出 5 个神经元，则：

```text
W.shape = (10, 5)
```

不是：

```text
W.shape = (32, 5)
```

因为 `32` 是样本数，权重矩阵不应该依赖 batch size。

### 4.3 手写 for 循环输出 `220.` 不是错误

如果用：

```python
Y = np.zeros((N, H))
```

NumPy 默认创建 float 数组，所以结果可能显示为：

```text
220.
```

这表示：

```text
220.0
```

如果想显示整数，可以写：

```python
Y = np.zeros((N, H), dtype=int)
```

## 5. 自测题

1. 如果 `X.shape = (8, 784)`，输出 10 个类别得分，`W.shape` 和 `Y.shape` 分别是多少？

2. 如果：

```text
X @ W =
[[2, 4],
 [6, 8],
 [10, 12]]

b = [1, 3]
```

那么 `Y = X @ W + b` 等于多少？

3. 为什么 `b.shape = (H,)`，而不是 `(N,)`？

4. 用一句话解释：

```text
Y[n, h] = sum over d of X[n, d] * W[d, h]
```

这条公式在神经网络中表示什么？
