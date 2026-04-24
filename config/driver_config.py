#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/4/24 11:47
# @Author: Rena

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class DriverConfig:
    def driver_config(self):
        """
        浏览器驱动（使用 selenium-manager 自动管理 ChromeDriver）
        :return:
        """
        options = Options()
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-insecure-localhost")
        options.add_argument("--incognito")
        # options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # 关键修改：指定你下载的 chromedriver 的完整路径
        chrome_driver_path = "/Users/zhaoyang/file/project/python/pythonProject/trading_system_autotest/drivers/chromedriver"  # 改成你的实际路径
        service = Service(chrome_driver_path)

        # Service() 不传任何参数，selenium-manager 自动下载匹配版本的 ChromeDriver
        driver = webdriver.Chrome(service=service, options=options)
        driver.delete_all_cookies()

        return driver


if __name__ == '__main__':
    DriverConfig().driver_config()
    