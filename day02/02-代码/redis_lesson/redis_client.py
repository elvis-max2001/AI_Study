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
        except Exception as e:
            logger.error(f'Redis加载失败: {e}')
            raise # 重新将错误抛出

if __name__ == '__main__':
    redis_client = RedisClient()