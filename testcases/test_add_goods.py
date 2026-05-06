#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/4 17:16
# @Author: Rena

from time import sleep

import pytest

from config.driver_config import DriverConfig
from page.LoginPage import LoginPage
from page.LeftMenuPage import LeftMenuPage
from page.GoodsPage import GoodsPage


class TestAddGoods:
    @pytest.fixture()
    def driver(self):
        get_driver = DriverConfig().driver_config()
        yield get_driver
        get_driver.quit()

    def test_add_goods_1(self, driver):
        # driver = DriverConfig().driver_config()
        LoginPage().login(driver, 'jay')
        LeftMenuPage().click_level_one_menu(driver, '产品')
        sleep(1)
        LeftMenuPage().click_level_two_menu(driver, "新增二手商品")
        sleep(1)
        GoodsPage().add_new_goods(
            driver,
            goods_title='新增商品测试-Rena',
            goods_details='新增商品测试详情-Rena',
            goods_quantity=1,
            goods_pic_list=['商品图片一.jpg'],
            goods_price=999,
            goods_status='上架',
            bottom_button_name='提交'
        )
        sleep(5)
        # driver.quit()
