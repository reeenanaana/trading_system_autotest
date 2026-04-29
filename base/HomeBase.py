#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/4/29 22:47
# @Author: Rena

class HomeBase:
    def wallet_switch(self):
        """
        首页的钱包开关
        :return:
        """
        return "//span[contains(@class,'switch')]"  # 定位属性 contains(@属性名,'值')

    def logo(self):
        """
        进入系统后，首页的logo
        :return:
        """
        return "//div[contains(text(),'二手')]"  # 定位文本 contains(text(),'值')

    def welcome(self):
        """
        首页，欢迎您回来
        :return:
        """
        return "//span[starts-with(text(),'欢迎您回来')]"    # 定位起始文本 starts-with(text(),'起始文本')
