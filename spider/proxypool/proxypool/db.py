import redis
import re
from proxypool.settings import *
from proxypool.error import PoolEmptyError
import random


class RedisClient:
    """
    操作代理池。设置代理的分数，获取代理等操作
    """

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: redis主机地址
        :param port: redis端口号
        :param password: redis密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理，设置分数
        :param proxy: 代理端口地址
        :param score: 分数
        :return: 添加结果
        """
        if not re.match('(\d+\.){3}\d+:\d+', proxy):
            print('代理格式错误', proxy, '丢弃')
            return
        # 如果key中不存在proxy的得分，则新增这个proxy并设置得分
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, {proxy: score})

    def random(self):
        """
        随机的获取有效的代理，首先尝试满分代理，如果没有满分则随机返回
        :return: 有效代理
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if not len(result):
            # 取前100个出来再随机
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
        if not len(result):
            raise PoolEmptyError
        return random.choice(result)

    def decrease(self, proxy):
        """
        降低代理分数值
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        检验代理是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        return not self.db.zscore(REDIS_KEY, proxy) is None

    def max(self, proxy):
        """
        将该代理设置为 MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        """
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, {proxy: MAX_SCORE})

    def count(self):
        """
        获取代理池大小
        :return: 代理数量
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.db.zremrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop):
        """
        批量获取
        :param start: 起始索引, 包含
        :param stop: 结束索引, 不包含
        :return: 代理列表
        """
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)
