#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/15 15:42
# @Author: Rena

from selenium.webdriver.common.by import By

from base.HomeBase import HomeBase
from base.ObjectMap import ObjectMap


class HomePage(HomeBase, ObjectMap):
    def get_user_balance(self, driver):
        """
        获取首页的账户余额
        :return:
        """
        balance_xpath = self.user_balance()
        # 获得元素后，{元素}.text就可以获取余额的文本
        return self.element_get(driver, By.XPATH, balance_xpath).text
