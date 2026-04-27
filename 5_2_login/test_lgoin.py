#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/4/24 12:17
# @Author: Rena

from time import sleep

from config.driver_config import DriverConfig

from selenium.webdriver.common.by import By

driver = DriverConfig().driver_config()
driver.get("http://192.168.64.1")
sleep(2)
driver.find_element(By.XPATH, "//input[@placeholder='用户名']").send_keys("周杰伦")
sleep(1)
driver.find_element(By.XPATH,"//input[@placeholder='密码']").send_keys("123456")
sleep(1)
driver.find_element(By.XPATH,"//span[text()='登录']/parent::button").click()
sleep(2)
# driver.quit()
