#! /usr/bin/python3
# coding = utf-8
"""
测试结果通知编排模块。

业务场景：
pytest 执行结束后，conftest.py 会把本轮收集到的用例结果交给本模块。
本模块负责把本次 pytest 结果整理成统一的 TestResultSummary，再交给具体通知渠道发送。

这样做的好处：
1. pytest hook 只关心“什么时候收集结果”，不关心“通知内容怎么拼”。
2. 钉钉、企业微信、飞书等渠道以后可以复用同一份 TestResultSummary。
3. Jenkins/Allure 报告链接、失败用例列表等业务字段集中维护。
"""

import logging
import os
from dataclasses import dataclass, field
from typing import Iterable, List, Optional

from common.ding_talk import send_dingtalk_msg_markdown
from common.yaml_config import GetConf

logger = logging.getLogger(__name__)

# 当配置文件没有填写项目名或报告标题时，用下面的默认值兜底。
# 业务场景：本地调试时可能还没配置 Jenkins/报告信息，不能因此中断测试结束流程。
DEFAULT_PROJECT_NAME = "trading_system_autotest"
DEFAULT_REPORT_TITLE = "UI自动化测试-测试报告"


@dataclass
class TestCaseResult:
    """
    单条测试用例的执行结果。

    语法说明：
    @dataclass 是 Python 标准库提供的装饰器，会自动生成 __init__、__repr__ 等方法。
    业务场景：
    pytest_runtest_makereport 每跑完一条用例，就生成一个 TestCaseResult 放进列表，
    最终用于通知中展示失败用例、耗时、错误信息等。
    """

    # 类型注解 name: str 表示 name 期望是字符串，便于 IDE 提示和后续维护。
    name: str
    # pytest report.outcome 的常见值是 passed、failed、skipped。
    outcome: str
    # 默认值 0.0 表示即使 pytest 没给 duration，也不会影响通知构建。
    duration: float = 0.0
    # 失败原因可选，当前通知先不展示，后续可用于扩展详细失败摘要。
    error: str = ""


@dataclass
class TestResultSummary:
    """
    本轮测试结果汇总，用于不同通知渠道复用同一份数据。

    业务场景：
    这是通知链路中的“统一数据模型”。不管最终发钉钉还是企业微信，都先把数据整理成它，
    避免每个渠道各自拼 Jenkins 地址、处理失败用例。
    """

    project_name: str
    report_title: str
    allure_url: str
    total_count: int
    success_count: int
    failure_count: int
    progress: str
    failed_testcases_name: str = ""
    start_time: str = "-"
    # field(default_factory=list) 的作用是给每个实例创建自己的新列表。
    # 业务场景：避免多个 TestResultSummary 共用同一个列表，导致不同批次测试结果互相污染。
    testcases: List[TestCaseResult] = field(default_factory=list)

    @property
    def passed(self):
        # @property 让调用方可以用 summary.passed 访问结果，而不是 summary.passed()。
        # 业务场景：判断本轮测试是否全通过，后续可用于控制通知标题颜色或是否 @所有人。
        return self.failure_count == 0


def _format_failed_names(failed_names: Iterable[str]) -> str:
    # Iterable[str] 表示参数可以是 list、tuple 等可迭代对象，不限定必须是 list。
    # 业务场景：Redis 返回列表，本地兜底也会生成列表，统一在这里格式化成通知文案。
    names = [name for name in failed_names if name]
    if not names:
        return ""
    return "，失败的用例为：" + "，".join(names)


def _build_progress(total_count: int, finished_count: int) -> str:
    if total_count <= 0:
        return "0.0%"
    return "{:.1f}%".format(finished_count / total_count * 100)


def _build_allure_url(jenkins_url: str, project_name: str) -> str:
    # 本地手动运行时，如果需要钉钉跳转到本次生成的本地报告，可以显式传入最终报告地址。
    # 业务场景：只跑单个 case 时，避免误跳到 Jenkins 上一次全量构建报告。
    explicit_allure_url = os.getenv("ALLURE_REPORT_URL")
    if explicit_allure_url:
        return explicit_allure_url

    # Jenkins 构建时会自动注入 BUILD_URL，例如 http://jenkins/job/demo/12/。
    # 业务场景：钉钉通知必须指向“本次构建”的 Allure 报告，而不是 Job 维度的最新报告。
    build_url = os.getenv("BUILD_URL")
    if build_url:
        return build_url.rstrip("/") + "/allure/"

    # 非 Jenkins 环境下不使用 jenkins.url 兜底，避免本地手动运行单 case 时跳到 Jenkins 全量报告。
    return ""


def build_test_result_summary(testcases: Iterable[TestCaseResult], conf: Optional[GetConf] = None, start_time: str = "-"):
    """
    从本次 pytest 收集结果中生成统一测试报告摘要。
    :param testcases: pytest hook 收集到的用例结果
    :param conf: 配置读取对象，默认读取 environment.yaml
    :param start_time: 本次测试开始时间
    :return: TestResultSummary
    """
    # conf or GetConf() 是常见兜底写法：
    # 调用方没传配置对象时，默认读取 environment.yaml；单元测试时也可以传假的 conf。
    conf = conf or GetConf()
    # list(testcases) 把可迭代对象固定成列表，后续可多次遍历，不怕生成器被消费掉。
    testcase_list = list(testcases)
    # 通知统计只使用本次 pytest report，避免 Redis 历史数据或并行写入污染最终报告。
    total_count = len(testcase_list)
    success_count = len([testcase for testcase in testcase_list if testcase.outcome == "passed"])
    failure_count = len([testcase for testcase in testcase_list if testcase.outcome == "failed"])
    failed_names = [testcase.name for testcase in testcase_list if testcase.outcome == "failed"]
    progress = _build_progress(total_count, success_count + failure_count)

    project_name = conf.get_project_name() or DEFAULT_PROJECT_NAME
    report_title = conf.get_report_title() or DEFAULT_REPORT_TITLE
    allure_url = _build_allure_url(conf.get_jenkins_url(), project_name)

    # 返回统一摘要对象，后续通知渠道只依赖这个对象，不直接依赖 Redis 或 pytest。
    return TestResultSummary(
        project_name=project_name,
        report_title=report_title,
        allure_url=allure_url,
        total_count=total_count,
        success_count=success_count,
        failure_count=failure_count,
        progress=progress,
        failed_testcases_name=_format_failed_names(failed_names),
        start_time=start_time or "-",
        testcases=testcase_list,
    )


def notify_test_result(summary: TestResultSummary, conf: Optional[GetConf] = None):
    """
    统一发送测试结果通知。当前项目先接入钉钉，后续可在这里扩展企业微信/飞书。
    :param summary: 测试结果汇总
    :param conf: 配置读取对象，默认读取 environment.yaml
    :return: True 表示已触发发送，False 表示未配置 webhook
    """
    conf = conf or GetConf()
    # webhook 是钉钉机器人地址，放在配置文件中，避免写死在通知逻辑里。
    webhook = conf.get_dingding_webhook()
    if not webhook:
        logger.warning("未配置钉钉 webhook，跳过测试结果通知")
        return False

    # 当前只接入钉钉；以后新增企业微信/飞书时，可以继续在这里分发，不改 conftest.py。
    send_dingtalk_msg_markdown(
        webhook,
        summary.allure_url,
        summary.total_count,
        summary.success_count,
        summary.failure_count,
        summary.failed_testcases_name,
        summary.report_title,
        progress=summary.progress,
        start_time=summary.start_time,
    )
    return True
