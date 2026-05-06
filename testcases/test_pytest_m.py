#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/6 14:06
# @Author: Rena

from time import sleep

import pytest

from config.driver_config import DriverConfig


class TestPytestMClass:
    @pytest.mark.bilibili
    def test_open_bilibili(self):
        driver = DriverConfig().driver_config()
        driver.get("https://www.bilibili.com/")
        sleep(3)
        driver.quit()

    @pytest.mark.baidu
    def test_open_baidu(self):
        print("test_open_baidu")
        driver = DriverConfig().driver_config()
        driver.get("https://www.baidu.com")
        sleep(3)
        driver.quit()

    @pytest.mark.google
    def test_open_google(self):
        driver = DriverConfig().driver_config()
        driver.get("https://www.google.com")
        sleep(3)
        driver.quit()