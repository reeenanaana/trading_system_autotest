#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/17 13:14
# @Author: Rena

from time import sleep

import pytest
import allure

from common.report_add_img import add_img_to_report
from common.tools import get_now_date_time_str


class TestTradingFlow:
    @pytest.mark.trading_flow
    @allure.feature("交易流")
    @allure.description("交易流")
    def test_trading_flow(self, driver, test_objects):
        """
        交易流
        :param driver:
        :return:
        """
        with allure.step("登录卖家"):
            test_objects.login_page.api_login(driver, "jay")
            add_img_to_report(driver, "登录卖家")

        with allure.step("进入新增二手商品（二级菜单）"):
            test_objects.left_menu_page.click_level_one_menu(driver, "产品")
            sleep(1)
            test_objects.left_menu_page.click_level_two_menu(driver, "新增二手商品")
            sleep(2)
            add_img_to_report(driver, "进入新增二手商品")

        with allure.step("新增商品"):
            goods_title = f"交易流测试+{get_now_date_time_str()}"
            test_objects.goods_page.add_new_goods(
                driver,
                goods_title,
                goods_details="交易流测试",
                goods_quantity=1,
                goods_pic_list=["商品图片三.jpg"],
                goods_price=199,
                goods_status='上架',
                bottom_button_name='提交'
            )
            add_img_to_report(driver, '新增商品')
            sleep(5)

        with allure.step("登录买家"):
            test_objects.login_page.api_login(driver, "william")
            add_img_to_report(driver, "登录买家")

        with allure.step("进入交易市场"):
            test_objects.left_menu_page.click_level_one_menu(driver, "交易市场")
            add_img_to_report(driver, "进入交易市场")

        with allure.step("搜索宝贝"):
            test_objects.trading_market_page.fill_search_input(driver, goods_title)
            test_objects.trading_market_page.click_search_button(driver)
            add_img_to_report(driver, "搜索宝贝")

        with allure.step("点击商品卡片"):
            test_objects.trading_market_page.click_product_card(driver, goods_title)
            sleep(1)
            add_img_to_report(driver, "点击商品卡片")

        with allure.step("点击‘我想要’"):
            test_objects.trading_market_page.click_i_want(driver)
            sleep(1)
            add_img_to_report(driver, "点击我想要")

        with allure.step("选择收货地址"):
            test_objects.trading_market_page.click_address_input(driver)
            sleep(1)
            test_objects.trading_market_page.select_receiving_address(driver, 1)
            add_img_to_report(driver, "选择收货地址")

        with allure.step("点击确定"):
            test_objects.trading_market_page.click_confirm_button(driver)
            sleep(1)
            add_img_to_report(driver, "点击确定")

        with allure.step("买家支付"):
            test_objects.order_page.click_order_operation(driver, goods_title, "去支付")
            sleep(1)
            test_objects.order_page.click_operation_confirm_button(driver)
            add_img_to_report(driver, "买家支付")

        with allure.step("登录卖家"):
            test_objects.login_page.api_login(driver, "jay")
            add_img_to_report(driver, "登录卖家")

        with allure.step("进入已卖出的宝贝"):
            test_objects.left_menu_page.click_level_one_menu(driver, "我的订单")
            sleep(1)
            test_objects.left_menu_page.click_level_two_menu(driver, "已卖出的宝贝")
            sleep(2)
            add_img_to_report(driver, "进入界面-已卖出的宝贝")

        with allure.step("卖家发货"):
            test_objects.order_page.click_order_operation(driver, goods_title, "去发货")
            sleep(1)
            test_objects.order_page.click_logistics_input(driver)
            sleep(1)
            test_objects.order_page.select_logistics_company(driver, '圆通速递')
            sleep(1)
            test_objects.order_page.fill_tracking_number(driver, "YT7621463542605")
            sleep(1)
            test_objects.order_page.click_operation_confirm_button(driver)
            add_img_to_report(driver, "卖家发货")
            sleep(3)

        with allure.step("登录买家"):
            test_objects.login_page.api_login(driver, "william")
            add_img_to_report(driver, "登录买家")

        with allure.step("进入已买到的宝贝"):
            test_objects.left_menu_page.click_level_one_menu(driver, "我的订单")
            sleep(1)
            test_objects.left_menu_page.click_level_two_menu(driver, "已买到的宝贝")
            sleep(1)
            add_img_to_report(driver, "进入界面-已买到的宝贝")

        with allure.step("买家确认收货"):
            test_objects.order_page.click_order_operation(driver, goods_title, "去确认收货")
            sleep(1)
            test_objects.order_page.click_operation_confirm_button(driver)
            add_img_to_report(driver, "买家确认收货")

        with allure.step("买家评价"):
            test_objects.order_page.click_order_operation(driver, goods_title, "去评价")
            sleep(1)
            test_objects.order_page.click_rating_stars(driver, 1)
            sleep(1)
            test_objects.order_page.click_evaluation_confirm_button(driver)
            sleep(1)
            add_img_to_report(driver, "买家评价")
