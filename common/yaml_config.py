#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/4/27 15:36
# @Author: Rena

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
        config_path = get_project_path("trading_system_autotest") / "config" / config_file
        if not config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_path}")

        with open(config_path, 'r', encoding="utf-8") as env_file:
            self.env = yaml.full_load(env_file)  # full_load 等同于 load(..., FullLoader)
            # print(f"✅ 配置文件加载成功: {config_path}")

        # print(self.env)
        # print(config_path)

    def get_username_password(self):
        return self.env['username'], self.env['password']

    def get_url(self):
        return self.env['url']

#
# if __name__ == '__main__':
#     print(GetConf().get_username_password())
# 你的代码思路正确，主要需要改进：
# 用 Path 替代硬编码路径
# 用 safe_load/full_load() 替代 load
# 添加异常处理

