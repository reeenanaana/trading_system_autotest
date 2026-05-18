#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/18 13:48
# @Author: Rena

from time import sleep

from selenium.webdriver.common.by import By

from base.ObjectMap import ObjectMap
from base.TradingMarketBase import TradingMarketBase
from logs.log import log


class TradingMarketPage(TradingMarketBase, ObjectMap):
    def fill_search_input(self, driver, input_value):
        """
        输入搜索宝贝输入框
        :param driver:
        :param input_value:
        :return:
        """
        log.info(f"在搜索宝贝输入框输入 + {input_value}")
        search_input_xpath = self.search_input()
        return self.element_fill_value(driver, By.XPATH, search_input_xpath, input_value)

    def click_search_button(self, driver):
        """
        点击搜索按钮
        :param driver:
        :return:
        """
        log.info("点击搜索按钮")
        search_button_xpath = self.search_button()
        return self.element_click(driver, By.XPATH, search_button_xpath)

    def click_product_card(self, driver, product_name):
        """
        点击商品卡片
        :param driver:
        :param product_name:
        :return:
        """
        log.info(f"点击{product_name}的商品卡片")
        product_card_xpath = self.product_card(product_name)
        return self.element_click(driver, By.XPATH, product_card_xpath)

    def click_i_want(self, driver):
        """
        点击我想要
        :param driver:
        :return:
        """
        log.info("点击我想要")
        i_want_button_xpath = self.i_want_button()
        self.scroll_to_element(driver, By.XPATH, i_want_button_xpath)
        return self.element_click(driver, By.XPATH, i_want_button_xpath)

    def click_address_input(self, driver):
        """
        点击收货地址输入框
        :param driver:
        :return:
        """
        log.info("点击收货地址输入框")
        receiving_address_input_xpath = self.receiving_address_input()
        return self.element_click(driver, By.XPATH, receiving_address_input_xpath)

    def select_receiving_address(self, driver, num, address=None):
        """
        选择收货地址
        :param driver:
        :param num:收货地址序号
        :param address:具体的收货地址
        :return:
        """
        if address:
            log.info(f"选择收货地址+{address}")
            receiving_address_xpath = self.receiving_address_option(0, address=address)
        else:
            log.info(f"选择选项中的第{num}个收获地址")
            receiving_address_xpath = self.receiving_address_option(num)
        return self.element_click(driver, By.XPATH, receiving_address_xpath)

    def click_confirm_button(self, driver):
        """
        点击确定按钮
        :param driver:
        :return:
        """
        log.info("点击确定按钮")
        confirm_button_xpath = self.confirm_button()
        return self.element_click(driver, By.XPATH, confirm_button_xpath)
