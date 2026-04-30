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
        return "//span[starts-with(text(),'欢迎您回来')]"  # 定位起始文本 starts-with(text(),'起始文本')

    def show_date(self):
        """
        首页显示日期
        :return:
        """
        return "//div[@class='calender']/following-sibling::div"

    def home_user_avatar(self):
        """
        首页用户头像大图
        :return:
        """
        return "//span[contains(text(),"欢迎您回来")]/parent::div/preceding-sibling::div"

    def home_user_avatar_2(self):
        """
        首页用户头像大图二
        :return:
        """
        return "//span[text()='我的地址']/ancestor::div[@class='first_card']/div[contains(@class,'avatar')]//img"