#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/5 17:55
# @Author: Rena

from time import sleep


class TestPersonalInfo:
    def test_upload_personal_avatar(self, driver, test_objects):
        test_objects.login_page.login(driver, 'jay')
        test_objects.left_menu_page.click_level_one_menu(driver, '账户设置')
        sleep(1)
        test_objects.left_menu_page.click_level_two_menu(driver, '个人资料')
        sleep(3)
        test_objects.account_page.upload_avatar(driver, '个人头像二.jpg')
        sleep(3)
        test_objects.account_page.click_save(driver)
        sleep(3)
