 To Do:
 
 DeepSeek Engram 这篇论文，以及它背后的两条技术支线：Memory Network 和 N-gram。理解了这些背景工作，再看 Engram 就会发现水到渠成。

📚 本期串讲的论文/背景:

【Memory 支线】
• Facebook 2019 - Language Models as Knowledge Bases
• Google 2020 - T5 作为 Knowledge Base
• 2021 - Transformer FFN 层是 Key-Value Memory
• Microsoft 2022 - Knowledge Neurons
• Facebook 2019 - Product Key Memory (PKM)
• Meta - Memory Layer 扩展到 128B 参数
• DeepMind 2022 - Retrieval-Enhanced Transformer (RETRO)
• Google 2023 - External Memory 提升模型能力

【N-gram 支线】
• 传统 N-gram 语言模型基础
• Google 2022 - N-Grammer：用 N-gram Embedding 增强 Transformer
• Google 2025 - Scaling Embedding Layer

【DeepSeek Engram】
• 核心思想：用 N-gram Embedding + Hash 查表实现高效知识检索
• 技术要点：Sparsity、Gating 机制、Memory Hierarchy
• 与 MoE 的关系：Engram 是 MoE 的补充

🎯 核心观点:
1. Transformer 的 FFN 层本质是一个 Key-Value Memory
2. Sparsity 是打破「不可能三角」的关键（Performance / Compute / Model Size）
3. 通过 Hash 查表实现 O(1) 复杂度的 N-gram 检索
4. Engram 让模型不用「计算」就能「记住」常识知识
5. DeepSeek 的工作是前人研究的集大成者

