#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/5 17:08
# @Author: Rena

import pytest

from time import sleep

from config.driver_config import DriverConfig
from page.LeftMenuPage import LeftMenuPage
from page.LoginPage import LoginPage
from page.OrderPage import OrderPage

tab_list = ['全部', '待付款', '待发货', '运输中', '待确认', '待评价']


# 参数化后的测试用例执行和前面有for循环的形式不同。
# 参数化是点完“全部”后，关闭浏览器，再重复一遍后点“待付款”

class TestOrderPurchaseList():
    @pytest.mark.parametrize("tab", tab_list)
    def test_order_purchase_list(self, driver, tab):
        # driver = DriverConfig().driver_config()
        LoginPage().login(driver, 'william')
        LeftMenuPage().click_level_one_menu(driver, "我的订单")
        sleep(1)
        LeftMenuPage().click_level_two_menu(driver, "已买到的宝贝")
        sleep(2)
        # tab_list = ['全部', '待付款', '待发货', '运输中', '待确认', '待评价']
        # for tab_name in tab_list:
        OrderPage().click_order_tab(driver, tab)
        sleep(1)
        # driver.quit()
