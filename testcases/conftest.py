#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/6 18:44
# @Author: Rena

import pytest

from config.driver_config import DriverConfig
from common.report_add_img import add_img_to_report


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
