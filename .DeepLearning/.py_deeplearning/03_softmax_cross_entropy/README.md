# 03_softmax_cross_entropy 学习总结

## 1. 本目录练了什么

本目录练习分类输出层最核心的两件事：

```text
1. Softmax：把网络输出的原始分数 logits 变成概率分布。
2. Cross Entropy：根据真实标签计算分类损失。
```

```cpp
Softmax 把 logits 变成概率。
Cross Entropy 惩罚真实类别概率太低。
Softmax with Loss 的反向传播梯度是 dlogits = y - t。
```

上一目录 `02_activation_functions` 学的是中间层的激活响应；本目录开始关注模型最终输出：

```text
logits -> probability -> loss
```

四个文件分别对应：

```text
01_softmax_basic.py
- 学习基础 Softmax。
- 重点：一组 logits 会变成总和为 1 的概率分布。

02_softmax_stable.py
- 学习数值稳定版 Softmax。
- 重点：先减去最大值，避免 exp 溢出。

03_cross_entropy_one_hot.py
- 学习 one-hot 标签下的交叉熵。
- 重点：交叉熵只关注真实类别对应的预测概率。

04_softmax_with_loss.py
- 把 Softmax 和 Cross Entropy 合起来。
- 重点：原始分数 -> 概率 -> 损失，并理解 dlogits = y - t。
```

## 2. Softmax

### 核心公式

```text
softmax(x_i) = exp(x_i) / sum(exp(x_j))
```

作用：

```text
一组任意分数 -> 一组概率
```

Softmax 输出满足：

```text
每个值都 > 0
所有值加起来 = 1
```

例子：

```text
logits = [2.0, 1.0, 0.1]
y = [0.659, 0.242, 0.099]
sum(y) = 1.0
```

### 为什么 Softmax 要用 exp

不能直接用：

```text
x_i / sum(x)
```

原因之一是 `x_i` 可能是负数，算出来的“概率”也可能是负数，而概率不能为负。

使用 `exp(x_i)` 有三个好处：

```text
1. exp(x_i) 一定是正数。
2. exp 会放大高分和低分之间的差异。
3. 再除以总和后，可以得到总和为 1 的概率分布。
```

如果两个 logits 相差 1，则指数后相差约：

```text
exp(1) ≈ 2.718 倍
```

所以：

```text
[1000, 1001, 1002]
```

虽然相邻只差 1，但 Softmax 后概率差异会比较明显。

## 3. 数值稳定版 Softmax

普通写法：

```python
exp_x = np.exp(x)
y = exp_x / np.sum(exp_x)
```

问题：

```text
如果 x = [1000, 1001, 1002]，
np.exp(1000) 可能溢出成 inf。
```

稳定写法：

```python
x = x - np.max(x)
exp_x = np.exp(x)
y = exp_x / np.sum(exp_x)
```

例子：

```text
[1000, 1001, 1002] - 1002 = [-2, -1, 0]
```

这样最大值变成 0，其余值变成负数，`exp` 不容易溢出。

关键结论：

```text
softmax(x) = softmax(x - max(x))
```

减去最大值不会改变类别之间的相对大小，所以原来最大的类别仍然概率最大。

## 4. One-hot 标签

One-hot 编码是用一个向量表示真实类别：

```text
只有真实类别的位置是 1，其余位置都是 0。
```

注意 Python / NumPy 里索引从 0 开始：

```text
类别索引:  0  1  2
t =       [1, 0, 0]  -> 真实类别索引 0，口语里的第一类
t =       [0, 1, 0]  -> 真实类别索引 1，口语里的第二类
t =       [0, 0, 1]  -> 真实类别索引 2，口语里的第三类
```

如果有 4 个类别，真实类别索引是 2：

```text
t = [0, 0, 1, 0]
```

## 5. Cross Entropy

### 核心公式

```text
loss = -sum(t * log(y + eps))
```

其中：

```text
y = 模型预测概率
t = one-hot 真实标签
eps = 很小的数，防止 log(0)
```

代码：

```python
def cross_entropy(y, t):
    eps = 1e-7
    return -np.sum(t * np.log(y + eps))
```

### 为什么只关注真实类别概率

如果：

```text
y = [0.7, 0.2, 0.1]
t = [1, 0, 0]
```

那么：

```text
t * log(y) = [1*log(0.7), 0*log(0.2), 0*log(0.1)]
```

非真实类别被 0 消掉，最后只剩：

```text
loss = -log(0.7)
```

所以交叉熵本质上是：

```text
loss = -log(真实类别的预测概率)
```

规律：

```text
真实类别概率越高，loss 越小。
真实类别概率越低，loss 越大。
```

例如：

```text
-log(0.9) ≈ 0.105
-log(0.7) ≈ 0.357
-log(0.1) ≈ 2.303
```

## 6. Softmax with Loss

Softmax with Loss 把两步合起来：

```text
logits -> softmax -> y -> cross entropy -> loss
```

其中：

```text
logits = 网络直接输出的原始分数
y = logits 经过 softmax 后得到的概率
t = one-hot 真实标签
loss = 分类损失
```

例子：

```text
logits = [2.0, 1.0, 0.1]
y = [0.659, 0.242, 0.099]
t = [1, 0, 0]
loss ≈ -log(0.659) ≈ 0.417
```

`t = [1, 0, 0]` 表示真实类别索引 0，所以 loss 主要由 `y[0]` 决定。

## 7. Softmax with Loss 的反向传播直觉

重要结论：

```text
dlogits = y - t
```

其中：

```text
y = softmax 输出概率
t = one-hot 真实标签
```

例子：

```text
y = [0.2, 0.7, 0.1]
t = [0, 1, 0]

dlogits = y - t
        = [0.2, -0.3, 0.1]
```

真实类别是索引 1，对应梯度是：

```text
-0.3
```

它是负数。梯度下降更新规则是：

```text
z_new = z_old - lr * gradient
```

所以负梯度会让真实类别 logit 变大：

```text
z_new = z_old - lr * (-0.3)
      = z_old + 0.3lr
```

含义：

```text
真实类别概率不够高 -> 把真实类别 logit 往上推。
错误类别概率过高 -> 把错误类别 logit 往下压。
```

更严重错误的例子：

```text
y = [0.8, 0.1, 0.1]
t = [0, 1, 0]

dlogits = [0.8, -0.9, 0.1]
```

解释：

```text
真实类别概率只有 0.1，离目标 1 差很多，所以真实类别梯度是 -0.9。
第 0 类错误概率高达 0.8，所以第 0 类梯度是 0.8，需要明显往下压。
```

## 8. 我出错或补充过的点

### 点 1：类别索引和口语“第几类”容易混

标准理解：

```text
Python 索引从 0 开始。
类别索引 1 = 口语里的第二类。
```

### 点 2：dlogits 是向量，不是单个数

错误理解：

```text
dlogits = -0.3
```

正确理解：

```text
dlogits = y - t，是逐元素相减得到的向量。
```

例如：

```text
[0.2, 0.7, 0.1] - [0, 1, 0] = [0.2, -0.3, 0.1]
```

### 点 3：负梯度不是往下压，而是往上推

标准理解：

```text
梯度下降沿负梯度方向更新。
如果 gradient 是负数，减去负数会让变量变大。
```

所以真实类别梯度为负时，是把真实类别 logit 往上推。

### 点 4：Softmax 输出相差明显，是因为 exp 放大比例

标准理解：

```text
logits 相差 1，exp 后大约相差 e 倍。
```

所以 Softmax 中相邻 logits 差 1，概率可能已经有明显差异。

## 9. 和 YOLO/FPN 熵剪枝论文的关系

剪枝和激活函数改变的是中间 feature map 或网络结构，但最终评价模型好不好，需要看输出预测是否仍然正确。

本目录帮助理解：

```text
1. 网络输出 logits 后，如何变成概率。
2. 真实类别概率低时，为什么 loss 会变大。
3. loss 如何通过梯度 y - t 指导模型更新。
4. 剪枝后 fine-tune 为什么能让剩余参数重新适应任务。
```

和论文实验的连接：

```text
剪枝后如果真实类别概率下降，loss 会增大，mAP 可能下降。
fine-tune 通过反向传播调整剩余参数，让真实类别概率重新提高。
所以不能只看中间 feature map，也要看最终检测输出和评价指标。
```

## 10. 自测题

### 题 1：Softmax 输出规律

```text
logits = [2.0, 1.0, 0.1]
```

问：

```text
哪个位置的 Softmax 概率最大？为什么？
```

### 题 2：数值稳定

```text
logits = [1000, 1001, 1002]
```

问：

```text
为什么普通 Softmax 可能溢出？稳定版 Softmax 怎么处理？
```

### 题 3：One-hot

```text
有 4 个类别，真实类别索引是 2。
```

问：

```text
one-hot 标签 t 应该是什么？
```

### 题 4：Cross Entropy

```text
y = [0.7, 0.2, 0.1]
t = [1, 0, 0]
```

问：

```text
loss 主要看 y 的哪个位置？为什么？
```

### 题 5：dlogits

```text
y = [0.2, 0.7, 0.1]
t = [0, 1, 0]
```

问：

```text
dlogits = y - t 是多少？真实类别 logit 应该往上推还是往下压？
```

### 题 6：论文迁移

问：

```text
为什么 Softmax with Loss 有助于理解剪枝后 fine-tune？
```

## 11. 一句话核心记忆点

```text
Softmax 把 logits 变成概率，Cross Entropy 惩罚真实类别概率太低，二者合起来的反向传播梯度就是 dlogits = y - t。
```
