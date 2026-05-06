#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/6 14:06
# @Author: Rena

from time import sleep

import pytest

from config.driver_config import DriverConfig


class TestPytestMClass:

    @pytest.fixture(scope='class')
    def scope_class(self):
        print("我是class级别，我只执行一次")

    @pytest.fixture(scope='function')
    def driver(self):
        get_driver = DriverConfig().driver_config()
        return get_driver

    @pytest.mark.bilibili
    def test_open_bilibili(self, driver, scope_class):
        # driver = DriverConfig().driver_config()
        driver.get("https://www.bilibili.com/")
        sleep(3)
        driver.quit()

    @pytest.mark.baidu
    def test_open_baidu(self, driver, scope_class):
        print("test_open_baidu")
        # driver = DriverConfig().driver_config()
        driver.get("https://www.baidu.com")
        sleep(3)
        driver.quit()

    @pytest.mark.google
    def test_open_google(self, driver, scope_class):
        # driver = DriverConfig().driver_config()
        driver.get("https://www.google.com")
        sleep(3)
        driver.quit()
