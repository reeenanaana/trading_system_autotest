#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/4/28 23:11
# @Author: Rena
import unittest
from time import sleep

from config.driver_config import DriverConfig
from page.LoginPage import LoginPage


class TestLogin:

    def test_login(self):
        driver = DriverConfig().driver_config()
        driver.get("http://192.168.64.1")
        sleep(3)
        LoginPage().login_input_value(driver, '用户名', '周杰伦')
        sleep(1)
        LoginPage().login_input_value(driver, "密码", '123456')
        sleep(1)
        LoginPage().click_login(driver, "登录")
        sleep(5)
        driver.quit()

    