#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/5 18:29
# @Author: Rena

from time import sleep

from config.driver_config import DriverConfig
from page.LoginPage import LoginPage
from page.LeftMenuPage import LeftMenuPage
from page.IframeBaiduMapPage import IframeBaiduMapPage


class TestIframeBaiduMap:
    def test_iframe_baidu_map(self):
        driver = DriverConfig().driver_config()
        LoginPage().login(driver, 'william')
        sleep(2)
        LeftMenuPage().click_level_one_menu(driver, 'iframe测试')
        sleep(1)
        IframeBaiduMapPage().switch_2_baidu_map_iframe(driver)
        sleep(10)
        IframeBaiduMapPage().get_baidu_map_search_button(driver)
        sleep(3)
        IframeBaiduMapPage().iframe_out(driver)
        sleep(3)
        LeftMenuPage().click_level_one_menu(driver, '首页')
        sleep(3)
        driver.quit()

