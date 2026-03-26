# -*-coding:utf-8-*-
import jieba
from rank_bm25 import BM25L
import logging

# 配置日志
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BM25Search():
    def __init__(self, documents):
        # documents:代表所有的文档
        self.documents = documents
        # 对所有的文档进行分词
        self.tokenized_docs = [jieba.lcut(doc) for doc in documents]
        # 实例化BM25模型
        self.bm25 = BM25L(self.tokenized_docs)
        logger.info('BM25模型初始化完成')

    def search(self, query):
        # 对query进行分词
        tokenized_query = jieba.lcut(query)
        try:
            # 计算query和每个doc的bm25的分数
            scores = self.bm25.get_scores(tokenized_query)
            # print(f'scores--》{scores}')
            # 获得最高分数的索引
            best_idx = scores.argmax()
            # print(f'best_idx-->{best_idx}')
            # 获取最匹配的doc以及对应的分数
            best_score = scores[best_idx]
            best_doc = self.documents[best_idx]
            logger.info(f'查询：{query}, 最佳匹配doc：{best_doc}, 分数为：{best_score}')
            return best_doc, best_score
        except Exception as e:
            logger.error(f'检索失败：{e}')
            return None, 0


if __name__ == '__main__':
    documents = ["我喜欢编程", "编程很有趣"]
    bm25_model = BM25Search(documents)
    query = "他喜欢编程"
    bm25_model.search(query)


