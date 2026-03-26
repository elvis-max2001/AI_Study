## 什么是 `BGEM3EmbeddingFunction`？

`BGEM3EmbeddingFunction` 是 **Milvus 向量数据库生态** 中的一个类，用于将文本转换为多模态嵌入向量，它封装了 **BAAI（智源研究院）发布的 BGE-M3 模型** 的推理能力。

它来自库：`milvus-model`（原 `milvus-sdk` 的扩展），用于与 Milvus / Zilliz Cloud 等向量数据库无缝集成。

### ✅ 安装方式

```python
pip install milvus-model
```

### ✅ 基本使用示例

```python
from milvus_model.hybrid import BGEM3EmbeddingFunction

ef = BGEM3EmbeddingFunction()

texts = ["什么是人工智能？", "iPhone 价格是多少？"]
embeddings = ef(texts)

print(embeddings.keys())  # 输出:dict_keys(['dense', 'sparse'])
```

返回三种向量：

- `dense`: 稠密向量（用于语义相似度）
- `sparse`: 稀疏向量（用于关键词匹配）

------

## 🔍 核心能力：一个模型，两种检索模式

| 检索模式         |               |                                            |
| ---------------- | ------------- | ------------------------------------------ |
| Dense Retrieval  | `dense_vecs`  | 捕捉语义相似性（“猫” ≈ “猫咪”）            |
| Sparse Retrieval | `sparse_vecs` | 模拟加权关键词匹配（类似 BM25 + 语义扩展） |