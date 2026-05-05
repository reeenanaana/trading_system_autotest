#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/5 18:26
# @Author: Rena

from selenium.webdriver.common.by import By

from base.ObjectMap import ObjectMap
from base.IframeBaiduMapBase import IframeBaiduMapBase


class IframeBaiduMapPage(IframeBaiduMapBase, ObjectMap):
    def get_baidu_map_search_button(self, driver):
        """
        获取百度地图搜索按钮
        :param driver:
        :return:
        """
        button_xpath = self.get_search_button_locator()
        return self.element_get(driver, By.XPATH, button_xpath)

    def switch_2_baidu_map_iframe(self, driver):
        """
        切换到百度地图的iframe
        :param driver:
        :return:
        """
        iframe_xpath = self.get_baidu_map_iframe()
        return self.switch_into_iframe(driver, By.XPATH, iframe_xpath)

    def iframe_out(self, driver):
        """
        从百度地图iframe切回校园二手交易系统
        :param driver:
        :return:
        """
        return self.switch_from_iframe_to_contnet(driver)
