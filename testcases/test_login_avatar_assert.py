#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/9 17:42
# @Author: Rena

import pytest
from time import sleep

from page.LoginPage import LoginPage


class TestLoginAvatarAssert:
    @pytest.mark.login
    def test_login_avatar_assert(self, driver):
        """
        登录后断言图片
        :param driver:
        :return:
        """
        LoginPage().login(driver, 'jay')
        sleep(10)
        assert LoginPage().login_avatar_assert(driver, "周杰伦头像截图.png") > 0.9

# 跑不了，暂时注释掉（5.11要继续往后看12-15章）
