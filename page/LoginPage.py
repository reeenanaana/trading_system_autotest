#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/4/28 22:57
# @Author: Rena
from time import sleep

from selenium.webdriver.common.by import By

from base.LoginBase import LoginBase
from base.ObjectMap import ObjectMap
from common.yaml_config import GetConf
from logs.log import log
from common.report_add_img import add_specific_img_to_report
from common.ocr_identify import OcrIdentify


# 继承了LoginBase（元素定位）, ObjectMap（SE二次封装）
class LoginPage(LoginBase, ObjectMap):
    def login_input_value(self, driver, input_placeholder: str, input_value):
        """
        登录页输入值
        :param driver:
        :param input_placeholder:
        :param input_value:
        :return:
        """
        log.info("输入" + input_placeholder + "为" + str(input_value))
        input_xpath = self.login_input(input_placeholder)  # xpath定位表达式
        # driver.find_element(By.XPATH, input_xpath).send_keys(input_value)
        return self.element_fill_value(driver, By.XPATH, input_xpath, input_value)

    def click_login(self, driver, button_name):
        """
        点击登录
        :param driver:
        :param button_name:
        :return:
        """
        log.info("点击登录")
        button_xpath = self.login_button(button_name)
        # driver.find_element(By.XPATH, button_xpath).click()
        return self.element_click(driver, By.XPATH, button_xpath)

    def login(self, driver, user, need_captcha=False):
        """
        登录
        :param driver:
        :param user:
        :param need_captcha: 是否需要验证码
        :return:
        """
        log.info("跳转登录页")
        self.element_to_url(driver, "/login")
        # 确认是否需要验证码
        if need_captcha:
            sleep(3)
            log.info("需要验证码")
            self.select_need_captcha(driver)
            # 需要验证码则定位验证码元素位置
            captcha_xpath = self.captcha()
            # 找到验证码元素后，截图并存放到指定路径
            ele_screenshot_path = self.element_screenshot(driver, By.XPATH, captcha_xpath)
            # 将验证码截图添加到Allure报告中
            add_specific_img_to_report(ele_screenshot_path, '图像验证码')
            # 识别验证码截图中的text
            identify_result = OcrIdentify().identify(ele_screenshot_path)
            log.info(f"成功识别验证码为: {identify_result}")
            # 定位验证码输入框
            input_captcha_xpath = self.input_captcha()
            log.info("添入验证码")
            self.element_fill_value(driver, By.XPATH, input_captcha_xpath, identify_result)
            sleep(3)
        username, password = GetConf().get_username_password(user)
        self.login_input_value(driver, "用户名", username)
        self.login_input_value(driver, "密码", password)
        self.click_login(driver, "登录")
        self.assert_login_success(driver)

    def login_avatar_assert(self, driver, img_name):
        """
        登录后判断头像
        :param driver:
        :param img_name:
        :return:
        """
        return self.find_img_in_screenshot(driver, img_name)

    def assert_login_success(self, driver):
        """
        验证是否登录成功（是否有登录成功的标签）
        :param driver:
        :return:
        """
        success_xpath = self.login_success()
        self.element_appear(driver, By.XPATH, success_xpath, timeout=2)

    def select_need_captcha(self, driver):
        """
        点击勾选是否需要验证码
        :param driver:
        :return:
        """
        log.info("点击勾选是否需要验证码")
        select_captcha_xpath = self.select_captcha()
        return self.element_click(driver, By.XPATH, select_captcha_xpath)