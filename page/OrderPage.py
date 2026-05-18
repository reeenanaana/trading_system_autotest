#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/5 17:00
# @Author: Rena

from selenium.webdriver.common.by import By

from base.ObjectMap import ObjectMap
from base.OrderBase import OrderBase
from logs.log import log


class OrderPage(OrderBase, ObjectMap):
    def click_order_tab(self, driver, tab_name):
        """
        点击订单tab栏按钮
        :param driver:
        :param tab_name:
        :return:
        """
        tab_xpath = self.get_order_tab_locator(tab_name)
        return self.element_click(driver, By.XPATH, tab_xpath)

    def click_order_operation(self, driver, product_title, operation):
        """
        点击订单的操作按钮
        :param driver:
        :param product_title:
        :param operation:去支付/去发货/去评价等
        :return:
        """
        log.info(f"订单标题为'{product_title}'，点击订单的操作按钮'{operation}''")
        operation_button_xpath = self.order_operation_button(product_title, operation)
        self.scroll_to_element(driver, By.XPATH, operation_button_xpath)
        return self.element_click(driver, By.XPATH, operation_button_xpath)

    def click_operation_confirm_button(self, driver):
        """
        点击订单操作按钮后，点击弹窗中的确认按钮
        :param driver:
        :return:
        """
        log.info("点击订单操作按钮后，点击弹窗中的确认按钮")
        confirm_button_xpath = self.order_operation_confirm_button()
        return self.element_click(driver, By.XPATH, confirm_button_xpath)

    def click_logistics_input(self, driver):
        """
        点击物流公司选择框
        :param driver:
        :return:
        """
        log.info("点击物流公司选择框")
        logistics_input_xpath = self.logistics_input()
        return self.element_click(driver, By.XPATH, logistics_input_xpath)

    def select_logistics_company(self, driver, logistics_company):
        """
        选择物流公司
        :param driver:
        :param logistics_company: 物流公司
        :return:
        """
        log.info("选择物流公司")
        logistics_option_xpath = self.logistics_options(logistics_company)
        return self.element_click(driver, By.XPATH, logistics_option_xpath)

    def fill_tracking_number(self, driver, tracking_number):
        """
        填入物流单号
        :param driver:
        :param tracking_number:
        :return:
        """
        log.info(f"填入物流单号: {tracking_number}")
        tracking_number_input_xpath = self.tracking_number_input()
        return self.element_fill_value(driver, By.XPATH, tracking_number_input_xpath, tracking_number)

    def click_rating_stars(self, driver, num):
        """
        点击评价星级
        :param driver:
        :param num: 几颗星
        :return:
        """
        log.info(f"评价星级: {num}星")
        stars_xpath = self.rating_stars(num)
        self.scroll_to_element(driver, By.XPATH, stars_xpath)
        return self.element_click(driver, By.XPATH, stars_xpath)

    def click_evaluation_confirm_button(self, driver):
        """
        点击星级后，点击确认按钮
        :param driver:
        :return:
        """
        log.info("点击星级后，点击确认按钮")
        evaluation_confirm_button_xpath = self.evaluation_confirm_button()
        return self.element_click(driver, By.XPATH, evaluation_confirm_button_xpath)
