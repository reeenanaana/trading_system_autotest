#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/19 11:47
# @Author: Rena

import logging

import redis

from common.tools import get_now_date_time_str
from common.redis_operation import RedisOperation

logger = logging.getLogger(__name__)


class ProcessRedis:
    def __init__(self):
        # RedisOperation().redis_client 是封装后的 Redis 连接对象。
        # 业务场景：测试执行过程中持续写入进度，测试结束通知再从 Redis 读取汇总。
        self.redis_client = RedisOperation().redis_client
        # Redis hash key：保存本轮自动化测试的 total/success/failed/start_time/end_time。
        self.UI_AUTOTEST_PROCESS = 'ui_autotest_process'
        # Redis list key：保存失败用例名称，通知中用于展示“失败的用例为：xxx”。
        self.FAILED_TESTCASES_NAMES = 'failed_testcases_name'
        # Redis string key：保存任务运行状态，1 表示运行中，0 表示已结束。
        self.RUNNING_STATUS = 'running_status'
        self.RUNNING = 1
        self.FINISHED = 0

    def _execute(self, operation, default=None):
        # operation 是一个函数对象，调用 _execute(lambda: xxx) 时，真正的 Redis 操作会在这里执行。
        # 业务场景：统一处理 Redis 不可用的情况，避免 Redis 挂了导致 UI 自动化测试本身失败。
        if self.redis_client is None:
            return default
        try:
            return operation()
        except redis.RedisError as error:
            logger.warning("Redis操作失败，已跳过本次进度同步: %s", error)
            return default

    def reset_all(self):
        # 删除所有进度
        self._execute(lambda: self.redis_client.delete(self.UI_AUTOTEST_PROCESS))
        # 删除所有失败用例的名称
        self._execute(lambda: self.redis_client.delete(self.FAILED_TESTCASES_NAMES))

    def init_process(self, total):
        """
        初始化进度，包括总数、成功数、失败数、开始时间、运行状态
        :param total:
        :return:
        """
        # hset 写入 Redis hash 字段，适合保存同一轮测试下的多个统计字段。
        self._execute(lambda: self.redis_client.hset(self.UI_AUTOTEST_PROCESS, 'total', total))
        self._execute(lambda: self.redis_client.hset(self.UI_AUTOTEST_PROCESS, 'success', 0))
        self._execute(lambda: self.redis_client.hset(self.UI_AUTOTEST_PROCESS, 'failed', 0))
        self._execute(lambda: self.redis_client.hset(self.UI_AUTOTEST_PROCESS, 'start_time', get_now_date_time_str()))
        self._execute(lambda: self.redis_client.hset(self.UI_AUTOTEST_PROCESS, 'end_time', ""))
        self.modify_running_status(self.RUNNING)

    def update_success(self):
        """
        成功用例个数+1
        :return:
        """
        # hincrby 是 Redis 的原子自增操作，适合多条用例执行时累计成功数量。
        self._execute(lambda: self.redis_client.hincrby(self.UI_AUTOTEST_PROCESS, 'success'))

    def update_failed(self):
        """
        失败用例个数+1
        :return:
        """
        # 失败数单独累计，通知中会用 success/failed/total 生成测试结果摘要。
        self._execute(lambda: self.redis_client.hincrby(self.UI_AUTOTEST_PROCESS, 'failed'))

    def insert_into_failed_testcases_name(self, failed_testcases_name):
        """
        增加失败用例名称
        :param failed_testcases_name:失败用例名称
        :return:
        """
        # lpush 把失败用例名称压入 Redis list。
        # 业务场景：测试结束后可以一次性 lrange 取出全部失败用例并拼到通知里。
        self._execute(lambda: self.redis_client.lpush(self.FAILED_TESTCASES_NAMES, failed_testcases_name))

    def get_result(self):
        """
        获取测试结果
        :return:
        """
        # hget 读取 Redis hash 中的单个字段；default 用于 Redis 不可用时兜底。
        total = self._execute(lambda: self.redis_client.hget(self.UI_AUTOTEST_PROCESS, 'total'), 0)
        if total is None:
            total = 0
        success = self._execute(lambda: self.redis_client.hget(self.UI_AUTOTEST_PROCESS, 'success'), 0)
        if success is None:
            success = 0
        failed = self._execute(lambda: self.redis_client.hget(self.UI_AUTOTEST_PROCESS, 'failed'), 0)
        if failed is None:
            failed = 0
        start_time = self._execute(lambda: self.redis_client.hget(self.UI_AUTOTEST_PROCESS, 'start_time'), '-')
        if start_time is None:
            start_time = '-'
        return total, success, failed, start_time

    def get_process(self):
        """
        获取测试进度，计算百分比
        :return:
        """
        total, success, failed, start_time = self.get_result()
        # Redis 读出的数字可能是字符串，计算前需要转成 int。
        total = int(total or 0)
        success = int(success or 0)
        failed = int(failed or 0)
        if total == 0:
            return "0%"
        return f"{(success + failed) / total * 100:.1f}%"

    def get_failed_testcases_name(self):
        """
        获取所有失败用例的名称
        :return:
        """
        # lrange(key, 0, -1) 表示读取整个 list。
        failed_testcases_names = self._execute(lambda: self.redis_client.lrange(self.FAILED_TESTCASES_NAMES, 0, -1), [])
        return failed_testcases_names

    def write_end_time(self):
        """
        把测试结束时间写入redis
        :return:
        """
        # 测试结束时写入 end_time，外部看板或通知都可以知道本轮执行闭环完成。
        self._execute(lambda: self.redis_client.hset(self.UI_AUTOTEST_PROCESS, 'end_time', get_now_date_time_str()))

    def modify_running_status(self, status):
        """
        修改运行状态
        :param status:
        :return:
        """
        # 运行状态是单值，用 Redis string 保存即可。
        self._execute(lambda: self.redis_client.set(self.RUNNING_STATUS, status))
