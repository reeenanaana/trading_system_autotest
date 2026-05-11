#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/10 16:48
# @Author: Rena

import time
import os
from common.find_img import FindImg
from common.tools import get_project_path, get_screenshot_path, get_target_img_path


def get_img_path(img_name):
    """
    获取商品图片的路径
    :param img_name:
    :return:
    """
    img_dir_path = get_project_path(project_name='trading_system_autotest') / 'img' / img_name
    return str(img_dir_path)  # 2026.5.4修改 ObjectMap().upload()方法的必参file_path必须为str


def get_screenshot_path(img_name):
    """
    图像识别时，获取截图的路径
    :param img_name:
    :return:
    """
    screenshot_dir_path = get_project_path(project_name='trading_system_autotest') / 'img' / 'screenshots' / img_name
    return str(screenshot_dir_path)


def get_target_img_path(img_name):
    """
    图像识别是，获取需要查找的图片的路径
    :param img_name:
    :return:
    """
    target_img_path = get_project_path(project_name='trading_system_autotest') / 'img' / 'target_imgs' / img_name
    return str(target_img_path)


def login(self, driver, user):
    """
    登录
    :param driver:
    :param user:
    :return:
    """
    self.element_to_url(driver, "/login")
    username, password = GetConf().get_username_password(user)
    self.login_input_value(driver, "用户名", username)
    self.login_input_value(driver, "密码", password)
    self.click_login(driver, "登录")


def login_avatar_assert(self, driver, img_name):
    """
    登录后判断头像
    :param driver:
    :param img_name:
    :return:
    """
    return self.find_img_in_screenshot(driver, img_name)


import aircv as ac


# from common.tools import get_img_path


class FindImg:
    def img_imread(self, img_path):
        """
        读取图片
        :param img_path:
        :return:
        """
        return ac.imread(img_path)

    def get_confidence(self, screenshot_path, target_img_path):
        """
        查找图片
        :param screenshot_path:原图路径
        :param target_img_path: 需要查找的图片的路径
        :return:
        """
        img_src = self.img_imread(screenshot_path)
        img_tar = self.img_imread(target_img_path)
        result = ac.find_template(img_src, img_tar)
        print(result)
        return result['confidence']


def find_img_in_screenshot(self, driver, img_name):
    """
    截图并在截图中查找图片
    :param driver:
    :param img_name:
    :return:
    """
    # 截图后图片保存的路径（大图）
    screenshot_path = get_screenshot_path(img_name)
    # 需要查找的图片的路径
    target_img_path = get_target_img_path(img_name)
    # 截图后保存图片到screenshot_path路径下
    png_bytes = driver.get_screenshot_as_png()
    os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
    with open(screenshot_path, 'wb') as f:
        f.write(png_bytes)
        time.sleep(3)
    # 在截图中查找是否有指定的图片，返回信心值
    confidence = FindImg().get_confidence(screenshot_path, target_img_path)
    return confidence
