#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/5 17:00
# @Author: Rena

from selenium.webdriver.common.by import By

from base.ObjectMap import ObjectMap
from base.OrderBase import OrderBase


class OrderPage(OrderBase, ObjectMap):
    def click_order_tab(self, driver, tab_name):
        """
        点击订单tab栏按钮
        :param driver:
        :param tab_name:
        :return:
        """
        tab_xpath = self.get_order_tab_locator(tab_name)
        return self.element_click(driver, By.XPATH, tab_xpath)
