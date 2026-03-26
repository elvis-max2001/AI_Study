

# argparse基本使用

> `argparse` 是 Python 内置模块，用于轻松编写用户友好的命令行接口。  
> 它能自动解析命令行参数、生成帮助信息、进行类型检查和错误处理。

---

## 🧩 一、基本结构（你的代码解析）

你写的这段代码非常标准：

```python
import argparse

parser = argparse.ArgumentParser(description="EduRAG System Main Entry Point")
parser.add_argument('--data-processing', action='store_true', help='Run in data processing mode instead of query mode.')
parser.add_argument('--data-dir', type=str, default='./data', help='Path to the data directory.')
args = parser.parse_args()

main(query_mode=(not args.data_processing), directory_path=args.data_dir)
```

我们来逐行解释。

---

### 1. 创建解析器

```python
parser = argparse.ArgumentParser(description="EduRAG System Main Entry Point")
```

- `ArgumentParser` 是主类
- `description`：在 `--help` 时显示的描述信息

---

### 2. 添加参数

```python
parser.add_argument('--data-processing', action='store_true', help='...')
```

| 参数                  | 含义                                                  |
| --------------------- | ----------------------------------------------------- |
| `--data-processing`   | 可选参数（以 `--` 开头）                              |
| `action='store_true'` | 如果命令行中出现这个参数，值为 `True`；否则为 `False` |
| `help`                | 帮助文档，`--help` 时显示                             |

👉 使用方式：
```bash
python main.py --data-processing        # args.data_processing = True
python main.py                          # args.data_processing = False
```

---

```python
parser.add_argument('--data-dir', type=str, default='./data', help='...')
```

| 参数               | 含义                 |
| ------------------ | -------------------- |
| `--data-dir`       | 可选参数             |
| `type=str`         | 要求输入是字符串类型 |
| `default='./data'` | 如果没提供，默认值   |
| `help`             | 帮助说明             |

👉 使用方式：
```bash
python main.py --data-dir ./my_data
```

---

### 3. 解析参数

```python
args = parser.parse_args()
```

这行代码会：
- 读取 `sys.argv`（命令行输入）
- 解析成一个对象 `args`
- 你可以通过 `args.data_processing`、`args.data_dir` 访问

---

### 4. 传递给主函数

```python
main(query_mode=(not args.data_processing), directory_path=args.data_dir)
```

- 如果 `--data-processing` 出现 → `args.data_processing=True` → `query_mode=False`
- 否则 → `query_mode=True`

