# Trainer和TrainingArguments如何使用

在 Hugging Face 的 `transformers` 库中，`Trainer` 和 `TrainingArguments` 是用于训练和微调预训练模型（如 BERT、RoBERTa、T5 等）的核心类。它们大大简化了训练流程，无需手动编写训练循环、梯度更新、分布式训练等底层逻辑。

---

## 一、`TrainingArguments` 类

`TrainingArguments` 用于配置训练过程中的各种超参数和训练选项。

### 基本用法

```python
from transformers import TrainingArguments

training_args = TrainingArguments(
    output_dir="./results",              # 模型输出和日志保存路径
    num_train_epochs=3,                 # 训练轮数
    per_device_train_batch_size=16,     # 每个设备的训练 batch size
    per_device_eval_batch_size=64,      # 每个设备的评估 batch size
    warmup_steps=500,                   # 学习率预热步数
    weight_decay=0.01,                  # 权重衰减
    logging_dir="./logs",               # 日志目录（TensorBoard 使用）
    logging_steps=10,                   # 每多少步记录一次日志
    evaluation_strategy="steps",        # 评估策略：steps 或 epoch
    eval_steps=500,                     # 每多少步评估一次
    save_strategy="steps",              # 保存策略
    save_steps=500,                     # 每多少步保存一次模型
    learning_rate=5e-5,                 # 学习率
    save_total_limit=2,                 # 最多保存几个 checkpoint
    load_best_model_at_end=True,        # 训练结束时加载最优模型
    metric_for_best_model="accuracy",   # 选择最优模型的指标
    greater_is_better=True,             # 指标越大越好
    report_to="none",                   # 不使用 wandb 或 tensorboard 等（可选 "tensorboard", "wandb"）
    fp16=True,                          # 使用混合精度训练（GPU 支持时）
    gradient_accumulation_steps=2,      # 梯度累积步数，模拟更大 batch
    seed=42,                            # 随机种子
)
```

### 主要参数解释

| 参数                          | 说明                                          |
| ----------------------------- | --------------------------------------------- |
| `output_dir`                  | 模型、检查点、日志的保存路径                  |
| `num_train_epochs`            | 总共训练多少轮                                |
| `per_device_train_batch_size` | 每个 GPU/CPU 的训练 batch 大小                |
| `per_device_eval_batch_size`  | 每个设备的评估 batch 大小                     |
| `learning_rate`               | 优化器学习率                                  |
| `warmup_steps`                | 学习率预热步数，前几步线性增长                |
| `weight_decay`                | AdamW 优化器的权重衰减                        |
| `logging_steps`               | 每几步记录一次训练日志                        |
| `evaluation_strategy`         | 评估时机：`"no"`, `"steps"`, `"epoch"`        |
| `eval_steps`                  | 若使用 steps 策略，每几步评估一次             |
| `save_strategy`               | 模型保存策略                                  |
| `save_steps`                  | 保存间隔步数                                  |
| `save_total_limit`            | 保留最多几个 checkpoint，自动删除旧的         |
| `load_best_model_at_end`      | 训练结束后加载验证集上表现最好的模型          |
| `metric_for_best_model`       | 判断“最好模型”的指标（如 accuracy, loss, f1） |
| `greater_is_better`           | 该指标是否越大越好                            |
| `fp16`                        | 是否使用半精度（16位）加速训练（需 GPU 支持） |
| `gradient_accumulation_steps` | 梯度累积步数，用于模拟更大的 batch size       |
| `seed`                        | 随机种子，保证实验可复现                      |
| `report_to`                   | 集成日志工具，如 `"tensorboard"`, `"wandb"`   |

---

## 二、`Trainer` 类

`Trainer` 是一个高级训练接口，封装了训练、评估、预测等流程。

### 基本用法

```python
from transformers import Trainer, AutoModelForSequenceClassification, AutoTokenizer
import torch

# 1. 加载模型和分词器
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# 2. 准备数据集（示例使用 Dataset 对象）
from datasets import Dataset

train_data = {
    "text": ["I love this movie", "This is terrible", ...],
    "label": [1, 0, ...]
}
train_dataset = Dataset.from_dict(train_data)

# 定义 tokenize 函数
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

train_dataset = train_dataset.map(tokenize_function, batched=True)

# 3. 定义 compute_metrics 函数（用于评估）
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    accuracy = accuracy_score(labels, predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average="binary")
    return {
        "accuracy": accuracy,
        "f1": f1,
        "precision": precision,
        "recall": recall
    }

# 4. 创建 Trainer
trainer = Trainer(
    model=model,                         # 要训练的模型
    args=training_args,                  # 训练参数
    train_dataset=train_dataset,         # 训练数据集
    eval_dataset=eval_dataset,           # 验证数据集（可选）
    tokenizer=tokenizer,                 # 分词器（用于动态 padding）
    compute_metrics=compute_metrics,     # 评估函数
)

# 5. 开始训练
trainer.train()

# 6. 评估
results = trainer.evaluate()
print(results)

# 7. 保存模型
trainer.save_model("./fine_tuned_model")
```

---

## 三、关键组件详解

### 1. 数据集格式要求

- 使用 `datasets.Dataset` 或 `torch.utils.data.Dataset`。
- 数据需包含 `input_ids`, `attention_mask`, `labels` 等字段（`Trainer` 自动识别）。
- 推荐使用 `map()` 进行预处理（如 tokenize）。

### 2. `compute_metrics` 函数

- 输入为 `(logits, labels)` 元组。
- 返回一个字典，包含评估指标（如 `{"accuracy": 0.95}`）。
- `Trainer` 会自动在 `evaluate()` 和日志中记录这些指标。

### 3. 动态 Padding（推荐使用 `DataCollator`）

```python
from transformers import DataCollatorWithPadding

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,        # 自动 padding batch
    compute_metrics=compute_metrics,
)
```

> 说明：如果不使用 `data_collator`，需在 `tokenize` 时固定长度（`padding="max_length"`）；使用 `DataCollatorWithPadding` 可动态 padding，更高效。

---

## 四、完整训练流程总结

1. ✅ 加载预训练模型和 tokenizer
2. ✅ 准备数据集（`Dataset` 格式）
3. ✅ tokenize 并格式化为模型输入
4. ✅ 定义 `TrainingArguments`
5. ✅ 定义 `compute_metrics` 函数
6. ✅ 实例化 `Trainer`
7. ✅ 调用 `trainer.train()` 开始训练
8. ✅ 调用 `trainer.evaluate()` 评估
9. ✅ 保存模型和 tokenizer

---

## 五、高级技巧

### 1. 使用 TensorBoard 查看训练日志

```python
training_args = TrainingArguments(
    ...
    logging_dir="./logs",
    report_to="tensorboard",
)
```

然后运行：
```bash
tensorboard --logdir ./logs
```

### 2. 早停（Early Stopping）

需结合 `EarlyStoppingCallback`：

```python
from transformers import EarlyStoppingCallback

trainer = Trainer(
    ...
    callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
)
```

当验证指标连续 3 次未提升时停止训练。

---

## 六、注意事项

- `Trainer` 默认使用 `AdamW` 优化器和线性学习率预热。
- 确保 `labels` 字段在 dataset 中命名为 `"labels"`（标准命名）。
- 多卡训练自动支持（通过 `--local_rank` 或 `deepspeed` 配置）。
- 推荐使用 `Trainer` + `TrainingArguments` 快速实验，避免重复造轮子。

---

## 总结

| 类                  | 作用                       |
| ------------------- | -------------------------- |
| `TrainingArguments` | 配置训练超参数和行为       |
| `Trainer`           | 封装训练、评估、预测全流程 |

> ✅ 官方文档：https://huggingface.co/docs/transformers/main_classes/trainer