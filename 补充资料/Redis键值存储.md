# Redis键值存储

Redis 是一个基于内存的键值存储系统，它支持多种**丰富的数据类型**，但和 Python 中的原生类型（如字典、元组、布尔等）不完全对应。下面我们来详细解释：

注意：在 Redis 中，**所有的 key 都必须是字符串类型（binary-safe string）**。

---

## ✅ 一、Redis 支持的 **5 种核心数据类型**

Redis 的 **value** 可以是以下 5 种主要类型（key 始终是字符串）：

| 类型                             | 说明                                               | 对应场景                   |
| -------------------------------- | -------------------------------------------------- | -------------------------- |
| **String（字符串）**             | 最基础的类型，可以是文本、数字、JSON、二进制数据等 | 存储单个值，如缓存、计数器 |
| **List（列表）**                 | 有序、可重复的字符串列表                           | 消息队列、时间线（如微博） |
| **Set（集合）**                  | 无序、不重复的字符串集合                           | 标签、好友关系、去重       |
| **Hash（哈希）**                 | 类似“字段-值”映射表（field-value）                 | 存储对象（如用户信息）     |
| **Sorted Set（有序集合，ZSet）** | 带分数（score）的集合，按分排序                    | 排行榜、带权重的任务队列   |

> ⚠️ 注意：**Redis 没有原生的“元组、字典、布尔、浮点数”类型**，但可以通过 **String 或其他结构模拟**。

---

## 🔄 二、 Python 类型如何在 Redis 中表示？

| Python 类型         | 是否原生支持？      | 如何存储                                    | 建议方式                     |
| ------------------- | ------------------- | ------------------------------------------- | ---------------------------- |
| **字符串（str）**   | ✅ 是                | 直接存为 Redis String                       | `SET name "Alice"`           |
| **整数（int）**     | ✅ 是（作为 String） | 存为字符串，Redis 可做原子增减              | `INCR counter`               |
| **浮点数（float）** | ✅ 是（作为 String） | 存为字符串，如 `"3.14"`                     | `SET price 3.14`             |
| **布尔值（bool）**  | ❌ 否                | 用 `1` 表示 True，`0` 表示 False            | 存为整数 String              |
| **列表（list）**    | ✅ 是                | 使用 Redis **List** 类型                    | `LPUSH mylist "a" "b"`       |
| **字典（dict）**    | ❌ 否                | 用 Redis **Hash** 或 **String（JSON）**     | 推荐 JSON                    |
| **集合（set）**     | ✅ 是                | 使用 Redis **Set** 类型                     | `SADD tags "python" "redis"` |
| **元组（tuple）**   | ❌ 否                | 视为列表，用 **List** 或 **String（JSON）** | 存为 JSON 字符串             |

---

## 🧩 三、具体示例：如何存储常见类型

### 1. 字符串、整数、浮点数、布尔（都用 String）
```python
# Python
name = "Alice"
age = 25
price = 3.14
is_active = True

# Redis 存储（都用 String）
redis.set("user:name", "Alice")        # 字符串
redis.set("user:age", 25)             # 整数（字符串形式）
redis.set("user:price", 3.14)         # 浮点数
redis.set("user:active", 1 if is_active else 0)  # 布尔 → 0/1
```

---

### 2. 列表（用 Redis List）
```python
# Python
hobbies = ["reading", "coding", "music"]

# Redis 存储
redis.lpush("user:hobbies", *hobbies)
# 或
redis.rpush("user:hobbies", "reading", "coding", "music")
```

---

### 3. 字典（用 Hash 或 JSON）

#### ✅ 推荐方式：用 JSON 存为 String（灵活）
```python
import json

user = {"name": "Alice", "age": 25, "city": "Beijing"}
redis.set("user:1", json.dumps(user))
```

#### ✅ 或用 Hash（适合字段固定的对象）
```python
redis.hset("user:1", "name", "Alice")
redis.hset("user:1", "age", 25)
redis.hset("user:1", "city", "Beijing")
```

---

### 4. 集合（用 Redis Set）
```python
# Python
tags = {"python", "redis", "web"}

# Redis 存储
redis.sadd("post:1:tags", *tags)
```

---

### 5. 元组（视为不可变列表，用 JSON 存储）
```python
# Python
location = ("Beijing", 39.9, 116.4)  # 城市, 纬度, 经度

# Redis 存储
redis.set("user:location", json.dumps(location))
```

---

## 📌 四、重要说明

1. **Key 必须是字符串**  
   Redis 的 key 只能是二进制安全的字符串（通常用 UTF-8）。

2. **Value 是二进制安全的**  
   所有 value 都可以是字符串、JSON、MessagePack、Protobuf 等序列化后的字节流。

3. **Redis 没有“嵌套结构”**  
   不能直接存 `{"users": [{"name": "Alice"}]}` 这样的嵌套结构，需要用 **JSON 序列化后存为 String**。

4. **数值操作仅限 String 中的整数/浮点数**  
   Redis 支持 `INCR`、`DECR`、`INCRBYFLOAT`，但前提是 value 是合法数字字符串。

---

## ✅ 五、总结：Redis 数据类型映射表

| Python 类型           | Redis 存储方式        | 推荐方法                     |
| --------------------- | --------------------- | ---------------------------- |
| str, int, float, bool | String                | 直接存，bool 用 0/1          |
| list                  | List 或 String (JSON) | 简单列表用 List，复杂用 JSON |
| dict                  | Hash 或 String (JSON) | 字段固定用 Hash，灵活用 JSON |
| set                   | Set                   | 直接用 `SADD`                |
| tuple                 | String (JSON)         | 序列化后存储                 |
| nested structures     | String (JSON)         | 用 `json.dumps()`            |

---

## 💡 建议

> 在实际开发中，**推荐将复杂结构（如 dict、list、tuple）用 JSON 序列化后存为 Redis String**，简单结构（如计数器、标签）使用原生 List/Set/Hash。

