# 04_gradient_descent 学习总结

## 1. 本目录练了什么

本目录学习有了梯度以后，参数如何更新。

上一目录 `03_softmax_cross_entropy` 学到：

```text
Softmax with Loss 的反向传播梯度是 dlogits = y - t。
```

本目录继续回答：

```text
拿到梯度以后，W、b 这些参数怎么变化？
```

核心公式：

```text
new_param = old_param - learning_rate * gradient
```

三个文件分别对应：

```text
01_gradient_sign_demo.py
- 学习梯度符号和参数更新方向。
- 重点：正梯度让参数变小，负梯度让参数变大。

02_sgd_update.py
- 学习用字典管理多组参数和梯度。
- 重点：params[key] = params[key] - lr * grads[key]。

03_learning_rate_compare.py
- 学习 learning rate 对更新幅度的影响。
- 重点：lr 太小更新慢，lr 太大可能震荡或发散。
```

## 2. 梯度下降更新公式

标准公式：

```text
new_param = old_param - lr * gradient
```

其中：

```text
old_param = 当前参数
gradient = loss 对该参数的梯度
lr = learning rate，学习率
new_param = 更新后的参数
```

梯度的含义：

```text
梯度指向 loss 上升最快的方向。
```

所以要让 loss 下降，就要沿相反方向走：

```text
参数更新 = 减去 learning_rate * gradient
```

## 3. 梯度符号和参数变化

如果：

```text
param = [2.0, 2.0, 2.0]
grad  = [0.5, -0.5, 0.0]
lr = 0.1
```

逐元素更新：

```text
new_param = param - lr * grad
          = [2.0, 2.0, 2.0] - 0.1 * [0.5, -0.5, 0.0]
          = [1.95, 2.05, 2.0]
```

规律：

```text
grad > 0 -> 参数变小
grad < 0 -> 参数变大
grad = 0 -> 参数不变
```

原因：

```text
梯度为正，说明参数增大时 loss 倾向增大，所以参数要反向变小。
梯度为负，说明参数增大时 loss 倾向减小，所以参数要变大。
```

## 4. SGD 参数更新

SGD 全称：

```text
Stochastic Gradient Descent
```

中文：

```text
随机梯度下降
```

更新公式仍然是：

```text
W = W - lr * dW
b = b - lr * db
```

SGD 通常用一个 batch 或 mini-batch 算出来的梯度来更新参数，而不是每次都用完整数据集。

## 5. 为什么 params 和 grads 用字典

神经网络通常有多组参数：

```text
W, b
W1, b1, W2, b2
Conv1_W, Conv1_b, Affine1_W, Affine1_b
```

用字典可以用名字管理每组参数：

```python
params = {
    "W": np.array([1.0, 2.0, 3.0]),
    "b": np.array([0.5]),
}
```

对应梯度用相同 key 保存：

```python
grads = {
    "W": np.array([0.1, -0.2, 0.3]),
    "b": np.array([0.4]),
}
```

这样就可以统一更新：

```python
for key in params:
    params[key] = params[key] - lr * grads[key]
```

含义：

```text
key = "W" 时，更新 params["W"]
key = "b" 时，更新 params["b"]
```

## 6. SGD 更新例子

如果：

```text
W = [1.0, 2.0, 3.0]
dW = [0.1, -0.2, 0.3]
lr = 0.1
```

则：

```text
new_W = W - lr * dW
      = [1.0, 2.0, 3.0] - 0.1 * [0.1, -0.2, 0.3]
      = [0.99, 2.02, 2.97]
```

如果：

```text
b = [0.5]
db = [0.4]
lr = 0.1
```

则：

```text
new_b = [0.5] - 0.1 * [0.4]
      = [0.46]
```

## 7. Learning Rate 的作用

学习率控制每次更新走多大一步。

如果：

```text
param = [2.0]
grad = [0.5]
```

不同学习率下：

```text
lr = 0.01 -> new_param = [1.995]
lr = 0.1  -> new_param = [1.95]
lr = 1.0  -> new_param = [1.5]
```

规律：

```text
lr 越大，参数一步变化越大。
lr 越小，参数一步变化越小。
```

学习率太小：

```text
loss 下降慢，训练效率低。
```

学习率太大：

```text
一步跨太远，可能越过低 loss 区域。
下一步梯度方向改变后，又跨回另一边。
最终可能震荡，甚至发散。
```

## 8. Fine-tune 流程

fine-tune 可以理解成：

```text
在已有模型基础上，用较小学习率继续训练，让模型适应新结构或新数据。
```

结合剪枝场景：

```text
1. 先有一个训练好的 baseline 模型。
2. 对模型做剪枝，例如删除低信息量 FPN 分支或通道。
3. 剪枝后模型结构改变，mAP / loss 可能变差。
4. 用训练集继续训练剪枝后的模型。
5. forward 得到预测。
6. 计算 loss。
7. backward 得到剩余参数的梯度。
8. 用 SGD / Adam 等优化器更新剩余参数。
9. 在验证集上观察 loss 和 mAP 是否恢复。
```

一句话：

```text
fine-tune = 剪枝或迁移后，保留已有权重，用较小学习率继续训练，让剩余参数重新适应任务。
```

## 9. 我出错或补充过的点

### 点 1：正梯度和参数变化方向

错误理解：

```text
梯度为正时，参数变大时 loss 变小。
```

正确理解：

```text
梯度为正，表示参数增大时 loss 倾向增大。
为了让 loss 下降，参数应该变小。
```

### 点 2：字典保存 params / grads 的意义

标准理解：

```text
用字典可以用名字管理每组参数，并且 grads 用相同 key 保存对应梯度。
```

### 点 3：fine-tune 不是重新随机训练

标准理解：

```text
fine-tune 是在已有权重基础上继续训练。
剪枝后只更新剩余参数，让模型重新适应任务。
```

### 点 4：学习率太大不利于 fine-tune

标准理解：

```text
fine-tune 通常希望在已有权重附近微调。
学习率太大可能破坏已有特征，使 loss/mAP 震荡。
```

## 10. 代码注意点

`02_sgd_update.py` 当前有一行不必要的导入：

```python
from sympy.physics.vector.printing import params
```

这行和 SGD 更新无关，可以删除。

SGD 示例只需要：

```python
import numpy as np
```

## 11. 和 YOLO/FPN 熵剪枝论文的关系

论文中的信息熵剪枝会改变 FPN 结构：

```text
删除低信息量分支或通道。
```

剪枝后模型通常需要 fine-tune：

```text
剩余参数继续通过梯度下降更新。
loss 下降后，真实类别预测概率提高。
mAP 有机会恢复到接近 baseline。
```

本目录帮助理解：

```text
1. 剪枝后为什么还要继续训练。
2. 剩余参数如何根据梯度更新。
3. 学习率为什么影响 fine-tune 稳定性。
4. 为什么不能随便用特别大的 learning rate。
```

## 12. 自测题

### 题 1：梯度符号

```text
param = [3.0, 3.0]
grad = [0.2, -0.4]
lr = 0.1
```

问：

```text
new_param 是多少？每个参数分别朝哪个方向变化？
```

### 题 2：SGD 字典更新

```python
params = {"W1": np.array([1.0, 2.0]), "b1": np.array([0.5])}
grads = {"W1": np.array([0.3, -0.1]), "b1": np.array([0.2])}
lr = 0.1
```

问：

```text
更新后的 W1 和 b1 是多少？
为什么 params 和 grads 要使用相同 key？
```

### 题 3：学习率比较

```text
param = [2.0]
grad = [0.5]
```

问：

```text
lr = 0.01、0.1、1.0 时，更新幅度有什么区别？
```

### 题 4：学习率过大

问：

```text
为什么学习率太大可能导致 loss 震荡，而不是稳定下降？
```

### 题 5：论文迁移

问：

```text
为什么剪枝后 fine-tune 通常使用较小 learning rate？
请把“已有权重”“剩余参数”“loss 下降”“mAP 恢复”联系起来说明。
```

## 13. 一句话核心记忆点

```text
梯度下降用 new_param = old_param - lr * gradient 沿 loss 下降方向更新参数；剪枝后的 fine-tune 就是用较小学习率继续更新剩余参数，让模型重新适应任务。
```
