#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/6 18:44
# @Author: Rena

import pytest

from config.driver_config import DriverConfig
from common.report_add_img import add_img_to_report
from common.process_redis import ProcessRedis

process_redis = ProcessRedis()


def pytest_collection_finish(session):
    # 获取所有用例的个数
    total = len(session.items)
    # 重置用例进度和失败用例名称
    process_redis.reset_all()
    # 初始化进度
    process_redis.init_process(total)


def pytest_sessionfinish(session, exitstatus):
    # 测试会话结束后写入结束时间和运行状态，便于外部看板判断本轮执行已完成。
    process_redis.write_end_time()
    process_redis.modify_running_status(process_redis.FINISHED)


@pytest.fixture()
def driver():
    get_driver = DriverConfig().driver_config()
    yield get_driver
    get_driver.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    result = yield
    report = result.get_result()
    report.description = str(item.function.__doc__)

    if report.when == 'call' and report.failed:
        # 从 fixture 中获取 driver 实例
        # item.funcargs 就是一个字典，存储了测试用例使用的所有 fixture 实例，通过键值对的方式存取。
        driver_instance = item.funcargs.get('driver')
        if driver_instance:
            add_img_to_report(
                driver_instance,
                "失败截图",
                need_sleep=False
            )
            # 更新失败用例个数
            process_redis.update_failed()
            # 增加失败用例的名称到报告用例中的description
            process_redis.insert_into_failed_testcases_name(report.description)
    elif report.when == 'call' and report.passed:
        # 更新用例成功的个数
        process_redis.update_success()
    else:
        pass
    process = process_redis.get_process()
    print(process)
