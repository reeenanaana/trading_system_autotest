#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/19 11:34
# @Author: Rena

import redis
import logging

from common.yaml_config import GetConf

logger = logging.getLogger(__name__)


class RedisOperation:
    DEFAULT_SOCKET_CONNECT_TIMEOUT = 2
    DEFAULT_SOCKET_TIMEOUT = 2

    def __init__(self):
        redis_info = GetConf().get_redis()
        self.redis_client = redis.Redis(
            host=redis_info['host'],
            port=redis_info['port'],
            db=redis_info['db'],
            decode_responses=True,
            # charset='utf-8', ✅ redis-py 4.x+ 的变化，默认编码固定为 UTF‑8（不再允许修改，charset参数被 彻底移除）
            encoding='utf-8',
            password=redis_info.get('password'),
            socket_connect_timeout=redis_info.get('socket_connect_timeout', self.DEFAULT_SOCKET_CONNECT_TIMEOUT),
            socket_timeout=redis_info.get('socket_timeout', self.DEFAULT_SOCKET_TIMEOUT),
        )
        try:
            self.redis_client.ping()
        except redis.RedisError as error:
            logger.warning("Redis连接不可用，测试进度将不会写入Redis: %s", error)
            self.redis_client = None


if __name__ == '__main__':
    # 获取db中的值，前面作者在db0中添加了一个kv对，william:12345678，我没添加
    print(RedisOperation().redis_client.get("william"))
