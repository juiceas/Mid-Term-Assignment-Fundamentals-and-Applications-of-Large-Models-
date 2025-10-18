# Overleaf XeLaTeX 编译说明

## 📋 快速步骤

### 1️⃣ 上传文件到Overleaf

1. 访问 [Overleaf](https://www.overleaf.com/)（免费账号即可）
2. 点击 "New Project" → "Blank Project"
3. 命名项目，例如：`Transformer期中作业`
4. 删除默认的 `main.tex` 文件
5. 点击 "Upload" 按钮，上传 `report.tex` 文件

### 2️⃣ 设置编译器为XeLaTeX

**重要**：必须使用XeLaTeX才能正确编译中文！

1. 点击左上角的 "Menu" 按钮（三条横线图标）
2. 找到 "Compiler" 选项
3. 从下拉菜单中选择 **"XeLaTeX"**
4. 点击菜单外的任意位置关闭菜单

### 3️⃣ 编译文档

1. 点击绿色的 "Recompile" 按钮
2. 等待编译完成（第一次可能需要1-2分钟）
3. 右侧会显示生成的PDF预览

### 4️⃣ 下载PDF

1. 点击右上角的 "Download PDF" 按钮
2. PDF文件会下载到您的电脑

---

## ✅ 我已经做的优化

### 1. 包加载顺序优化

```latex
% ✓ 正确的顺序
\usepackage{xcolor}      % 必须在listings之前
\usepackage{listings}
\usepackage{hyperref}    % 通常放在最后
```

### 2. 代码样式优化

- 添加了 `inputencoding=utf8` 支持中文注释
- 优化了代码框样式
- 增强了关键字高亮

### 3. 图片处理

- 将图片引用注释掉，避免缺少图片文件的错误
- 提供了文字说明替代

### 4. 中文支持

- 使用 `ctexart` 文档类，完美支持中文
- XeLaTeX会自动使用系统中文字体

---

## 🎨 个性化修改

### 修改个人信息

找到第49行：

```latex
\author{学生姓名\thanks{学号：XXXXXXXXXX，邮箱：xxx@xxx.edu.cn}}
```

改为：

```latex
\author{张三\thanks{学号：2021001234，邮箱：zhangsan@example.edu.cn}}
```

### 修改日期

默认使用 `\today`（今天的日期），如果想固定日期：

```latex
\date{2025年10月17日}
```

---

## 🔧 常见问题解决

### ❌ 问题1：编译出现 "Font not found" 错误

**原因**：XeLaTeX找不到中文字体

**解决方案**：
- Overleaf通常已经包含中文字体，直接使用XeLaTeX即可
- 如果仍有问题，可以在文档开头添加：

```latex
\setCJKmainfont{Noto Serif CJK SC}  % 使用Overleaf自带的中文字体
```

### ❌ 问题2：图片无法显示

**原因**：缺少图片文件

**解决方案**：
1. **方案A（推荐）**：暂时使用文字说明（已在模板中实现）
2. **方案B**：上传图片文件
   - 运行训练生成 `results/training_curves.png`
   - 在Overleaf中点击 "Upload" 上传图片
   - 取消注释图片代码

### ❌ 问题3：参考文献格式问题

**原因**：BibTeX配置

**解决方案**：
- 当前使用的是 `\begin{thebibliography}` 环境，无需额外配置
- 如果想使用BibTeX，需要改用 `.bib` 文件

### ❌ 问题4：代码中的中文显示异常

**原因**：编码问题

**解决方案**：
- 确保使用 XeLaTeX 编译器
- 代码中已设置 `inputencoding=utf8`

---

## 📝 插入训练结果图片

如果您已经运行了训练并生成了结果图片：

### 步骤1：上传图片到Overleaf

1. 在Overleaf项目中，点击左上角的 "Upload" 按钮
2. 选择以下图片文件上传：
   - `results/training_curves.png`（训练曲线）
   - 其他图片（如果有）

### 步骤2：修改report.tex

找到第531-540行（训练曲线图部分）：

```latex
\begin{figure}[H]
    \centering
    \fbox{\parbox{0.8\textwidth}{\centering 
    [此处应插入实际训练曲线图：results/training\_curves.png]\\
    \vspace{2cm}
    包含4个子图：训练/验证损失、训练/验证困惑度、学习率曲线、验证损失详细图
    }}
    \caption{基础模型训练曲线}
    \label{fig:training_curves}
\end{figure}
```

改为：

```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.95\textwidth]{training_curves.png}
    \caption{基础模型训练曲线（包含4个子图：训练/验证损失、训练/验证困惑度、学习率曲线、验证损失详细图）}
    \label{fig:training_curves}
\end{figure}
```

---

## 🎯 完整编译流程

### 完整流程（从零开始）

```bash
# 本地操作

# 1. 运行训练（可选）
python src/train.py

# 2. 准备文件
# - report.tex（主文档）
# - training_curves.png（如果已生成）

# Overleaf操作

# 3. 上传到Overleaf
#    - 上传 report.tex
#    - 上传图片（如果有）

# 4. 设置编译器为 XeLaTeX

# 5. 点击 Recompile

# 6. 下载生成的PDF
```

---

## 📊 优化前后对比

| 项目 | 优化前 | 优化后 |
|-----|--------|--------|
| 编译器设置 | 需要手动设置 | 已说明 |
| 包加载顺序 | 可能有冲突 | ✅ 已优化 |
| 中文支持 | 基本支持 | ✅ 完美支持 |
| 代码高亮 | 基本样式 | ✅ 增强样式 |
| 图片处理 | 可能报错 | ✅ 容错处理 |
| hyperref配置 | 重复定义 | ✅ 统一配置 |

---

## 💡 高级技巧

### 1. 自定义字体大小

```latex
% 在导言区添加
\usepackage{setspace}
\setstretch{1.5}  % 1.5倍行距
```

### 2. 调整页边距

```latex
% 修改第17行
\geometry{left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}

% 改为更窄的边距
\geometry{left=2cm,right=2cm,top=2cm,bottom=2cm}
```

### 3. 添加页眉页脚

```latex
% 在导言区添加
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhead[L]{Transformer实现}
\fancyhead[R]{大模型期中作业}
\fancyfoot[C]{\thepage}
```

### 4. 优化表格显示

如果表格太宽，可以使用：

```latex
\begin{table}[H]
\centering
\small  % 缩小字体
\begin{tabular}{...}
...
\end{tabular}
\end{table}
```

---

## 🚨 注意事项

### ⚠️ 必须设置XeLaTeX

- **不要使用pdfLaTeX**，会导致中文无法显示
- **不要使用LuaLaTeX**，可能有兼容性问题
- **必须使用XeLaTeX**

### ⚠️ 首次编译较慢

- 第一次编译需要下载包和字体，可能需要1-2分钟
- 后续编译会快很多（10-30秒）

### ⚠️ 图片文件名

- 避免使用中文文件名
- 避免使用空格
- 推荐：`training_curves.png`（✓）
- 不推荐：`训练曲线.png`（✗）

### ⚠️ 编译次数

- 第一次编译可能看不到目录和引用
- **至少编译2次**才能看到完整效果
- 参考文献需要编译3次

---

## ✅ 检查清单

编译前请确认：

- [ ] 已将 `report.tex` 上传到Overleaf
- [ ] 编译器设置为 **XeLaTeX**
- [ ] 已修改个人信息（姓名、学号）
- [ ] 如果有图片，已上传并修改图片引用
- [ ] 点击 "Recompile" 至少2次
- [ ] PDF正常显示中文
- [ ] 所有表格和公式正常显示

---

## 🎉 完成后

编译成功后，您会得到：

- ✅ 一份完整的PDF报告（约10-15页）
- ✅ 包含完整的数学公式和推导
- ✅ 包含代码示例
- ✅ 包含实验结果表格
- ✅ 包含参考文献

---

## 📞 需要帮助？

如果遇到问题：

1. **检查编译器**：确认是XeLaTeX
2. **查看错误日志**：点击 "Logs and output files"
3. **重新上传**：删除项目重新上传
4. **使用模板**：Overleaf有中文LaTeX模板可参考

---

**祝编译顺利！** 🚀

如果一切正常，您应该能看到一份漂亮的中文学术报告PDF！

