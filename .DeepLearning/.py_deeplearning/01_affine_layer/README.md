# 01_affine_layer 学习总结

## 1. 本目录练了什么

本目录练习 Affine 层的前向传播，也就是全连接层的基本计算：

```text
Y = X @ W + b
```

三个文件分别对应：

```text
01_single_affine_forward.py
- 单个样本经过 Affine 层。
- 重点理解一个输入向量如何变成多个输出神经元结果。

02_batch_affine_forward.py
- 多个样本同时经过 Affine 层。
- 重点理解 batch 维度 N 不参与权重 shape。

03_affine_shape_check.py
- 在计算前检查 shape 是否匹配。
- 重点理解 X、W、b 三者的维度约束。
```

## 2. 核心公式和 shape 规则

### 单个样本

```text
X.shape = (D,)
W.shape = (D, H)
b.shape = (H,)
Y.shape = (H,)
```

含义：

```text
D = 输入特征数
H = 输出特征数 / 输出神经元数
```

### 多个样本

```text
X.shape = (N, D)
W.shape = (D, H)
b.shape = (H,)
Y.shape = (N, H)
```

含义：

```text
N = 样本数
D = 每个样本的输入特征数
H = 每个样本的输出特征数 / 输出神经元数
```

矩阵乘法只看中间维度是否相等：

```text
(N, D) @ (D, H) = (N, H)
```

其中 `D` 被匹配掉，保留下来的外侧维度就是输出 shape。

## 3. Bias 广播

`b.shape = (H,)`，表示每个输出神经元一个 bias。

当：

```text
Y_without_bias.shape = (N, H)
b.shape = (H,)
```

NumPy 会把 `b` 自动加到每一个样本的输出上：

```text
第 1 个样本输出 + b
第 2 个样本输出 + b
...
第 N 个样本输出 + b
```

所以 `b` 的长度必须等于输出特征数 `H`，不是样本数 `N`。

## 4. Shape 检查规则

Affine 计算前必须检查两件事：

```text
1. X 的输入特征数必须等于 W 的输入维度：
   X.shape[1] == W.shape[0]

2. b 的长度必须等于 W 的输出维度：
   b.shape[0] == W.shape[1]
```

如果：

```text
X.shape = (8, 4)
W.shape = (4, 6)
b.shape = (6,)
```

则可以计算：

```text
Y.shape = (8, 6)
```

如果：

```text
X.shape = (8, 4)
W.shape = (5, 6)
b.shape = (6,)
```

则不能计算，因为：

```text
X 的输入特征数是 4
W 期待的输入维度是 5
4 != 5
```

## 5. 我出错过的点

### 错点 1：把 batch 维度当成输入特征数

错误理解：

```text
Y.shape = (2, 2) 中，第一个 2 是两个输入特征。
```

正确理解：

```text
X.shape = (2, 3)

2 = 样本数 N
3 = 每个样本的输入特征数 D
```

所以：

```text
Y.shape = (2, 2)

第一个 2 = 2 个样本
第二个 2 = 每个样本输出 2 个神经元结果
```

### 错点 2：以为 W 需要包含 batch size

错误理解：

```text
W.shape 可能需要写成 (N, D, H)。
```

正确理解：

```text
W.shape = (D, H)
```

原因：

```text
同一组权重 W 会作用在 batch 中的每一个样本上。
batch size 只是一次送进来多少条数据，不是模型参数的一部分。
```

### 错点 3：代码中二维数组每行长度不一致

错误写法：

```python
X = np.array([
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0, 7.0],
])
```

正确写法：

```python
X = np.array([
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0],
])
```

Affine 层要求 batch 中每个样本的特征数一致。

### 错点 4：Python 主函数入口写错

错误写法：

```python
if **name** == "**main**":
    main()
```

正确写法：

```python
if __name__ == "__main__":
    main()
```

## 6. 标准理解

Affine 层本质是把输入特征通过一组可学习参数映射到输出特征：

```text
输入特征 X
    ↓
权重矩阵 W 做线性组合
    ↓
加上 bias b
    ↓
得到输出 Y
```

标准表达：

```text
Affine 层的前向传播是 Y = X @ W + b。
对于 batch 输入，X.shape = (N, D)，W.shape = (D, H)，b.shape = (H,)，输出 Y.shape = (N, H)。
其中 N 是样本数，D 是输入特征数，H 是输出特征数。
```

## 7. 和 YOLO/FPN 熵剪枝论文的关系

Affine 层虽然不是 YOLO/FPN 中的主要算子，但它训练的是最基础的 shape 思维：

```text
输入维度必须和权重的输入维度对齐。
输出维度会影响下一层的输入维度。
```

这对后面理解 channel 剪枝很重要：

```text
如果剪枝把某层 feature map 的 channel 从 64 改成 48，
那么后面接收它的卷积层输入通道数也必须同步改成 48。
```

否则就会出现 shape 不匹配：

```text
前一层输出 channel = 48
后一层权重仍然期待 input channel = 64
计算无法正确进行
```

所以本目录的核心价值是：

```text
先用 Affine 层学会维度对齐，
再迁移到 CNN / FPN / channel pruning 的 shape 检查。
```

## 8. 自测题

### 题 1：基础 shape

```text
X.shape = (4, 3)
W.shape = (3, 2)
b.shape = (2,)
```

问：

```text
Y.shape 是多少？每一维代表什么？
```

### 题 2：shape 错误判断

```text
X.shape = (8, 4)
W.shape = (5, 6)
b.shape = (6,)
```

问：

```text
这个 Affine 能不能算？为什么？
```

### 题 3：bias 广播

```text
Y_without_bias.shape = (10, 5)
b.shape = (5,)
```

问：

```text
为什么 b 可以加到 Y_without_bias 上？
```

### 题 4：参数共享

问：

```text
为什么 W.shape 不包含 batch size？
```

### 题 5：论文迁移

问：

```text
为什么 Affine 层的 shape 检查，有助于理解 YOLO/FPN 的 channel 剪枝？
```

## 9. 一句话核心记忆点

```text
Affine 层就是 Y = X @ W + b；batch 维度 N 只表示样本数量，W 只负责把 D 维输入映射成 H 维输出。
```
