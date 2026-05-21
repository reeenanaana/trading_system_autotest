#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/19 17:46
# @Author: Rena
"""
钉钉机器人通知模块。

业务场景：
自动化测试结束后，需要把测试结果推送到钉钉群，方便团队不用打开 Jenkins 也能看到本轮结果。
本模块只负责“怎么发钉钉”，不负责“测试结果从哪里来”，结果数据由 common/test_result_notify.py 传入。
"""

import logging

import requests

from common.yaml_config import GetConf
from common.tools import get_everyday_wallpaper

logger = logging.getLogger(__name__)

# 钉钉 webhook 是外部 HTTP 服务，必须设置超时。
# 业务场景：如果钉钉接口或网络异常，不能让 pytest 结束流程一直卡住。
DEFAULT_TIMEOUT = 10


def _post_dingtalk(webhook, data, timeout=DEFAULT_TIMEOUT):
    # headers 告诉钉钉服务：请求体是 JSON。
    # ;charset=utf-8 用于明确中文内容按 UTF-8 编码处理。
    headers = {"Content-Type": "application/json ;charset=utf-8"}
    try:
        # requests.post(..., json=data) 会自动把 Python dict 序列化为 JSON 请求体。
        # 业务场景：钉钉机器人接口要求用 POST 提交固定格式的 JSON 消息。
        res = requests.post(url=webhook, json=data, headers=headers, timeout=timeout)
        logger.info("发送钉钉消息，返回结果: %s", res.text)
        return res
    except requests.RequestException as error:
        # 捕获 requests 的网络异常，避免通知失败导致测试进程异常退出。
        logger.warning("发送钉钉消息失败: %s", error)
        return None


def send_dingtalk_msg(webhook, content, timeout=DEFAULT_TIMEOUT):
    """
    发送钉钉消息-text
    :param webhook:
    :param content:
    :param timeout:
    :return:
    """
    # data 是钉钉机器人要求的文本消息结构：
    # msgtype 指定消息类型，text.content 是实际展示内容。
    data = {
        "msgtype": "text",
        "text": {
            "content": content,  # 内容必须包含机器人设置的关键词，如"自动化测试"
            # isAtAll 使用布尔值 True，表示通知时 @所有人；如果不想打扰全员，可改成 False。
            "at": {"isAtAll": True},
        }
    }
    return _post_dingtalk(webhook, data, timeout=timeout)


def build_dingtalk_markdown(
        allure_url,
        total_count,
        success_count,
        failure_count,
        failed_testcases_name,
        report_title,
        progress=None,
        start_time=None
):
    """
    构建钉钉 Markdown 消息内容。
    :param allure_url:
    :param total_count:
    :param success_count:
    :param failure_count:
    :param failed_testcases_name:
    :param report_title:
    :param progress:
    :param start_time:
    :return:
    """
    # 每日壁纸是通知里的展示增强项；获取失败时返回 None，不影响核心测试结果通知。
    wallpaper_url = get_everyday_wallpaper()
    # lines 用列表逐行保存 Markdown 文案，最后用 "\n".join(lines) 合并。
    # 业务场景：比直接长字符串拼接更容易维护，例如后续增加耗时、环境信息。
    lines = [
        # #### 是 Markdown 四级标题，钉钉会把它展示成报告标题。
        "#### " + report_title,
        # > 是 Markdown 引用块，钉钉里会以更紧凑的报告样式展示。
        "> 用例总数：{}个".format(total_count),
        ">",
        "> 测试结果：通过{}个，失败{}个{}".format(
            success_count,
            failure_count,
            # 没有失败时不展示失败用例列表，避免出现“失败0个，失败的用例为：”这种噪音。
            failed_testcases_name if failure_count else "",
        ),
    ]
    if progress:
        # progress 来自 Redis 统计，业务含义是本轮已完成用例占比。
        lines.append("> 执行进度：{}".format(progress))
    if start_time:
        # start_time 来自 Redis，方便排查是哪一轮测试产生的通知。
        lines.append("> 开始时间：{}".format(start_time))
    if wallpaper_url:
        # Markdown 图片语法：![图片描述](图片地址)。
        lines.append("![每日壁纸]({})".format(wallpaper_url))
    if allure_url:
        # Allure 链接只有在 Jenkins URL 已配置时才展示。
        lines.extend([
            "> ###### 点击查看测试报告",
            # Markdown 链接语法：[展示文本](跳转地址)。
            "> [Allure测试报告]({})".format(allure_url),
        ])
    return "\n".join(lines)


def send_dingtalk_msg_markdown(
        ding_webhook,
        allure_url,
        total_count,
        success_count,
        failure_count,
        failed_testcases_name,
        report_title,
        progress=None,
        start_time=None,
        timeout=DEFAULT_TIMEOUT
):
    """
    发送markdown格式的消息到钉钉
    :param ding_webhook:钉钉群的webhook
    :param allure_url:allure地址
    :param total_count:总数
    :param success_count:成功个数
    :param failure_count:失败个数
    :param failed_testcases_name:失败用例名称
    :param report_title:报告标题
    :param progress:执行进度
    :param start_time:开始时间
    :param timeout:请求超时时间
    :return:
    """
    # data 是钉钉机器人要求的 Markdown 消息结构。
    # markdown.title 是消息卡片标题，markdown.text 是正文。
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": report_title,
            "text": build_dingtalk_markdown(
                allure_url,
                total_count,
                success_count,
                failure_count,
                failed_testcases_name,
                report_title,
                progress=progress,
                start_time=start_time,
            ),
        },
    }
    return _post_dingtalk(ding_webhook, data, timeout=timeout)


if __name__ == "__main__":
    webhook = GetConf().get_dingding_webhook()
    send_dingtalk_msg(webhook, "rena测试")
