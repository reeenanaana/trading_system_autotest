#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/15 10:37
# @Author: Rena


from time import sleep

import pytest
import allure


class TestLoginByApi:
    @pytest.mark.login
    @allure.feature("api登录")
    @allure.description("api登录")
    def test_login_by_api(self, driver, test_objects):
        """
        api登录
        :param driver:
        :return:
        """
        with allure.step("登录jay"):
            test_objects.login_page.api_login(driver, "jay")
            sleep(5)

        with allure.step("切换用户到william"):
            test_objects.login_page.api_login(driver, "william")
            sleep(5)
