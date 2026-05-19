#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/6 14:06
# @Author: Rena

from time import sleep

import pytest


class TestPytestMClass:

    @pytest.fixture(scope='class')
    def scope_class(self):
        print("我是class级别，我只执行一次")

    @pytest.mark.bilibili
    def test_open_bilibili(self, driver, scope_class):
        driver.get("https://www.bilibili.com/")
        sleep(3)

    @pytest.mark.baidu
    def test_open_baidu(self, driver, scope_class):
        print("test_open_baidu")
        driver.get("https://www.baidu.com")
        sleep(3)

    @pytest.mark.google
    def test_open_google(self, driver, scope_class):
        driver.get("https://www.google.com")
        sleep(3)
