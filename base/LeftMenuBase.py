#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/4/30 12:04
# @Author: Rena

class LeftMenuBase:

    def level_one_menu(self, menu_name):
        """
        一级菜单栏
        :param menu_name:菜单栏名称
        :return:
        """
        return f"//aside[@class='el-aside']//span[text()='{menu_name}']/ancestor::li"

    def level_two_menu(self, menu_name):
        """
        二级菜单
        :param menu_name:菜单栏名称
        :return:
        """
        return f"//aside[@class='el-aside']//span[text()='{menu_name}']/parent::li"


if __name__ == '__main__':
    # print(LeftMenuBase().level_one_menu('产品'))
    print(LeftMenuBase().level_two_menu('新增二手商品'))
