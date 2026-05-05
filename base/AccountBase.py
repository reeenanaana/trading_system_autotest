#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/5 17:44
# @Author: Rena

class AccountBase:
    def get_basic_info_avatar_locator(self):
        """
        基本资料-个人头像
        :return:
        """
        return "//input[@type='file']"

    def get_basic_info_save_button_locator(self):
        """
        基本资料-保存按钮
        :return:
        """
        return "//span[text()='保存']/parent::button"
