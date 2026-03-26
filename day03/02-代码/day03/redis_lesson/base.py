# -*-coding:utf-8-*-
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Config:
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_PASSWORD = '1234'
    REDIS_DB = 0


if __name__ == '__main__':
    print(Config.REDIS_PORT)
    conf = Config()
    print(conf.REDIS_PORT)