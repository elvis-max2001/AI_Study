import os
import os
# from base import Config, logger
# conf = Config()
# print(conf.REDIS_PORT)
# logger.info('这是岑氏')
# print("INSERT INTO jpkb (subject_name, question, answer) VALUES (%s, %s, %s)" % (1, 2, 3))
#
# print("它的名字是%s" % ("张三"))

# class Fun():
#     def _getdata(self):
#         return '你好'
#
# fun = Fun()
# print(fun._getdata())
#
# a = None
# if not a:
#     print('你好')
# query = "你好"
# query = 2
# if isinstance(query, int):
#     print('aaa')

# if query is str:
#     print('ndada')

# import numpy as np
#
# scores = [1.2, 2.4, 3.6]
# print(np.max(scores))
# result1 = np.exp(scores-np.max(scores))
# print(result1)
#
# print(result1/result1.sum())

# # 遍历指定目录及其子目录
# directory_path = "/Users/ligang/Desktop/EduRAG课堂资料/codes/integrated_qa_system/rag_qa/data/ai_data"
# for root, _, files in os.walk(directory_path):
#     print(f'root---》{root}')
#     print(f'_---》{_}')
#     print(f'files---》{files}')
#     print('*'*80)

# from datetime import datetime
# print(datetime.now())
# a = datetime.now().isoformat()
# b = datetime.fromisoformat(a)
# print(b)

a = []
b = [2, 3]
a.extend(b)
print(a)
