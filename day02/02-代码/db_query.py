# -*-coding:utf-8-*-
from pymilvus import MilvusClient, DataType, AnnSearchRequest, RRFRanker, WeightedRanker
import random

#todo:1. 操作数据库
def operate_db():
    # 如果没有docker，也没有后端启动Milvus服务端的情况下
    # client = MilvusClient(uri='ai_milvus.db')
    # 如果uri为链接地址，代表Milvus属于单机服务，需要开启Milvus后台服务操作
    client = MilvusClient(uri="http://localhost:19530")
    # print(f'client-->{client}')
    # 查看库中有多少个databases;
    databases = client.list_databases()
    print(f'databases--》{databases}')
    # 先判断数据库是否存在，如果不存在，创建，否则直接使用
    if "milvus_demo" not in databases:
        client.create_database(db_name="milvus_demo")
    else:
        client.using_database(db_name='milvus_demo')

    return client
client = operate_db()
# todo:2. 复杂查询
def complex_query():
    # # 定义schema

    # schema = client.create_schema(enable_dynamic_field=False)
    # schema.add_field(field_name='film_id', datatype=DataType.INT64, is_primary=True)
    # schema.add_field(field_name='filmVector', datatype=DataType.FLOAT_VECTOR, dim=5) # 向量字段
    # schema.add_field(field_name="posterVector", datatype=DataType.FLOAT_VECTOR, dim=5) # 向量字段
    # # #
    # # 定义索引
    # index_params = client.prepare_index_params()
    # index_params.add_index(field_name='filmVector', index_type="IVF_FLAT",
    #                        metric_type="L2", params={"nlist": 128})
    # index_params.add_index(field_name='posterVector', index_type="",
    #                        metric_type="COSINE")
    #
    # # 创建集合
    # client.create_collection(collection_name='demo_v3', schema=schema, index_params=index_params)
    #
    # # 向量库中插入实体
    # entities = []
    # for _ in range(1000):
    #     # 构造实体
    #     film_id = random.randint(1, 10000)
    #     film_vector = [random.random() for _ in range(5)]
    #     poster_vector = [random.random() for _ in range(5)]
    #     entity = {"film_id": film_id, "filmVector": film_vector, "posterVector": poster_vector}
    #     entities.append(entity)
    # print(f'实体的数量--》{len(entities)}')
    # print(f'实体的数量--》{entities[0]}')
    # #  将上述数据插入到集合中
    # client.upsert(collection_name='demo_v3', data=entities)
    # 查询向量
    query_filmVector = [[0.8896863042430693, 0.370613100114602, 0.23779315077113428, 0.38227915951132996, 0.5997064603128835]]
    # 第一个向量字段的检索
    search_param_1 = {"data": query_filmVector, # 请求查询的向量数据
                      "anns_field": "filmVector", # 搜索的向量字段：filmVector
                      "param": {"metric_type": "L2", "params": {'nprobe': 10}}, # 'nprobe': 10代表前10个最相似的簇
                      "limit": 2
                      }
    request_1 = AnnSearchRequest(**search_param_1)
    # print(f'request_1--》{request_1}')
    # 创建多搜索请求 posterVector
    query_posterVector = [[0.02550758562349764, 0.006085637357292062, 0.5325251250159071, 0.7676432650114147, 0.5521074424751443]]
    sparse_search_params = {"data": query_posterVector,
                            "anns_field": "posterVector",
                            # 该参数值必须与集合模式中使用的值相同。
                            "param": {"metric_type": "COSINE"},
                            "limit": 2
                            }
    request_2 = AnnSearchRequest(**sparse_search_params)
    # 准备工作
    seqs = [request_1, request_2]
    # ranker = RRFRanker()
    ranker = WeightedRanker(0.7, 0.3)
    # 进行混合检索
    outputs = client.hybrid_search(collection_name="demo_v3",
                                   reqs=seqs,
                                   ranker=ranker,
                                   limit=2,
                                   output_fields=["filmVector", "posterVector"])
    print(f'outputs-->{outputs}')

    for hits in outputs:
        print("TopK results:")
        for hit in hits:
            print(hit)


# 删除集合
client.drop_collection(collection_name='demo_v3')
if __name__ == '__main__':
    # complex_query()
    ...