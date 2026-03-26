# -*- coding:utf-8 -*-
import logging
#todo: 1.log的基本使用
def dm01():
    # 配置基本的日志设置
    logging.basicConfig(level=logging.INFO)

    # 获取日志记录器
    logger = logging.getLogger("Example1")
    # logger2 = logging.getLogger("Example2")

    # 记录不同级别的日志
    logger.debug("这是调试信息，通常用于开发")
    logger.info("程序运行正常")
    logger.warning("注意，可能有小问题")
    logger.error("发生错误")
    logger.critical("严重错误，程序可能崩溃")

# todo:自定义日志的格式
def dm02():
    # 配置日志格式
    logging.basicConfig(
        level=logging.DEBUG,
        # format='%(asctime)s 日志级别： %(levelname)s  - 日志的消息：%(message)s'
        # format='%(asctime)s 日志级别： %(levelname)s  - 日志记录名称：%(name)s- 日志的消息：%(message)s'
        format='%(asctime)s - %(levelname)s - %(filename)s - %(name)s - Line:%(lineno)d - %(message)s'
    )

    # 获取日志记录器
    logger = logging.getLogger("Example2")

    # 记录日志
    logger.debug("调试模式已开启")
    logger.info("正在处理数据")
    logger.error("数据处理失败")

# todo:3. 指定日志输出到文件中保存
def dm03():
    import logging

    # 配置日志，输出到文件
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='app.log',  # 日志文件路径
        filemode='a',  # 'a'表示追加，'w'表示覆盖
        encoding='utf-8'
    )

    # 获取日志记录器
    logger = logging.getLogger("Example3")

    # 记录日志
    logger.info("程序启动")
    logger.warning("内存使用率较高")
    logger.error("无法连接数据库")

# todo:4. 将日志既在控制台输出也要保存到文件中
def dm04():
    # 创建日志记录器
    logger = logging.getLogger(name="Example4")
    logger.setLevel(level=logging.INFO) # 设置log的级别
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level=logging.INFO)# 设置控制台log的级别
    # 创建文件处理器
    file_handler = logging.FileHandler('ai.log')
    file_handler.setLevel(level=logging.DEBUG)# 设置文件处理器log的级别
    # 定义日志的格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # 为处理器设置格式
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    # 将处理器添加到记录器中
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    # 输出 日志
    logger.debug("调试信息，仅写入文件")
    logger.info("正常 信息")
    logger.error("发生错误")

if __name__ == '__main__':
    # dm01()
    # dm02()
    # dm03()
    dm04()