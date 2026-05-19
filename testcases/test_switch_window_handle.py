#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/5 16:10
# @Author: Rena

from time import sleep

import allure

from common.report_add_img import add_img_to_report


class TestWindowHandle:
    @allure.description("窗口句柄")
    @allure.epic("窗口句柄epic")
    @allure.feature("窗口句柄feature")
    @allure.story("窗口句柄story")
    @allure.tag('窗口句柄tag')
    def test_switch_window_handles(self, driver, test_objects):
        with allure.step("登录"):
            test_objects.login_page.login(driver, 'jay')
            sleep(3)
            add_img_to_report(driver, "登录")
        with allure.step("点击外链"):
            test_objects.left_menu_page.click_level_one_menu(driver, '外链')
            sleep(5)
            add_img_to_report(driver, "点击外链")

        with allure.step("断言title"):
            title = test_objects.external_link_page.goto_imoc(driver)
            print("title:", title)
            assert title == "慕课网-程序员的梦工厂"
