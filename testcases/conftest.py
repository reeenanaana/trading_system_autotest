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
from common.test_result_notify import (
    TestCaseResult,
    build_test_result_summary,
    notify_test_result,
)
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
# pytest 运行期间保存在内存里的用例结果列表。
# 业务场景：Redis 负责进度和失败名称持久化，这个列表负责给通知链路补充每条 case 的 outcome、耗时等明细。
testcase_results = []
CURRENT_PROCESS_IS_XDIST_WORKER = False


def is_xdist_worker(config):
    # pytest-xdist 并行运行时，每个 worker 都会有 workerinput 属性。
    # 业务场景：worker 只负责执行用例和更新 Redis，最终钉钉通知必须只由主进程发送一次。
    return hasattr(config, "workerinput")


def pytest_configure(config):
    global CURRENT_PROCESS_IS_XDIST_WORKER
    CURRENT_PROCESS_IS_XDIST_WORKER = is_xdist_worker(config)


def pytest_sessionstart(session):
    if is_xdist_worker(session.config):
        return

    # 并行模式下 collection_finish 可能不在主进程按预期执行，所以会话开始先清掉历史 Redis 数据。
    # total 先写 0，最终钉钉统计以本次 pytest 收到的 testcase_results 为准。
    process_redis.reset_all()
    process_redis.init_process(0)


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
    # @pytest.fixture 表示这是一个 pytest 夹具，测试用例可以通过参数名 test_objects 注入它。
    # scope='session' 表示整个测试会话只创建一次，避免每条用例都重复初始化页面对象。
    return ObjectPool()


# 作用：pytest 收集完本次要执行的所有用例后触发一次。
# 用法：这里用 session.items 拿到本轮用例总数，并初始化 Redis 中的自动化测试进度。
def pytest_collection_finish(session):
    if is_xdist_worker(session.config):
        return

    # pytest_collection_finish 是 pytest 的生命周期 hook：
    # 所有测试用例收集完成后自动调用，适合初始化“本轮测试总数”。
    # 获取所有用例的个数
    total = len(session.items)
    # 重置用例进度和失败用例名称
    process_redis.reset_all()
    # 初始化进度
    process_redis.init_process(total)


# 作用：从测试函数的 docstring 中提取用例名称。
# 用法：优先取 docstring 的第一行作为“测试用例”名称；如果没写 docstring，就用函数名兜底。
def get_testcase_description(item):
    # item.function 指向当前测试函数对象，__doc__ 是函数下方的三引号文档字符串。
    # 业务场景：用例写了 docstring 时，通知里展示业务描述；没写时用函数名兜底。
    doc = item.function.__doc__
    if not doc:
        return item.name
    # strip() 去掉首尾空白，splitlines()[0] 只取第一行，避免多行 docstring 把通知撑得太长。
    return doc.strip().splitlines()[0].strip()


def get_report_description(report):
    # xdist 会把 report.user_properties 从 worker 传回主进程，用它保留业务用例名称。
    for name, value in getattr(report, "user_properties", []):
        if name == "description" and value:
            return value
    return getattr(report, "description", report.nodeid)


# 作用：整个 pytest 会话结束后触发一次。
# pytest_sessionfinish 是 pytest 约定好的 Hook 函数名。
# pytest 在运行过程中会在固定生命周期节点主动查找并调用这些 Hook。只要你在 conftest.py 里定义了：pytest 就会自动注册它，并在 整个测试 session 即将结束时 调用它。
# 用法：这里统一写入结束状态，并把本轮收集到的所有 case 结果汇总成一条钉钉消息发送。
def pytest_sessionfinish(session, exitstatus):
    if is_xdist_worker(session.config):
        return

    # pytest_sessionfinish 是 pytest 的生命周期 hook：
    # 整个测试会话结束时自动调用，适合做收尾动作，例如写结束时间、发送通知。
    # 测试会话结束后写入结束时间和运行状态，便于外部看板判断本轮执行已完成。
    process_redis.write_end_time()
    process_redis.modify_running_status(process_redis.FINISHED)

    # build_test_result_summary 把 Redis 统计和本地 testcase_results 合并成统一摘要对象。
    summary = build_test_result_summary(process_redis, testcase_results)
    # notify_test_result 是统一通知入口；conftest.py 不直接关心钉钉 Markdown 怎么拼。
    notify_test_result(summary)


@pytest.fixture()
def driver():
    # yield 前是 fixture 的 setup：创建浏览器 driver。
    get_driver = DriverConfig().driver_config()
    yield get_driver
    # yield 后是 fixture 的 teardown：用例执行结束后关闭浏览器，释放资源。
    get_driver.quit()


# 作用：每条测试用例的 setup/call/teardown 阶段都会触发。
# 用法：这里只处理 call 阶段，因为 call 阶段才代表测试函数本身的执行结果；
#      本方法只负责更新 Redis 进度、失败截图、收集结果，不在这里发送钉钉消息。
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # hookwrapper=True 表示这是一个包装型 hook，必须先 yield，让 pytest 生成原始 report。
    # tryfirst=True 表示尽量优先执行本 hook，便于尽早给 report 补充 description 和截图。
    result = yield
    # result.get_result() 取出 pytest 为当前阶段生成的测试报告对象。
    report = result.get_result()
    report.description = get_testcase_description(item)
    report.user_properties.append(("description", report.description))

    if report.when == 'call' and report.failed:
        # report.when 有 setup/call/teardown 三种阶段。
        # 这里只处理 call，因为 call 才代表测试函数主体执行结果，避免 setup/teardown 重复计数。
        # 从 fixture 中获取 driver 实例
        # item.funcargs 就是一个字典，存储了测试用例使用的所有 fixture 实例，通过键值对的方式存取。
        driver_instance = item.funcargs.get('driver')
        if driver_instance:
            # 失败时把当前浏览器截图挂到 Allure 报告，方便从通知跳转后定位问题。
            add_img_to_report(
                driver_instance,
                "失败截图",
                need_sleep=False
            )
    else:
        pass


def pytest_runtest_logreport(report):
    if CURRENT_PROCESS_IS_XDIST_WORKER or report.when != 'call':
        return

    description = get_report_description(report)
    if report.failed:
        # 更新失败用例个数
        process_redis.update_failed()
        # 增加失败用例的名称到报告用例中的description
        process_redis.insert_into_failed_testcases_name(description)
        # 把当前失败用例转换成统一数据模型，交给后续通知摘要使用。
        testcase_results.append(TestCaseResult(
            name=description,
            outcome=report.outcome,
            # getattr(obj, "attr", default) 表示安全读取属性；没有 duration 时返回 0.0。
            duration=getattr(report, "duration", 0.0),
            error=str(report.longrepr),
        ))
    elif report.passed:
        # 更新用例成功的个数
        process_redis.update_success()
        # 成功用例也记录下来，后续如果通知需要展示用例明细或耗时，可以直接复用。
        testcase_results.append(TestCaseResult(
            name=description,
            outcome=report.outcome,
            duration=getattr(report, "duration", 0.0),
        ))
    else:
        pass
