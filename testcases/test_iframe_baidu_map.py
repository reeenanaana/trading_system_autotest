#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/5 18:29
# @Author: Rena

from time import sleep


class TestIframeBaiduMap:
    def test_iframe_baidu_map(self, driver, test_objects):
        test_objects.login_page.login(driver, 'william')
        sleep(2)
        test_objects.left_menu_page.click_level_one_menu(driver, 'iframe测试')
        sleep(1)
        test_objects.iframe_baidu_map_page.switch_2_baidu_map_iframe(driver)
        sleep(10)
        test_objects.iframe_baidu_map_page.get_baidu_map_search_button(driver)
        sleep(3)
        test_objects.iframe_baidu_map_page.iframe_out(driver)
        sleep(3)
        test_objects.left_menu_page.click_level_one_menu(driver, '首页')
        sleep(3)
