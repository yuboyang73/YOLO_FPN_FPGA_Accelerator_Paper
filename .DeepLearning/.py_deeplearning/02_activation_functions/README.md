# 02_activation_functions 学习总结

## 1. 本目录练了什么

本目录练习激活函数的前向传播和 ReLU 的反向传播。

上一目录 `01_affine_layer` 学的是线性变换：

```text
Y = X @ W + b
```

如果神经网络只堆 Affine / Conv 这类线性计算，多层线性变换本质上仍然可以合并成一层线性变换。激活函数的作用是加入非线性，让网络能表达更复杂的函数。

本目录包含：

```text
01_sigmoid.py
- 学习 Sigmoid 前向传播。
- 重点：把任意实数压到 0 到 1 之间。

02_relu.py
- 学习 ReLU 前向传播。
- 重点：负数变 0，正数保留原值。

03_leaky_relu.py
- 学习 Leaky ReLU 前向传播。
- 重点：负数不直接变成 0，而是保留 alpha*x。

04_relu_backward.py
- 学习 ReLU 反向传播。
- 重点：前向输入 x <= 0 的位置，梯度被阻断为 0。
```

## 2. 核心公式

### Sigmoid

```text
sigmoid(x) = 1 / (1 + exp(-x))
```

数值规律：

```text
x < 0  -> 输出小于 0.5，靠近 0
x = 0  -> 输出等于 0.5
x > 0  -> 输出大于 0.5，靠近 1
```

例子：

```text
sigmoid(-2) ≈ 0.119
sigmoid(-1) ≈ 0.269
sigmoid(0)  = 0.5
sigmoid(1)  ≈ 0.731
sigmoid(2)  ≈ 0.881
```

### ReLU

```text
ReLU(x) = max(0, x)
```

数值规律：

```text
x < 0  -> 0
x = 0  -> 0
x > 0  -> x
```

例子：

```text
ReLU([-3, 0, 5]) = [0, 0, 5]
```

### Leaky ReLU

```text
LeakyReLU(x) = x,        if x > 0
LeakyReLU(x) = alpha*x,  if x <= 0
```

通常：

```text
alpha = 0.01
```

例子：

```text
LeakyReLU([-3, 0, 5]) = [-0.03, 0, 5]
```

### ReLU backward

ReLU 反向传播规则：

```text
如果前向输入 x > 0：
    梯度原样通过

如果前向输入 x <= 0：
    梯度变成 0
```

代码：

```python
dx = dout.copy()
dx[x <= 0] = 0
```

例子：

```text
x    = [-2, 0, 3]
dout = [10, 10, 10]
dx   = [0, 0, 10]
```

## 3. Shape 规则

激活函数通常是逐元素函数：

```text
输入 shape = 输出 shape
```

例如：

```text
X.shape = (5,)
Y.shape = (5,)
```

二维 feature map 也是一样：

```text
X.shape = (2, 3)
Y.shape = (2, 3)
```

激活函数改变的是每个元素的数值响应，不改变数组结构。

## 4. 重要 NumPy 语法

### np.maximum 和 np.max 的区别

`np.maximum` 是逐元素比较，适合写 ReLU：

```python
np.maximum(0, X)
```

例子：

```text
X = [-2, -1, 0, 1, 2]
np.maximum(0, X) = [0, 0, 0, 1, 2]
```

`np.max` 是从数组中求最大值：

```python
np.max(X)
```

例子：

```text
np.max([-2, -1, 0, 1, 2]) = 2
```

一句话：

```text
np.maximum 用来逐元素做 ReLU；np.max 用来找数组里的最大值。
```

### np.where

Leaky ReLU 使用：

```python
np.where(x > 0, x, alpha * x)
```

含义：

```text
如果 x > 0，取 x
否则，取 alpha * x
```

### copy

ReLU backward 中：

```python
dx = dout.copy()
```

作用是复制一份上游梯度，避免直接修改原始的 `dout`。

如果写成：

```python
dx = dout
```

则 `dx` 和 `dout` 指向同一个数组，后面修改 `dx` 时可能影响 `dout`。

### 布尔索引

```python
dx[x <= 0] = 0
```

含义：

```text
先判断 x <= 0，得到 True / False mask。
再把 mask 为 True 的位置对应的 dx 改成 0。
```

例如：

```text
x = [-2, 0, 3]
x <= 0 = [True, True, False]
dx = [10, 10, 10]
dx[x <= 0] = 0
dx = [0, 0, 10]
```

## 5. 我出错或补充过的点

### 点 1：Sigmoid 的输出范围

标准理解：

```text
Sigmoid 把输入压到 0 到 1 之间。
负数输出小于 0.5，0 输出 0.5，正数输出大于 0.5。
```

### 点 2：ReLU 不会把正数压到 0 到 1

容易混淆：

```text
Sigmoid 会把大正数压到接近 1。
ReLU 不会压缩正数。
```

例子：

```text
ReLU(5) = 5
ReLU(100) = 100
```

### 点 3：Leaky ReLU 的关键不只是保留负值，而是保留负半区梯度

标准理解：

```text
ReLU 在 x < 0 时输出 0，局部梯度为 0。
Leaky ReLU 在 x < 0 时输出 alpha*x，局部梯度为 alpha。
```

所以 Leaky ReLU 可以缓解负半区完全没响应的问题。

### 点 4：fine-tune 依赖梯度更新参数

标准理解：

```text
fine-tune 不是根据前向输出直接改参数，
而是根据反向传播得到的梯度来更新参数。
```

如果某条路径的梯度一直为 0，这条路径相关参数就没有有效更新信号。

## 6. 标准理解

激活函数的核心作用：

```text
1. 接在线性计算之后。
2. 对每个元素独立处理。
3. 通常不改变 shape。
4. 改变特征响应的数值分布。
5. 引入非线性，使网络能表达复杂函数。
```

三种激活函数对比：

```text
Sigmoid:
- 输出范围是 0 到 1。
- 适合理解“压缩成概率样式响应”。

ReLU:
- 负数变 0，正数保留原值。
- 常用于 CNN，因为计算简单，正半区梯度稳定。

Leaky ReLU:
- 负数保留 alpha*x。
- 负半区仍然有小梯度 alpha。
```

ReLU backward 的核心：

```text
前向输入 x > 0 的位置，梯度通过。
前向输入 x <= 0 的位置，梯度阻断。
```

## 7. 和 YOLO/FPN 熵剪枝论文的关系

YOLO/FPN 中的特征图会经过卷积、BN、激活函数等模块。

激活函数帮助理解：

```text
feature map 中哪些位置/通道有强响应；
哪些位置被截断或弱化；
梯度能否从损失函数传回前面的层；
剪枝后 fine-tune 为什么依赖梯度重新调整剩余参数。
```

和 channel 剪枝的联系：

```text
剪枝会删除部分通道或分支。
剪枝后需要 fine-tune。
fine-tune 依赖反向传播的梯度更新剩余参数。
ReLU backward 帮助理解哪些位置能传回梯度，哪些位置梯度为 0。
```

本目录的核心价值：

```text
从“线性映射的 shape 理解”进入“特征响应和梯度传播理解”，
为后面学习 CNN、feature map、剪枝和 fine-tune 打基础。
```

## 8. 自测题

### 题 1：Sigmoid 输出规律

```text
X = [-2, 0, 2]
```

问：

```text
Sigmoid 输出分别靠近 0、0.5、还是 1？
```

### 题 2：ReLU 前向传播

```text
X = [-3, 0, 5]
```

问：

```text
ReLU(X) 是多少？
```

### 题 3：Leaky ReLU 前向传播

```text
alpha = 0.01
X = [-3, 0, 5]
```

问：

```text
LeakyReLU(X) 是多少？
```

### 题 4：ReLU backward

```text
X = [-2, 0, 3]
dout = [10, 10, 10]
```

问：

```text
dX 是多少？为什么？
```

### 题 5：shape 规则

问：

```text
为什么 Sigmoid、ReLU、Leaky ReLU 通常不会改变输入 shape？
```

### 题 6：论文迁移

问：

```text
为什么理解 ReLU backward 有助于理解剪枝后的 fine-tune？
```

## 9. 一句话核心记忆点

```text
激活函数逐元素改变特征响应，通常不改变 shape；ReLU backward 根据前向输入是否大于 0 决定梯度能否继续传递。
```
