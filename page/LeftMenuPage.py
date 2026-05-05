#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/3 23:03
# @Author: Rena

from selenium.webdriver.common.by import By

from base.LeftMenuBase import LeftMenuBase
from base.ObjectMap import ObjectMap


class LeftMenuPage(LeftMenuBase, ObjectMap):

    def click_level_one_menu(self, driver, menu_name):
        """
        点击一级菜单
        :param driver: 浏览器驱动
        :param menu_name: 菜单栏名称
        :return:
        """
        menu_xpath = self.level_one_menu(menu_name)
        return self.element_click(driver, By.XPATH, menu_xpath)

    def click_level_two_menu(self, driver, menu_name):
        """
        点击二级菜单
        :param driver: 浏览器驱动
        :param menu_name: 菜单栏名称
        :return:
        """
        menu_xpath = self.level_two_menu(menu_name)
        return self.element_click(driver, By.XPATH, menu_xpath)
