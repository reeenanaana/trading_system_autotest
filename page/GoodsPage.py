#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/4 13:00
# @Author: Rena

from time import sleep

from selenium.webdriver.common.by import By

from base.ObjectMap import ObjectMap
from base.GoodsBase import GoodsBase
from common.tools import get_img_path


class GoodsPage(GoodsBase, ObjectMap):
    def input_goods_title(self, driver, input_value):
        """
        输入商品标题
        :param driver:
        :param input_value:
        :return:
        """
        goods_title_xpath = self.get_goods_title_locator()
        return self.element_fill_value(driver, By.XPATH, goods_title_xpath, input_value)

    def input_goods_details(self, driver, input_value):
        """
        输入商品详情
        :param driver:
        :param input_value:
        :return:
        """
        goods_details_xpath = self.get_goods_details_locator()
        return self.element_fill_value(driver, By.XPATH, goods_details_xpath, input_value)

    def select_goods_quantity(self, driver, quantity):
        """
        选择商品数量
        :param driver:
        :param quantity:
        :return:
        """
        goods_quantity_add_xpath = self.get_goods_quantity_locator(symbol='plus')
        for i in range(quantity):
            self.element_click(driver, By.XPATH, goods_quantity_add_xpath)
            sleep(1)

    def upload_goods_img(self, driver, img_name):
        """
        上传商品图片
        :param driver:
        :param img_name:
        :return:
        """
        img_path = get_img_path(img_name)
        upload_xpath = self.get_goods_img_locator()
        return self.upload(driver, By.XPATH, upload_xpath, img_path)

    def input_goods_price(self, driver, input_value):
        """
        输入商品单价
        :param driver:
        :param input_value:
        :return:
        """
        goods_price_xpath = self.get_goods_price_locator()
        return self.element_fill_value(driver, By.XPATH, goods_price_xpath, input_value)

    def select_goods_status(self, driver, option_name):
        """
        选择商品状态
        :param driver:
        :param option_name:上架/下架
        :return:
        """
        goods_status_xpath = self.get_goods_status_locator()
        self.element_click(driver, By.XPATH, goods_status_xpath)
        sleep(1)
        goods_status_option_xpath = self.get_goods_status_option_locator(option_name)
        return self.element_click(driver, By.XPATH, goods_status_option_xpath)

    def click_bottom_button(self, driver, button_name):
        """
        点击底部按钮
        :param driver:
        :param button_name:提交/重置
        :return:
        """
        button_xpath = self.get_add_goods_bottom_button_locator(button_name)
        return self.element_click(driver, By.XPATH, button_xpath)

    def add_new_goods(self, driver, goods_title, goods_details, goods_quantity, goods_pic_list, goods_price, goods_status,
                      bottom_button_name):
        """
        新增二手商品
        :param driver:
        :param goods_title:
        :param goods_details:
        :param goods_quantity:
        :param goods_pic_list:
        :param goods_price:
        :param goods_status:上架/下架
        :param bottom_button_name:提交/重置
        :return:
        """
        self.input_goods_title(driver, goods_title)
        self.input_goods_details(driver, goods_details)
        self.select_goods_quantity(driver, goods_quantity)
        for goods_pic in goods_pic_list:
            self.upload_goods_img(driver, goods_pic)
            sleep(5)
        self.input_goods_price(driver, goods_price)
        self.select_goods_status(driver, goods_status)
        self.click_bottom_button(driver, bottom_button_name)
        return True
