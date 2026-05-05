#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/5 16:06
# @Author: Rena

from base.ObjectMap import ObjectMap


class ExternalLinkPage(ObjectMap):

    def goto_imoc(self, driver):
        """
        切换窗口到慕课网
        :param driver:
        :return:
        """
        self.switch_window_2_latest_handle(driver)
        return driver.title
