#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/18 12:39
# @Author: Rena


class TradingMarketBase:
    def search_input(self):
        """
        返回搜索宝贝输入框定位表达式
        """
        return "//div[text()='搜索宝贝']/following-sibling::input"

    def search_button(self):
        """
        搜索按钮
        :return:
        """
        # return "//div[text()='搜索宝贝']/following-sibling::input/following-sibling::div"
        return self.search_input() + "/following-sibling::div"

    def product_card(self, product_name):
        """
        商品卡片
        :return:
        """
        return f"//div[text()='{product_name}']/ancestor::div[@class='el-card__body']"

    def i_want_button(self):
        """
        '我想要'按钮
        :return:
        """
        return "//span[text()='我想要']/parent::button"

    def quantity_up_and_down(self, quantity_decision):
        """
        购买数量上下按钮
        :param quantity_decision: up / down
        :return:
        """
        return f"//i[@class='el-icon-arrow-{quantity_decision}']/parent::span"

    def receiving_address_input(self):
        """
        收货地址输入框
        :return:
        """
        return "//input[@placeholder='收货地址']"

    def receiving_address_option(self, num, address=None):
        """
        收货地址选项
        :param num: 多个地址的时候，选择第一个地址则[1]
        :param address:直接传地址
        :return:
        """
        if address:
            return f"//span[contains(text(),{address})]/parent::li"
        else:
            return f"//ul[contains(@class, 'list')]/li[{num}]"

    def confirm_button(self):
        """
        确定按钮
        :return:
        """
        return "//span[text()='确 定']/parent::button"
