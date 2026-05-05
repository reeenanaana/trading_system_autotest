#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/5 17:08
# @Author: Rena

from time import sleep

from config.driver_config import DriverConfig
from page.LeftMenuPage import LeftMenuPage
from page.LoginPage import LoginPage
from page.OrderPage import OrderPage


class TestOrderPurchaseList():
    def test_order_purchase_list(self):
        driver = DriverConfig().driver_config()
        LoginPage().login(driver, 'william')
        LeftMenuPage().click_level_one_menu(driver, "我的订单")
        sleep(1)
        LeftMenuPage().click_level_two_menu(driver, "已买到的宝贝")
        sleep(2)
        tab_list = ['全部', '待付款', '待发货', '运输中', '待确认', '待评价']
        for tab_name in tab_list:
            OrderPage().click_order_tab(driver, tab_name)
            sleep(1)
        driver.quit()
