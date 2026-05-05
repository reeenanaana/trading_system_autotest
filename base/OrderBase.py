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
