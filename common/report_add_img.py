#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/11 16:56
# @Author: Rena

from time import sleep

import allure


def add_img_to_report(driver, step_name, need_sleep=True):
    """
    截图并插入allure报告
    :param driver:
    :param step_name:
    :param need_sleep:
    :return:
    """
    if need_sleep:
        sleep(3)
    allure.attach(
        driver.get_screenshot_as_png(),
        step_name + ".png",
        allure.attachment_type.PNG
    )
