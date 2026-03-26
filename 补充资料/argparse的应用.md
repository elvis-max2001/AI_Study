# argparse的应用

`argparse` 是 Python 标准库中用于解析命令行参数和选项的模块，使用它可以让脚本更灵活、更易于使用。下面是一个简单的使用说明，帮助你快速上手 `argparse`。

---

### 一、基本结构

```python
import argparse

# 1. 创建解析器
parser = argparse.ArgumentParser(description='简要描述这个脚本的功能')

# 2. 添加参数
parser.add_argument('input', help='输入文件路径')  # 位置参数
parser.add_argument('--output', help='输出文件路径')  # 可选参数
parser.add_argument('--verbose', action='store_true', help='是否输出详细信息')

# 3. 解析参数
args = parser.parse_args()

# 4. 使用参数
print(f"输入文件: {args.input}")
if args.output:
    print(f"输出文件: {args.output}")
if args.verbose:
    print("详细模式已开启")
```

---

### 二、常见参数类型

#### 1. 位置参数（必须提供）
```python
parser.add_argument('filename', help='输入文件名')
```
使用方式：`python script.py myfile.txt`

#### 2. 可选参数（以 `--` 开头）
```python
parser.add_argument('--name', help='用户姓名')
```
使用方式：`python script.py --name Alice`

#### 3. 带默认值的参数
```python
parser.add_argument('--count', default=1, type=int, help='重复次数（默认1）')
```

#### 4. 布尔开关（使用 action='store_true'）
```python
parser.add_argument('--verbose', action='store_true', help='启用详细输出')
```
- 如果命令行中包含 `--verbose`，`args.verbose` 为 `True`，否则为 `False`。

#### 5. 限制取值范围（choices）
```python
parser.add_argument('--mode', choices=['fast', 'slow'], default='fast', help='运行模式')
```

#### 6. 类型转换（type）
```python
parser.add_argument('--age', type=int, help='年龄')
```

---

### 三、完整示例

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description='一个简单的示例程序')

    parser.add_argument('input', help='输入文件路径')
    parser.add_argument('--output', required=False, default='output.txt', help='输出文件路径')
    parser.add_argument('--verbose', action='store_true', help='是否打印详细信息')
    parser.add_argument('--times', type=int, default=1, help='重复处理次数')

    args = parser.parse_args()

    if args.verbose:
        print(f"正在处理 {args.input} -> {args.output}，重复 {args.times} 次")

    for i in range(args.times):
        print(f"处理中... {i+1}/{args.times}")

if __name__ == '__main__':
    main()
```

使用示例：
```bash
python script.py data.txt --output result.txt --verbose --times 3
```

---

### 四、常用技巧

- `required=True`：强制某个可选参数必须提供。
- `nargs='*'`：接受多个值（如 `--files a.txt b.txt c.txt`）。
- `help`：帮助信息，`--help` 会自动显示。
- `epilog`：在帮助末尾添加额外信息。

```python
parser.add_argument('--files', nargs='*', help='多个输入文件')
```

---

### 五、查看帮助

运行：
```bash
python script.py --help
```
会自动输出你定义的所有参数说明。

---

✅ 总结：`argparse` 让命令行脚本更专业，只需三步：创建解析器 → 添加参数 → 解析使用。推荐在所有命令行工具中使用。