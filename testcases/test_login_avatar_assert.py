#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/9 17:42
# @Author: Rena

from time import sleep

import pytest
import allure

from page.LoginPage import LoginPage
from common.report_add_img import add_img_to_report


class TestLoginAvatarAssert:
    @pytest.mark.login
    @allure.feature('登录')
    @allure.description('登录后断言图片')
    def test_login_avatar_assert(self, driver):
        """
        登录后断言图片
        :param driver:
        :return:
        """
        with allure.step("登录"):
            LoginPage().login(driver, 'jay')
            sleep(10)
        with allure.step("断言图片"):
            assert LoginPage().login_avatar_assert(driver, "周杰伦个人页截图.png", "周杰伦头像截图.png") > 0.9
