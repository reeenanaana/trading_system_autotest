#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/14 11:52
# @Author: Rena
import unittest

from time import sleep

import pytest
import allure

from common.report_add_img import add_img_to_report
from page.LoginPage import LoginPage


class TestCaptchaLogin:
    @pytest.mark.login
    @allure.feature("登录")
    @allure.description('验证码登录')
    def test_captcha_login(self, driver):
        """
        测试验证码登录
        :param driver:
        :return:
        """
        with allure.step("登录"):
            LoginPage().login(driver, 'jay', need_captcha=True)
            sleep(2)
            add_img_to_report(driver, '登录')
