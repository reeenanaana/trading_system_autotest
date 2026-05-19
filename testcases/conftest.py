#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/6 18:44
# @Author: Rena

from functools import cached_property

import pytest

from common.mysql_operate import MysqlOperate
from config.driver_config import DriverConfig
from common.report_add_img import add_img_to_report
from common.process_redis import ProcessRedis
from page.AccountPage import AccountPage
from page.ExternalLinkPage import ExternalLinkPage
from page.GoodsPage import GoodsPage
from page.HomePage import HomePage
from page.IframeBaiduMapPage import IframeBaiduMapPage
from page.LeftMenuPage import LeftMenuPage
from page.LoginPage import LoginPage
from page.OrderPage import OrderPage
from page.TradingMarketPage import TradingMarketPage

process_redis = ProcessRedis()


class ObjectPool:
    @cached_property
    def account_page(self):
        return AccountPage()

    @cached_property
    def external_link_page(self):
        return ExternalLinkPage()

    @cached_property
    def goods_page(self):
        return GoodsPage()

    @cached_property
    def home_page(self):
        return HomePage()

    @cached_property
    def iframe_baidu_map_page(self):
        return IframeBaiduMapPage()

    @cached_property
    def left_menu_page(self):
        return LeftMenuPage()

    @cached_property
    def login_page(self):
        return LoginPage()

    @cached_property
    def mysql_operate(self):
        return MysqlOperate()

    @cached_property
    def order_page(self):
        return OrderPage()

    @cached_property
    def trading_market_page(self):
        return TradingMarketPage()


@pytest.fixture(scope='session')
def test_objects():
    return ObjectPool()


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
