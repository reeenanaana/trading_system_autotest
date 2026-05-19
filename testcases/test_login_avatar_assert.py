#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/9 17:42
# @Author: Rena

from time import sleep

import pytest
import allure


class TestLoginAvatarAssert:
    @pytest.mark.login
    @allure.feature('登录')
    @allure.description('登录后断言图片')
    def test_login_avatar_assert(self, driver, test_objects):
        """
        登录后断言图片
        :param driver:
        :return:
        """
        with allure.step("登录"):
            test_objects.login_page.login(driver, 'jay')
            sleep(10)
        with allure.step("断言图片"):
            assert test_objects.login_page.login_avatar_assert(driver, "周杰伦个人页截图.png", "周杰伦头像截图.png") > 0.9
