#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/5 18:21
# @Author: Rena

class IframeBaiduMapBase:
    def get_search_button_locator(self):
        """
        获取iframe页面内搜索按钮定位表达式
        :return:
        """
        return "//button[@id='search-button']"

    def get_baidu_map_iframe(self):
        """

        :return:
        """
        return "//iframe[@src='https://map.baidu.com/']"
