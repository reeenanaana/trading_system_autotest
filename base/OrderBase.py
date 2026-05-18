#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/5 16:57
# @Author: Rena

class OrderBase:
    def get_order_tab_locator(self, tab_name):
        """
        订单tab按钮
        :param tab_name:全部、待付款、待发货、运输中、待确认、待评价
        :return:
        """
        return f"//div[@role='tab' and text()='{tab_name}']"

    def order_operation_button(self, product_title, operation):
        """

        :param product_title:
        :param operation:去支付/去发货/去评价等
        :return: 先通过商品标题定位到订单再去找到对应的操作按钮
        """
        return f"//div[text()='{product_title}']/ancestor::tr//span[text()='{operation}']/parent::button"

    def order_operation_confirm_button(self):
        """
        点击操作按钮以后，弹窗的确定按钮
        :return:
        """
        return "//div[@class='el-dialog__wrapper' and contains(@style,'index')]//span[text()='确 定']"

    def logistics_input(self):
        """
        物流公司选择框的定位
        :return:
        """
        return "//label[text()='物流公司']/following-sibling::div//input[@placeholder='请选择']"

    def logistics_options(self, logistics_company):
        """
        物流公司选择框的选项
        :param logistics_company: 物流公司名称
        :return:
        """
        return f"//span[text()='{logistics_company}']/parent::li"

    def tracking_number_input(self):
        """
        物流单号输入框的定位
        :return:
        """
        return "//label[text()='物流单号']/following-sibling::div//input"

    def rating_stars(self, num):
        """
        星级评价
        :param num: 几颗星
        :return:
        """
        return f"//span[text()='请给卖家评价']/following-sibling::div/span[{num}]/i"

    def evaluation_confirm_button(self):
        """
        评价界面的确认按钮
        :return:
        """
        return "//span[text()='评价']/ancestor::div[@role='dialog']//span[text()='确 定']/parent::button"
