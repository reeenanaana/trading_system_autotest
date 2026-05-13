#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/4/28 23:11
# @Author: Rena
from time import sleep

import pytest
import allure

# from config.driver_config import DriverConfig
from page.LoginPage import LoginPage
from common.report_add_img import add_img_to_report


class TestLogin:
    @pytest.mark.login
    @allure.feature('登录')
    def test_login_failure(self, driver):
        """使用错误的账号登录"""
        with allure.step('登录'):
            # driver = DriverConfig().driver_config()
            # 注释掉了，因为有conftest.py中有driver的夹具可以用
            LoginPage().login(driver, 'failure')
            sleep(3)
            add_img_to_report(driver, '登录')
            # driver.quit()

    def test_login_success(self, driver):
        """使用正确的账号登录"""
        with allure.step('登录'):
            LoginPage().login(driver, 'jay')
            sleep(3)
            add_img_to_report(driver, '登录')
