#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/5 17:48
# @Author: Rena

from selenium.webdriver.common.by import By

from base.ObjectMap import ObjectMap
from base.AccountBase import AccountBase
from common.tools import get_img_path


class AccountPage(ObjectMap, AccountBase):
    def upload_avatar(self, driver, image_name):
        """
        上传个人头像
        :param driver:
        :param image_name:
        :return:
        """
        img_path = get_img_path(image_name)
        upload_xpath = self.get_basic_info_avatar_locator()
        return self.upload(driver, By.XPATH, upload_xpath, img_path)

    def click_save(self, driver):
        """
        个人资料-点击保存
        :param driver:
        :return:
        """
        button_xpath = self.get_basic_info_save_button_locator()
        return self.element_click(driver, By.XPATH, button_xpath)
