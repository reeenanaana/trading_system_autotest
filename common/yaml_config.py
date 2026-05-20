#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/4/27 15:36
# @Author: Rena

import os

import yaml
from pathlib import Path
from common.tools import get_project_path


class GetConf:
    def __init__(self, config_file: str = "environment.yaml"):
        """
        初始化，加载配置文件
        :param config_file: 配置文件名，默认 environment.yaml
        """
        # pathlib库的最大优点之一就是跨平台兼容。代码中的 / 操作符会被Python自动转换成当前系统（Windows、macOS、Linux）对应的路径分隔符，这是它的标准特性。
        # 业务场景：无论从 PyCharm、命令行还是 Jenkins 启动，都能定位到项目 config/environment.yaml。
        config_path = get_project_path("trading_system_autotest") / "config" / config_file
        if not config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_path}")

        with open(config_path, 'r', encoding="utf-8") as env_file:
            # yaml.full_load 会把 YAML 文件解析成 Python dict。
            # 业务场景：通知链路通过 dict 读取 dingding_group、project、report、jenkins 等配置。
            self.env = yaml.full_load(env_file)  # full_load 等同于 load(..., FullLoader)
            # print(f"✅ 配置文件加载成功: {config_path}")

        # print(self.env)
        # print(config_path)

    def get_username_password(self, user):
        # return self.env['username'], self.env['password']
        return self.env["user"][user]["username"], self.env["user"][user]["password"]

    def get_url(self):
        return self.env['url']

    def get_mysql_config(self):
        return self.env['mysql']

    def get_redis(self):
        return self.env["redis"]

    def get_dingding_webhook(self):
        # Jenkins 中优先从环境变量读取 webhook，避免把钉钉机器人 token 提交到 Git 仓库。
        # 本地调试时仍兼容 environment.yaml 里的 dingding_group.webhook。
        webhook = os.getenv("DINGDING_WEBHOOK") or os.getenv("DINGTALK_WEBHOOK")
        if webhook:
            return webhook
        # get(..., {}) 是安全读取写法：配置缺失时返回空字符串，让通知链路跳过发送而不是报 KeyError。
        return self.env.get("dingding_group", {}).get("webhook", "")

    def get_project_name(self):
        # 项目名用于拼 Jenkins Allure 地址：/job/{project_name}/allure/。
        return self.env.get("project", {}).get("name", "trading_system_autotest")

    def get_report_title(self):
        # 报告标题会展示在钉钉 Markdown 消息顶部。
        return self.env.get("report", {}).get("title", "UI自动化测试-测试报告")

    def get_jenkins_url(self):
        # Jenkins 地址为空时，通知仍会发送，只是不展示 Allure 报告链接。
        return self.env.get("jenkins", {}).get("url", "")


if __name__ == '__main__':
    # print(GetConf().get_username_password("william"))
    print(GetConf().get_dingding_webhook())
# 你的代码思路正确，主要需要改进：
# 用 Path 替代硬编码路径
# 用 safe_load/full_load() 替代 load
# 添加异常处理
