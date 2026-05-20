#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/4/28 23:11
# @Author: Rena
from time import sleep

import pytest
import allure

from common.report_add_img import add_img_to_report


class TestLogin:
    @pytest.mark.login
    @allure.feature('登录')
    def test_login_failure(self, driver, test_objects):
        """使用错误的账号登录"""
        with allure.step('登录'):
            test_objects.login_page.login(driver, 'failure', assert_success=False)
            sleep(3)
            assert not test_objects.login_page.is_login_success_displayed(driver)
            add_img_to_report(driver, '登录')

    def test_login_success(self, driver, test_objects):
        """使用正确的账号登录"""
        with allure.step('登录'):
            test_objects.login_page.login(driver, 'jay')
            sleep(3)
            add_img_to_report(driver, '登录')
