#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/6 18:44
# @Author: Rena

import pytest

from config.driver_config import DriverConfig


@pytest.fixture()
def driver():
    get_driver = DriverConfig().driver_config()
    yield get_driver
    get_driver.quit()
