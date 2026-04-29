#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/4/28 15:18
# @Author: Rena

"""
验证 Selenium 环境和浏览器驱动是否能正常工作
"""
#
# from time import sleep
#
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
#
# from common.tools import get_project_path
#
# service_path = get_project_path("trading_system_autotest") / "drivers" / "chromedriver"
# service = Service(service_path)
#
# chrome_options = Options()
# #   设置窗口大小1920*1080
# chrome_options.add_argument('--window-size=1920,1080')
# #   最大化窗口
# # chrome_options.add_argument('--start-maximized')
# #   去除“chrome正受到自动测试软件的控制”的提示
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# #   解决selenium无法访问https的问题
# chrome_options.add_argument("--ignore-certificate-errors")
# #   允许忽略Localhost上的TLS/SSL错误
# chrome_options.add_argument("--allow-insecure-localhost")
# #   设置为无痕模式
# chrome_options.add_argument("--incognito")
# #   设置为无头模式，启用无头模式（不显示浏览器界面），在高并发或服务器环境下使用。
# # chrome_options.add_argument("--headless")
# #   解决卡顿1:禁用沙盒模式，用于在 Linux 系统以 root 权限运行。
# chrome_options.add_argument("--no-sandbox")
# #   解决卡顿2:禁用 GPU 加速，在 Linux 虚拟环境或无头模式下可防卡死。
# chrome_options.add_argument("--disable-gpu")
# #   解决卡顿3：禁用 / dev / shm（共享内存），解决Docker容器中内存不足导致浏览器崩溃的问题
# chrome_options.add_argument("--disable-dev-shm-usage")
#
# driver = webdriver.Chrome(service=service, options=chrome_options)
# driver.get("http://192.168.64.1")
# sleep(5)
# driver.quit()
