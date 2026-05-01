#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/4/28 22:57
# @Author: Rena

from selenium.webdriver.common.by import By

from base.LoginBase import LoginBase


class LoginPage(LoginBase):
    def login_input_value(self, driver, input_placeholder: str, input_value):
        """
        登录页输入值
        :param driver:
        :param input_placeholder:
        :param input_value:
        :return: 
        """

        input_xpath = self.login_input(input_placeholder)
        driver.find_element(By.XPATH, input_xpath).send_keys(input_value)

    def click_login(self, driver, button_name):
        """
        点击登录
        :param driver:
        :param button_name:
        :return:
        """
        button_xpath = self.login_button(button_name)
        driver.find_element(By.XPATH, button_xpath).click()
