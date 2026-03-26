# -*-coding:utf-8-*-
import redis
import json
from base import Config, logger

class RedisClient():
    def __init__(self):
        self.logger = logger
        try:
            # 连接redis
            self.client = redis.StrictRedis(host=Config.REDIS_HOST,
                                            port=Config.REDIS_PORT,
                                            password=Config.REDIS_PASSWORD,
                                            db=Config.REDIS_DB,
                                            decode_responses=True, # redis默认返回的结果它是字节数据格式，decode_responses设置为True，默认用utf-8去解码
                                            )
            logger.info('Redis加载成功')
        except redis.RedisError as e:
            logger.error(f'Redis加载失败: {e}')
            raise # 重新将错误抛出


    def set_data(self, key, value):
        try:
            self.client.set(key, json.dumps(value, ensure_ascii=False))
            self.logger.info(f"存储数据到 Redis: {key}")
        except redis.RedisError as e:
            self.logger.error(f"Redis 存储失败: {e}")


    def get_data(self, key):
        try:
            data = self.client.get(key)
            # print(f'data--》{data}')
            return json.loads(data) if data else None
        except redis.RedisError as e:
            self.logger.error(f"Redis 获取失败: {e}")
            return None

    def get_answer(self, query):
        try:
            answer = self.client.get(f"answer:{query}")
            if answer:
                self.logger.info(f"从 Redis 获取答案: {query}")
                return answer
            return None
        except redis.RedisError as e:
            self.logger.error(f"Redis 查询失败: {e}")
            return None

    def deleter_key(self, key):
        try:
            result = self.client.delete(key)
            if result == 1:
                self.logger.info(f'成功删除Redis键：{key}')
            else:
                self.logger.info(f'Redis键不存在，无法删除：{key}')
            return result
        except redis.RedisError as e:
            self.logger.error(f'Redis删除失败：{e}')

    def get_keys(self):
        '''获取当前redis中有多少个键'''
        return self.client.keys("*")


if __name__ == '__main__':
    redis_client = RedisClient()
    key = 'answer:黑马程序员'
    value = {"name": '黑马', "age": 19}
    # # key = 1
    # # value = "王五"
    # redis_client.set_data(key, value)
    # result = redis_client.get_data(key)
    # print(result)
    # redis_client.deleter_key(key)
    print(redis_client.get_answer(query="黑马程序员"))
    # print(redis_client.get_keys())
    # print(redis_client.get_answer(query="关联子查询的执行顺序是什么"))

