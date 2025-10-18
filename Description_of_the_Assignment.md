# Fundamentals and Applications of Large Models
## Mid-Term Assignment

**Title**
**Student**: student name
**Student ID**: ID

---

### 1 作业说明

#### 1.1 作业总体说明:
[cite_start]提交内容:中文、不少于5页、latex编译成pdf [cite: 9]。

* [cite_start]实现并撰写一篇报告:包含引言、相关工作介绍、提供清晰的数学推导、伪代码 [cite: 10][cite_start]。实现 multi-head self-attention position-wise FFN、残差+Layer Norm、位置编码等 [cite: 10][cite_start]。完成后分数 60-70分 [cite: 10]。
* [cite_start]手工搭建一个 Transformer,在小规模文本建模任务上训练并做消融实验,包含框架说明、关键实现片段、实验设置、结果图表)(如果只有 encoder block 70-80分,加 decoder block 80-90分) [cite: 11]。
* [cite_start]代码需开源并附上运行说明(10分) [cite: 12]。

#### 1.2 代码开源要求
* [cite_start]一个 Git 仓库(GitHub link) 包含:src/、requirements.txt、README.md scripts/run.sh [cite: 14]。
* [cite_start]results/放训练曲线图与表格 [cite: 15]。
[cite_start]在README 写清楚运行命令与硬件要求,给出重现实验的exact 命令行(含随机种子) [cite: 16]。

#### 1.3 小数据集验证
* [cite_start]基础:能在小数据集上跑通训练(loss下降);代码(含README) [cite: 18]。
* [cite_start]进阶:实现训练稳定性技巧(学习率调度、梯度裁剪、AdamW)、参数统计、模型保存/加载、训练 曲线可视化 [cite: 19]。
* [cite_start]挑战:实现 decoder、实现相对位置编码、实现稀疏/线性注意力或并行化优化、做规模/超参敏感性分析、在更大数据上微调或蒸馏 [cite: 20]。

#### 1.4 数据集合建议
* [cite_start]验证数据集合可以自由选择,建议数据集合小一些 [cite: 22][cite_start]。在报告中将数据集介绍写明并附链接,在代码仓库中提供数据集压缩包 [cite: 22]。
* [cite_start]Language Modeling Tasks (Encoder-only Transformer): Exemplifying some datasets suitable for training small-scale encoder-only Transformers for language modeling tasks[cite: 23]. [cite_start]Each dataset is lightweight and accessible via the Hugging Face Datasets platform[cite: 24].
* [cite_start]Sequence-to-Sequence Tasks (Encoder-Decoder Transformer): Exemplifying some datasets are commonly used for sequence-to-sequence learning tasks such as machine translation and summarization[cite: 25]. [cite_start]They provide paired input-output text samples suitable for training encoder-decoder Transformer architectures[cite: 26].

[cite_start]November 2025 [cite: 27]

---

| Dataset | Task Type | Typical Size | Hugging Face Link | Notes |
| :--- | :--- | :--- | :--- | :--- |
| WikiText-2 | Word-level LM | ~2M tokens | wikitext | Classic small dataset; easy to tokenize and train small models. |
| Penn Treebank (PTB) | Word-level LM | ~1M tokens | ptb\_text\_only | Extremely compact; good for debugging models. |
| Tiny Shakespeare | Character-level LM | ~1 MB | tiny\_shakespeare | Ideal for first training test; converges quickly. |
| AG News Subset | Text classification | ~120K samples | ag\_news | Can be treated as classification if you prefer supervised fine-tuning. |

[cite_start]**表 1: Language modeling and classification datasets for encoder-only Transformer training.** [cite: 29]

| Dataset | Task Type | Typical Size | Hugging Face Link | Notes |
| :--- | :--- | :--- | :--- | :--- |
| IWSLT2017 (EN DE) | Machine Translation | ~200K pairs | iwslt2017 | Excellent for small-scale MT: official benchmark. |
| TED Talks (Multi-lingual) | Translation/Paraphrase | ~100K pairs | ted talks iwslt | Small and language-diverse. |
| Gigaword Subset | Summarization | ~200K pairs | gigaword | Works well for headline generation. |
| CNN/DailyMail (trimmed) | Summarization | ~300K pairs | cnn\_\_dailymail | Use subset of 10K-20K for local training. |

[cite_start]**表2: Sequence-to-sequence datasets for encoder-decoder Transformer training.** [cite: 31]

### 1 Introduction
[cite_start]Introduce the background and motivation of the Transformer architecture[cite: 33]. [cite_start]Explain the purpose of this assignment and summarize the main contributions of your implementation[cite: 34].
* [cite_start]What problem does the Transformer solve? [cite: 35]
* [cite_start]Why is it important to build it from scratch? [cite: 36]
* [cite_start]What are your goals (e.g., understanding self-attention, reproducing training behavior)? [cite: 37]

### 2 Related Work
[cite_start]Briefly review the Transformer model and related architectures (e.g., different attention mechanisms)[cite: 39]. [cite_start]Cite the original Transformer paper [1] and optionally more recent improvements[cite: 40].

### 3 Model Architecture and Mathematical Derivation
[cite_start]Provide the theoretical foundation and equations behind each module[cite: 42]. [cite_start]All subsections are examples[cite: 42].

---

#### 3.1 Scaled Dot-Product Attention
[cite_start]Present the attention formula: [cite: 45]
[cite_start]$Attention(Q,K,V)=softmax(\frac{QK^{T}}{\sqrt{d_{k}}})V$ [cite: 48]
[cite_start]Explain all symbols and shapes[cite: 46].

#### 3.2 Multi-Head Attention
[cite_start]Derive how multiple attention heads are combined[cite: 49]. [cite_start]Explain why multi-head improves representation capacity[cite: 49].

#### 3.3 Position-Wise Feed-Forward Network
[cite_start]Define the two-layer MLP applied independently to each token[cite: 51].

#### 3.4 Residual Connections and Layer Normalization
[cite_start]Discuss the role of residual connections and normalization in stabilizing training[cite: 53].

#### 3.5 Positional Encoding
[cite_start]Describe sinusoidal or learned positional encodings[cite: 55]. [cite_start]Provide the mathematical formula[cite: 55].

### 4 Implementation Details
[cite_start]Describe how you implemented the model and training pipeline[cite: 57].
* [cite_start]Framework and language (e.g., PyTorch) [cite: 58]
* [cite_start]Implementation of attention, FFN, normalization [cite: 59]
* [cite_start]Masking (padding mask, future mask if decoder) [cite: 60]
* [cite_start]Model hyperparameters [cite: 61]
* [cite_start]Pseudocode or key code snippets [cite: 62]

```python
def scaled_dot_product_attention(Q, K, V, mask=None):
    d_k = Q.size(-1)
    scores = Q @ K.transpose(-2, -1) / math.sqrt(d_k)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
    attn = torch.softmax(scores, dim=-1)
    return attn @ V, attn
```
**Listing 1: Simplified self-attention implementation in PyTorch**

### 5 Experimental Setup
Describe the dataset, training setup, and evaluation metrics.
* [cite_start]Dataset (e.g., WikiText-2, small text corpus) [cite: 74]
* [cite_start]Data preprocessing [cite: 75]
* [cite_start]Training hyperparameters: batch size, learning rate, optimizer, scheduler, number of epochs [cite: 76]
* [cite_start]Evaluation metrics (loss, perplexity, accuracy) [cite: 77]

[cite_start]Provide a clear hyperparameter table: [cite: 78]

[cite_start]**表3: Hyperparameter Settings** [cite: 79]

| Parameter | Value |
| :--- | :--- |
| Embedding dimension | 128 |
| Number of heads | 4 |
| Feed-forward dimension | 512 |
| Number of layers | 2 |
| Batch size | 32 |
| Learning rate | 3e-4 |
| Optimizer | Adam |

[cite_start][cite: 80]

### 6 Results and Analysis
[cite_start]Present quantitative and qualitative results. [cite: 82]
* [cite_start]Training and validation curves [cite: 83]
* [cite_start]Sample predictions or generated text [cite: 84]
* [cite_start]Comparison between variants (e.g., different number of heads) [cite: 85]
* [cite_start]Ablation study: what happens if positional encoding is removed? [cite: 86]
[cite_start]Discuss findings and insights. [cite: 87]

### 7 Reproducibility and Code Structure
[cite_start]Explain how to reproduce the results. [cite: 89]
* [cite_start]github link [cite: 90]
* [cite_start]Dependencies and environment setup [cite: 91]
* [cite_start]Folder structure of your code repository [cite: 92]
* [cite_start]Command line examples [cite: 93]
* [cite_start]Expected runtime and hardware used [cite: 94]

---

Example:
```bash
$conda create -n transformer python=3.10$ pip install torch matplotlib
$ python train.py --config configs/base.yaml
```
**Listing 2: Example training command**

### 8 Conclusion and Future Work
Summarize what you have implemented and learned. Discuss possible extensions:
* [cite_start]Adding a decoder for sequence-to-sequence tasks [cite: 103]
* [cite_start]Trying relative positional encoding [cite: 104]
* [cite_start]Comparing with official PyTorch implementation [cite: 105]

### 参考文献
[1] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. [cite_start]Advances in neural information processing systems, 30, 2017. [cite: 107, 108]
