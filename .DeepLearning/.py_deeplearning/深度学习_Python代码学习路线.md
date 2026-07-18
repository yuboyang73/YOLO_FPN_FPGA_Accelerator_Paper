# 深度学习 Python 代码学习路线

> 本路线对应 `深度学习_整理版.md` 和当前 YOLO/FPN 熵剪枝论文方向。
> 目标不是重复抄理论，而是用 Python 把“神经网络基础 -> CNN/FPN 特征图 -> Entropy/L1/Random 剪枝 -> 论文实验证据”串成一条可练习、可复盘、可服务论文的方法链。

## 0. 学习主线

这份路线按下面的逻辑推进：

```text
NumPy shape
-> Affine 前向传播
-> 激活函数与损失函数
-> 反向传播与训练闭环
-> CNN 卷积/池化/BN
-> Conv-BN 推理融合
-> FPN feature map 理解
-> Entropy / L1 / Random 通道评分
-> 剪枝 mask 与数据量变化
-> 论文实验表格与硬件指标理解
```

你每写一个 `.py`，都要回答三个问题：

```text
1. 输入是什么，shape 是什么？
2. 这段代码对应哪个深度学习知识点？
3. 它和我的 YOLO/FPN 熵剪枝论文有什么关系？
```

## 1. 推荐目录结构

代码统一放在：

```text
.DeepLearning/.py_deeplearning/
```

推荐结构如下：

```text
.py_deeplearning/
├─ 00_python_numpy_basics/
├─ 01_affine_layer/
├─ 02_activation_functions/
├─ 03_softmax_cross_entropy/
├─ 04_gradient_descent/
├─ 05_backprop_layers/
├─ 06_two_layer_network/
├─ 07_training_tricks/
├─ 08_conv2d_basics/
├─ 09_pooling_layer/
├─ 10_batch_norm/
├─ 11_conv_bn_fusion/
├─ 12_cnn_forward_pipeline/
└─ 13_yolo_fpn_pruning_bridge/
```

已有文件保持原目录，不需要重新命名。后续如果要继续扩展论文相关练习，可以在 `13_yolo_fpn_pruning_bridge/` 下继续增加文件。

## 2. 第一阶段：把 shape 和 Affine 吃透

对应目录：

```text
00_python_numpy_basics/
01_affine_layer/
```

### 要融合的深度学习知识

- `X.shape = (N, D)`：batch 中有 `N` 个样本，每个样本 `D` 个特征。
- `W.shape = (D, H)`：把 `D` 个输入特征映射到 `H` 个输出神经元。
- `b.shape = (H,)`：每个输出神经元一个偏置。
- `Y = X @ W + b`：Affine 层前向传播。

### 必做代码

```text
00_python_numpy_basics/01_array_shape.py
00_python_numpy_basics/02_matrix_multiply.py
00_python_numpy_basics/03_broadcast_bias.py
01_affine_layer/01_single_affine_forward.py
01_affine_layer/02_batch_affine_forward.py
01_affine_layer/03_affine_shape_check.py
```

### 和论文的关系

YOLO/FPN 中的 feature map 本质上也是张量。你后面分析剪枝时，会频繁遇到：

```text
feature_map.shape = (N, C, H, W)
```

如果 `N, D, H` 的二维矩阵关系没弄清楚，后面很容易把 `batch size`、`channel`、`height/width` 混在一起。

这一阶段的论文连接点是：

```text
先学会看 shape，后面才能解释“剪掉的是通道 C，而不是样本 N 或空间尺寸 H/W”。
```

### 验收标准

- 能解释 `(N, D) @ (D, H) = (N, H)`。
- 能解释为什么 `W.shape` 不包含 batch size。
- 能解释为什么 bias 是 `(H,)`，不是 `(N,)`。

## 3. 第二阶段：激活函数、Softmax 和损失函数

对应目录：

```text
02_activation_functions/
03_softmax_cross_entropy/
```

### 要融合的深度学习知识

- ReLU：保留正值，负值变 0。
- Leaky ReLU：负半区保留小斜率，缓解 dying ReLU。
- Softmax：把类别得分 logits 转成概率。
- Cross entropy：惩罚真实类别概率太低。

### 必做代码

```text
02_activation_functions/01_sigmoid.py
02_activation_functions/02_relu.py
02_activation_functions/03_leaky_relu.py
02_activation_functions/04_relu_backward.py
03_softmax_cross_entropy/01_softmax_basic.py
03_softmax_cross_entropy/02_softmax_stable.py
03_softmax_cross_entropy/03_cross_entropy_one_hot.py
03_softmax_cross_entropy/04_softmax_with_loss.py
```

### 和论文的关系

你的阶段一实验最终要比较剪枝前后检测精度。精度变化不是直接由“剪掉多少通道”决定，而是由模型输出的分类/检测结果是否仍然正确决定。

这一阶段要建立的论文理解是：

```text
剪枝影响中间特征 -> 中间特征影响 logits -> logits 影响概率和检测结果 -> 最终影响 mAP / precision / recall。
```

### 必做观察

- 改变真实类别概率，观察 cross entropy 如何变化。
- 构造一组 logits，观察 Softmax 最大值不等于概率 1。
- 说明 Softmax 输出是概率，cross entropy 输出是损失，不要混为一个操作。

## 4. 第三阶段：梯度下降、反向传播和训练闭环

对应目录：

```text
04_gradient_descent/
05_backprop_layers/
06_two_layer_network/
07_training_tricks/
```

### 要融合的深度学习知识

- 梯度表示损失对参数变化的敏感程度。
- 反向传播用链式法则计算每层参数对损失的影响。
- `forward -> loss -> backward -> update` 是训练闭环。
- 训练集、验证集、测试集作用不同。

### 必做代码

```text
04_gradient_descent/01_gradient_sign_demo.py
04_gradient_descent/02_sgd_update.py
04_gradient_descent/03_learning_rate_compare.py
05_backprop_layers/01_add_layer.py
05_backprop_layers/02_mul_layer.py
05_backprop_layers/03_affine_backward.py
05_backprop_layers/04_relu_backward.py
05_backprop_layers/05_softmax_loss_backward.py
06_two_layer_network/01_forward_only.py
06_two_layer_network/02_loss_and_accuracy.py
06_two_layer_network/03_backward.py
06_two_layer_network/04_train_toy_data.py
07_training_tricks/01_xavier_init.py
07_training_tricks/02_he_init.py
07_training_tricks/03_momentum_sgd.py
07_training_tricks/04_l2_regularization.py
07_training_tricks/05_dropout_train_eval.py
```

### 和论文的关系

剪枝后通常需要 fine-tune。Fine-tune 的本质不是“重新发明模型”，而是：

```text
通道被删后，网络表达能力发生变化
-> 通过训练数据重新调整剩余参数
-> 尽量恢复 mAP、precision、recall
```

这一阶段要解决的问题是：

```text
为什么剪枝后不是只看模型能不能前向运行，还要微调和验证？
```

### 必做观察

- 比较学习率过大、过小对 loss 的影响。
- 比较 train / eval 下 Dropout 行为差异。
- 写一段注释解释：fine-tune 属于训练阶段，BN 融合属于推理阶段优化。

## 5. 第四阶段：CNN 基础算子

对应目录：

```text
08_conv2d_basics/
09_pooling_layer/
12_cnn_forward_pipeline/
```

### 要融合的深度学习知识

- Conv 用局部连接和权值共享提取图像特征。
- 多通道卷积把 `C_in` 个输入通道映射到 `C_out` 个输出通道。
- Pooling 改变空间尺寸，通常不含可学习参数。
- CNN 前向传播会产生中间 feature map。

### 必做代码

```text
08_conv2d_basics/01_single_channel_conv.py
08_conv2d_basics/02_multi_channel_conv.py
08_conv2d_basics/03_multi_kernel_output.py
08_conv2d_basics/04_stride_padding_shape.py
09_pooling_layer/01_max_pooling.py
09_pooling_layer/02_average_pooling.py
09_pooling_layer/03_pooling_shape_check.py
12_cnn_forward_pipeline/01_conv_relu_pool.py
12_cnn_forward_pipeline/02_simple_cnn_forward.py
12_cnn_forward_pipeline/03_feature_map_visual_check.py
```

### 和论文的关系

你的论文不是只研究最终输出，而是研究中间 FPN 特征图的通道贡献。CNN 阶段要先搞懂：

```text
Conv 输出 feature map
feature map 有 channel
channel 会带来计算量和数据搬运量
```

这一阶段的论文连接点是：

```text
FPN 多尺度特征图越多、通道越多，硬件推理时的数据搬运和缓存压力越大。
```

### 必做观察

- 打印每层输出 shape。
- 记录 `C, H, W` 如何变化。
- 计算一个 feature map 的数据量：

```text
num_elements = N * C * H * W
memory_bytes = num_elements * bytes_per_element
```

## 6. 第五阶段：BN 与推理融合

对应目录：

```text
10_batch_norm/
11_conv_bn_fusion/
```

### 要融合的深度学习知识

- BN 训练阶段使用 mini-batch 均值和方差。
- BN 推理阶段使用保存下来的 running mean / running var。
- 推理阶段 BN 可以写成固定线性变换。
- Conv + BN 可以融合成新的 `W'` 和 `b'`。

### 必做代码

```text
10_batch_norm/01_bn_training_forward.py
10_batch_norm/02_bn_inference_forward.py
10_batch_norm/03_bn_running_mean_var.py
11_conv_bn_fusion/01_conv_bn_separate.py
11_conv_bn_fusion/02_fuse_conv_bn_params.py
11_conv_bn_fusion/03_compare_before_after_fusion.py
```

### 和论文的关系

BN 融合是硬件推理加速中很典型的优化，它说明一个关键边界：

```text
训练阶段负责学参数
推理阶段负责让已训练模型更快、更省资源地运行
```

你的论文后续 HLS/FPGA 加速也要保持这个边界：

```text
剪枝和 BN 融合都服务于推理部署效率，但必须用验证指标证明精度没有明显崩坏。
```

### 必做观察

- 比较融合前后输出差异，使用 `np.max(np.abs(y1 - y2))`。
- 说明为什么训练阶段不能直接固定融合 BN。
- 写一句论文式解释：Conv-BN fusion reduces independent normalization computation during inference.

## 7. 第六阶段：YOLO/FPN 剪枝桥接

对应目录：

```text
13_yolo_fpn_pruning_bridge/
```

### 要融合的深度学习知识

- YOLO backbone 提取图像特征。
- FPN/neck 融合多尺度特征。
- FPN 输出的 feature map 通常可看成 `(N, C, H, W)`。
- 通道剪枝主要作用在 `C` 这个维度。

### 必做代码

```text
13_yolo_fpn_pruning_bridge/01_feature_map_tensor_shape.py
13_yolo_fpn_pruning_bridge/02_channel_l1_score.py
13_yolo_fpn_pruning_bridge/03_channel_entropy_score.py
13_yolo_fpn_pruning_bridge/04_random_channel_mask.py
13_yolo_fpn_pruning_bridge/05_apply_channel_mask.py
13_yolo_fpn_pruning_bridge/06_compare_pruning_scores.py
13_yolo_fpn_pruning_bridge/07_pruning_ratio_sweep.py
13_yolo_fpn_pruning_bridge/08_estimate_feature_memory.py
13_yolo_fpn_pruning_bridge/09_make_ablation_table.py
13_yolo_fpn_pruning_bridge/10_plot_accuracy_latency_tradeoff.py
```

### 论文必要操作 1：模拟 FPN feature map

用 NumPy 构造：

```text
feature_map.shape = (N, C, H, W)
```

你要能解释：

```text
N = batch size
C = channel 数，也是剪枝重点
H, W = 空间尺寸
```

验收问题：

```text
如果 feature_map.shape = (1, 128, 40, 40)，剪掉 25% 通道后 C 变成多少？
数据量减少多少？
```

### 论文必要操作 2：L1 通道评分

L1 可以对通道相关数值取绝对值求和，例如对 feature map：

```text
score[c] = sum(abs(feature_map[:, c, :, :]))
```

它代表一种 activation 版本的 L1 分数。若后续基于卷积权重，则可改成：

```text
score[out_channel] = sum(abs(weight[out_channel, :, :, :]))
```

验收问题：

```text
L1 看的是幅度大小，它和 entropy 看特征分布信息量有什么区别？
```

### 论文必要操作 3：Entropy 通道评分

Entropy 分数可以用直方图近似：

```text
1. 取某个通道的所有激活值
2. 用 histogram 得到概率分布 p
3. 计算 entropy = -sum(p * log(p))
```

注意：

```text
低熵不自动等于不重要。
高熵也不自动等于一定有用。
Entropy 是一种重要性假设，必须用 mAP / precision / recall 验证。
```

验收问题：

```text
为什么 Entropy 剪枝不能只看吞吐率，还要看 mAP？
```

### 论文必要操作 4：Random 通道 mask

Random 是无信息基线：

```text
随机选择要保留或删除的通道
```

它的作用不是追求最好，而是回答：

```text
Entropy 的效果是不是只是因为“剪掉通道”本身带来的？
```

验收问题：

```text
如果 Entropy 和 Random 都剪掉 30% 通道，但 Entropy 的 mAP 更高，说明什么？
```

### 论文必要操作 5：应用通道 mask

对 feature map 应用 mask：

```text
pruned_feature = feature_map[:, keep_channels, :, :]
```

要观察：

```text
剪枝前 shape:  (N, C, H, W)
剪枝后 shape:  (N, C_keep, H, W)
减少元素数:    N * (C - C_keep) * H * W
减少内存量:    减少元素数 * bytes_per_element
```

验收问题：

```text
为什么通道减少会减轻带宽压力和缓存压力？
```

## 8. 第七阶段：论文实验分析脚本

这一部分已经同步放在：

```text
13_yolo_fpn_pruning_bridge/
```

```text
13_yolo_fpn_pruning_bridge/06_compare_pruning_scores.py
13_yolo_fpn_pruning_bridge/07_pruning_ratio_sweep.py
13_yolo_fpn_pruning_bridge/08_estimate_feature_memory.py
13_yolo_fpn_pruning_bridge/09_make_ablation_table.py
13_yolo_fpn_pruning_bridge/10_plot_accuracy_latency_tradeoff.py
```

### 06_compare_pruning_scores.py

作用：

```text
对同一组模拟 feature map，同时计算 Entropy、L1、Random 的通道排序。
观察三种方法选择的通道是否一致。
```

论文理解：

```text
如果三种方法选出的通道不同，说明它们判断“重要性”的标准不同。
```

### 07_pruning_ratio_sweep.py

作用：

```text
模拟 pruning ratio = 10%, 20%, 30%, 40%, 50%
统计每个比例下保留通道数和数据量减少比例。
```

论文理解：

```text
剪枝率越高，硬件负载越低，但精度风险越大。
```

### 08_estimate_feature_memory.py

作用：

```text
输入 N, C, H, W, bytes_per_element
估算 feature map 的数据量和剪枝后的数据量。
```

论文理解：

```text
把“FPN 特征图导致带宽压力”变成可以量化的数字。
```

### 09_make_ablation_table.py

作用：

```text
把 Entropy / Random / L1 的 mAP、FLOPs、params、latency、throughput 整理成表格。
```

论文理解：

```text
论文不是只说方法有效，而是用对照实验表格证明 trade-off。
```

### 10_plot_accuracy_latency_tradeoff.py

作用：

```text
画出 accuracy-latency 或 mAP-FLOPs 曲线。
```

论文理解：

```text
Entropy 的优势应该体现为更好的 Pareto trade-off，而不是单看速度或单看精度。
```

## 9. 每个练习文件建议格式

每个 `.py` 文件都按下面结构写：

```text
1. import numpy as np
2. 构造最小输入数据
3. 打印输入 shape
4. 执行核心计算
5. 打印输出 shape
6. 打印关键数值
7. 写 2-3 行注释说明：
   - 对应哪个深度学习知识点
   - 和 YOLO/FPN 剪枝论文有什么关系
```

建议每个目录的 `README.md` 写三段：

```text
1. 本目录练什么
2. 我通过代码看懂了什么
3. 这个知识点如何服务论文
```

## 10. 推荐四周学习安排

### Week 1：神经网络基础代码

完成：

```text
00_python_numpy_basics/
01_affine_layer/
02_activation_functions/
03_softmax_cross_entropy/
```

本周论文连接：

```text
理解 logits、probability、loss，避免把 Softmax 和交叉熵混为一谈。
```

### Week 2：训练闭环和反向传播

完成：

```text
04_gradient_descent/
05_backprop_layers/
06_two_layer_network/
07_training_tricks/
```

本周论文连接：

```text
理解剪枝后为什么要 fine-tune，以及 fine-tune 是如何通过反向传播恢复性能的。
```

### Week 3：CNN 和 BN 推理优化

完成：

```text
08_conv2d_basics/
09_pooling_layer/
10_batch_norm/
11_conv_bn_fusion/
12_cnn_forward_pipeline/
```

本周论文连接：

```text
理解 feature map、channel、Conv-BN fusion、训练/推理边界。
```

### Week 4：YOLO/FPN 熵剪枝桥接

完成：

```text
13_yolo_fpn_pruning_bridge/
```

本周论文连接：

```text
理解 Entropy / L1 / Random 三类剪枝标准，以及为什么最终要比较精度、数据量、延迟和吞吐率的 trade-off。
```

## 11. 最小验收标准

每完成一个目录，至少检查：

```text
1. 代码能独立运行。
2. 每一步都打印 shape。
3. 输出和手算的小例子能对上。
4. README.md 里写清楚该目录对应的深度学习知识点。
5. 能解释这个练习和 YOLO/FPN 熵剪枝论文的关系。
```

每完成一个论文相关脚本，至少输出：

```text
1. 输入 feature map 或实验结果来自哪里。
2. 输出了什么分数、mask、表格或图。
3. 它支持论文中的哪一句结论。
4. 它不能证明什么，避免夸大。
```

## 12. 一句话目标

这套 Python 路线的目标不是只学会写深度学习代码，而是让你能用代码解释论文方法链：

```text
CNN/FPN 产生多尺度特征图
-> 特征图通道带来计算和带宽压力
-> Entropy / L1 / Random 给出不同通道重要性标准
-> 剪枝减少通道和数据搬运
-> fine-tune 恢复精度
-> mAP、latency、throughput、FLOPs、params 共同证明 trade-off
```
