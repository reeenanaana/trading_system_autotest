#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/4/28 23:11
# @Author: Rena
import unittest
from time import sleep

from config.driver_config import DriverConfig
from page.LoginPage import LoginPage


class TestLogin:

    def test_login(self, driver):
        # driver = DriverConfig().driver_config()
        LoginPage().login(driver, 'jay')
        sleep(3)
        # driver.quit()
