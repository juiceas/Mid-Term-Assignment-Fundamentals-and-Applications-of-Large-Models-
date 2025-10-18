# Transformer模型实现

这是一个从零开始实现的完整Transformer模型（Encoder-Decoder架构），用于大模型课程期中作业。

## 项目结构

```
.
├── src/                          # 源代码目录
│   ├── __init__.py              # 包初始化文件
│   ├── model.py                 # Transformer模型实现
│   ├── data_loader.py           # 数据加载和预处理
│   ├── train.py                 # 训练脚本
│   └── ablation_study.py        # 消融实验脚本
├── configs/                      # 配置文件目录
│   ├── base.yaml                # 基础配置
│   ├── small.yaml               # 小型模型配置（快速测试）
│   └── large.yaml               # 大型模型配置
├── scripts/                      # 运行脚本目录
│   ├── run.sh                   # Linux/Mac运行脚本
│   └── run.bat                  # Windows运行脚本
├── results/                      # 结果保存目录（自动生成）
│   ├── training_curves.png      # 训练曲线图
│   ├── training_history.json    # 训练历史数据
│   └── ablation_study/          # 消融实验结果
├── checkpoints/                  # 模型检查点目录（自动生成）
│   └── best_model.pth           # 最佳模型
├── requirements.txt              # Python依赖包
├── README.md                     # 本文件
└── 说明文档.md                   # 简单易懂的说明文档

```

## 功能特性

### ✅ 核心组件实现

- **多头自注意力机制 (Multi-Head Self-Attention)**
  - 缩放点积注意力
  - 多头并行计算
  - 支持mask机制（padding mask和future mask）

- **位置前馈网络 (Position-wise Feed-Forward Network)**
  - 两层全连接网络
  - ReLU激活函数

- **位置编码 (Positional Encoding)**
  - 正弦余弦位置编码
  - 支持任意长度序列

- **残差连接 + Layer Normalization**
  - 每个子层都有残差连接
  - Layer Norm用于稳定训练

### ✅ 完整架构

- **Encoder**：多层Encoder堆叠
- **Decoder**：多层Decoder堆叠（支持自注意力和交叉注意力）
- **输出层**：线性投影到词汇表大小

### ✅ 训练功能

- **优化器**：Adam / AdamW（带权重衰减）
- **学习率调度**：Cosine Annealing / ReduceLROnPlateau
- **梯度裁剪**：防止梯度爆炸
- **模型保存/加载**：自动保存最佳模型和定期检查点
- **训练可视化**：实时进度条、训练曲线绘制

### ✅ 消融实验

支持多种超参数的消融研究：
- 注意力头数（2, 4, 8）
- 模型层数（2, 4, 6）
- 模型维度（128, 256, 512）
- Dropout率（0.0, 0.1, 0.3）
- 优化器类型（Adam, AdamW）

## 安装依赖

### 方法1：使用pip安装

```bash
pip install -r requirements.txt
```

### 方法2：使用conda创建环境

```bash
conda create -n transformer python=3.10
conda activate transformer
pip install -r requirements.txt
```

## 快速开始

### 1. 测试模型组件

```bash
# Linux/Mac
./scripts/run.sh test

# Windows
scripts\run.bat test
```

### 2. 训练基础模型

```bash
# Linux/Mac
./scripts/run.sh train

# Windows
scripts\run.bat train
```

或者直接运行Python脚本：

```bash
python src/train.py
```

### 3. 运行消融实验

```bash
# Linux/Mac
./scripts/run.sh ablation

# Windows
scripts\run.bat ablation
```

或者：

```bash
python src/ablation_study.py
```

## 详细使用说明

### 训练自定义模型

修改`src/train.py`中的配置参数：

```python
config = {
    # 模型参数
    'd_model': 256,        # 模型维度
    'n_heads': 8,          # 注意力头数
    'd_ff': 1024,         # 前馈网络维度
    'n_layers': 4,        # 层数
    'max_len': 100,       # 最大序列长度
    'dropout': 0.1,       # Dropout率
    
    # 训练参数
    'batch_size': 32,     # 批大小
    'epochs': 50,         # 训练轮数
    'lr': 3e-4,          # 学习率
    'optimizer': 'AdamW', # 优化器
}
```

### 数据集

当前实现支持两种测试任务：

1. **复制任务 (Copy Task)**：将输入序列复制到输出
   - 最简单的序列到序列任务
   - 用于验证模型基本功能

2. **合成翻译任务 (Synthetic Translation)**：简单的词汇映射
   - src_i → tgt_i的映射关系
   - 30%概率反转序列

可以通过修改配置中的`task`参数切换任务：

```python
config = {
    'task': 'copy',  # 或 'synthetic_translation'
    'num_samples': 2000,
}
```

### 模型参数统计

运行训练时会自动显示模型参数统计：

```
总参数数量: 5,234,688
可训练参数数量: 5,234,688
```

### 训练输出

训练过程会实时显示：
- 训练损失和困惑度
- 验证损失和困惑度
- 当前学习率
- 进度条

训练结束后会生成：
- `results/training_curves.png`：训练曲线图
- `results/training_history.json`：训练历史数据
- `checkpoints/best_model.pth`：最佳模型
- `checkpoints/checkpoint_epoch_*.pth`：定期检查点

### 消融实验结果

运行消融实验后会生成：
- `results/ablation_study/ablation_results.json`：实验结果汇总
- `results/ablation_study/ablation_comparison.png`：对比图表
- 每个实验的单独结果和曲线

## 重现实验

为了确保结果可重现，所有随机种子已固定：

```python
torch.manual_seed(42)
np.random.seed(42)
```

在相同的硬件和环境下，使用相同的命令应该能得到一致的结果。

### 完整重现命令

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 设置随机种子（已在代码中设置）
export PYTHONHASHSEED=42

# 3. 运行训练
python src/train.py

# 4. 运行消融实验
python src/ablation_study.py
```

## 硬件要求

### 最低要求
- CPU：任何现代CPU
- 内存：4GB RAM
- 存储：500MB可用空间

### 推荐配置
- CPU：多核处理器
- 内存：8GB RAM
- GPU：NVIDIA GPU with CUDA support（可选，会自动检测）
- 存储：2GB可用空间

### 训练时间估计

在不同硬件上的训练时间（50 epochs，2000样本）：

| 硬件配置 | 训练时间 |
|---------|---------|
| CPU (Intel i5) | ~30分钟 |
| GPU (GTX 1660) | ~5分钟 |
| GPU (RTX 3080) | ~2分钟 |

## 模型架构详解

### 1. 缩放点积注意力

```
Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V
```

- Q, K, V: Query, Key, Value矩阵
- d_k: Key的维度
- sqrt(d_k): 缩放因子，防止softmax饱和

### 2. 多头注意力

```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) * W^O
where head_i = Attention(Q*W_i^Q, K*W_i^K, V*W_i^V)
```

- h: 注意力头数
- W^Q, W^K, W^V: 投影矩阵
- W^O: 输出投影矩阵

### 3. 位置编码

```
PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

- pos: 位置索引
- i: 维度索引
- d_model: 模型维度

## 常见问题

### Q: 如何使用GPU训练？

A: 代码会自动检测可用的GPU。如果安装了CUDA版本的PyTorch，会自动使用GPU。

```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
```

### Q: 如何加载已保存的模型？

A: 使用Trainer的load_checkpoint方法：

```python
trainer = Trainer(model, train_loader, val_loader, config, device)
epoch = trainer.load_checkpoint('checkpoints/best_model.pth')
```

### Q: 训练过程中断了怎么办？

A: 可以从最近的检查点恢复训练：

```python
trainer.load_checkpoint('checkpoints/checkpoint_epoch_40.pth')
# 继续训练
```

### Q: 如何调整超参数？

A: 修改`src/train.py`中的config字典，或者创建新的配置文件（参考`configs/`目录）。

### Q: 内存不足怎么办？

A: 尝试减小以下参数：
- batch_size（例如从32减到16或8）
- d_model（例如从256减到128）
- n_layers（例如从4减到2）
- num_samples（减少数据量）

## 项目亮点

1. ✅ **完整的Encoder-Decoder架构**：不仅实现了Encoder，还实现了完整的Decoder
2. ✅ **清晰的代码结构**：模块化设计，易于理解和修改
3. ✅ **详细的数学推导**：代码中包含公式注释
4. ✅ **完善的训练流程**：包括优化器、学习率调度、梯度裁剪等最佳实践
5. ✅ **全面的消融实验**：系统地研究各个组件的影响
6. ✅ **可视化结果**：自动生成训练曲线和对比图表
7. ✅ **可重现性**：固定随机种子，提供详细的运行说明

## 参考文献

[1] Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017). Attention is all you need. Advances in neural information processing systems, 30.

## 作者

- 学生姓名：[待填写]
- 学号：[待填写]
- 课程：大模型基础与应用
- 学期：2024-2025学年

## 许可证

本项目仅用于教育目的。

