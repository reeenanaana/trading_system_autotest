#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/4 17:16
# @Author: Rena

import pytest

from time import sleep

from page.LoginPage import LoginPage
from page.LeftMenuPage import LeftMenuPage
from page.GoodsPage import GoodsPage

goods_info_list = [
    {"goods_title": "新增批量商品测试1",
     "goods_details": "新增批量商品测试详情1",
     "goods_quantity": 1,
     "goods_pic_list": ['商品图片一.jpg'],
     "goods_price": 100,
     "goods_status": "上架",
     "bottom_button_name": "提交"
     },
    {"goods_title": "新增批量商品测试2",
     "goods_details": "新增批量商品测试详情2",
     "goods_quantity": 2,
     "goods_pic_list": ['商品图片二.jpg'],
     "goods_price": 200,
     "goods_status": "上架",
     "bottom_button_name": "提交"
     }
]


class TestAddGoods:
    @pytest.mark.parametrize("goods_info", goods_info_list)
    def test_add_goods_1(self, driver, goods_info):
        # driver = DriverConfig().driver_config()
        LoginPage().login(driver, 'jay')
        LeftMenuPage().click_level_one_menu(driver, '产品')
        sleep(1)
        LeftMenuPage().click_level_two_menu(driver, "新增二手商品")
        sleep(1)
        # GoodsPage().add_new_goods(
        #     driver,
        #     goods_title='新增商品测试-Rena',
        #     goods_details='新增商品测试详情-Rena',
        #     goods_quantity=1,
        #     goods_pic_list=['商品图片一.jpg'],
        #     goods_price=999,
        #     goods_status='上架',
        #     bottom_button_name='提交'
        # )
        GoodsPage().add_new_goods(
            driver,
            goods_title=goods_info['goods_title'],
            goods_details=goods_info['goods_details'],
            goods_quantity=goods_info['goods_quantity'],
            goods_pic_list=goods_info['goods_pic_list'],
            goods_price=goods_info['goods_price'],
            goods_status=goods_info['goods_status'],
            bottom_button_name=goods_info['bottom_button_name']
        )
        sleep(5)
        # driver.quit()
