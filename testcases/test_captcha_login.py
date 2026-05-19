#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/14 11:52
# @Author: Rena
import unittest

from time import sleep

import pytest
import allure

from common.report_add_img import add_img_to_report


class TestCaptchaLogin:
    @pytest.mark.login
    @allure.feature("登录")
    @allure.description('验证码登录')
    def test_captcha_login(self, driver, test_objects):
        """
        测试验证码登录
        :param driver:
        :return:
        """
        with allure.step("登录"):
            test_objects.login_page.login(driver, 'jay', need_captcha=True)
            sleep(2)
            add_img_to_report(driver, '登录')
