
# 资源
[Github链接](https://github.com/yuanzhoulvpi2017/zero_nlp/tree/main/train_llava)


**LLaVA** (Large Language-and-Vision Assistant) 是一个开源的**多模态大语言模型 (MLLM)**。简单来说，它通过极其简洁的架构，将“视觉编码器”和“大语言模型”连接起来，让 LLM 具备了看图、理解图并进行对话的能力。



### 1. 核心架构：简单的“连接器” (Connector)

LLaVA 的核心思想非常直接：**不要重新从头训练一个大模型，而是把现有的最强组件“缝合”在一起。**

它主要由三部分组成：

* **视觉编码器 (Vision Encoder):** 使用预训练好的 **CLIP (ViT-L/14)**。它的作用是将图片转换成机器能懂的“视觉特征向量”。
* **大语言模型 (LLM):** 使用 **Vicuna** (基于 Llama 微调的模型)。它负责逻辑推理和文本生成。
* **连接器 (Projection Layer):** **这是 LLaVA 的关键**。它仅仅是一个简单的**线性层 (Linear Layer)** 或 **MLP**。
* **原理：** 把 CLIP 提取出的视觉特征向量，通过这个线性层，“投影”到 LLM 的词嵌入空间 (Word Embedding Space) 中。
* **效果：** 对 LLM 来说，图片特征被转换成了它能看懂的 token embedding，就像看到了这图片对应的“文字描述”一样。



### 2. 关键创新：视觉指令微调 (Visual Instruction Tuning)

LLaVA 最大的贡献在于它证明了**数据质量**比模型复杂度更重要。

* **传统做法：** 使用海量的图文对（image-text pairs）进行训练，但这通常只能做简单的分类或简短描述。
* **LLaVA 的做法：** 既然 LLM 需要指令才能更好地工作，LLaVA 团队利用纯文本的 GPT-4，将传统的图文数据集改写成了**对话格式**的数据（即：视觉指令数据）。
* 这让模型不仅能“认出图里有什么”，还能学会“根据图片回答复杂问题”或“根据图片进行推理”。



### 3. 为什么 LLaVA 很重要？

在 LLaVA 出现之前，多模态模型通常需要昂贵的端到端训练。LLaVA 证明了：

1. **训练成本极低：** 只需要微调那个简单的“连接器”和少量的 LLM 参数，就可以获得 SOTA (State-of-the-Art) 的效果。
2. **开源生态基石：** 由于架构简单、效果好，LLaVA 成了后来很多多模态模型的基石（Base Model），许多后续工作（如 LLaVA-1.5, LLaVA-NeXT）都是在此基础上改进的。

