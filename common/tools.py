import datetime
import os
from pathlib import Path

import requests


def get_now_time():
    return datetime.datetime.now()


def get_now_date_time_str():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


# 下面这个方法已经落伍了
# def get_project_path():
#     """
#     获取项目绝对路径
#     :return:
#     """
#     project_name = "trading_system_autotest"
#     file_path = os.path.dirname(__file__)
#     return file_path[:file_path.find(project_name) + len(project_name)]
#
# def sep(path, add_sep_before=False, add_sep_after=False):
#     all_path = os.sep.join(path)
#     if add_sep_before:
#         all_path = os.sep + all_path
#     if add_sep_after:
#         all_path = all_path + os.sep
#     return all_path

def get_project_path(project_name: str) -> Path:
    # -> Path 是 Python 的类型注解（Type Hint），表示这个函数的返回值类型是 Path 对象。
    """
    获取项目绝对路径
    :param project_name: 项目文件夹名称
    :return: Path 对象
    """
    current = Path(__file__).resolve()
    for parent in current.parents:
        if parent.name == project_name:
            return parent
    # 兜底：向上退2层（假设当前在 common/ 目录下）
    # 如果前面找到了文件目录，那这个下面这个return就不会执行了。
    # 这是一个经典的 "守卫语句"（Guard Clause）模式。一旦 return 被执行，函数就会立即结束，后面的代码不会再运行。
    return Path(__file__).parent.parent


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
    图像识别时，存放截图的路径
    :param img_name:
    :return:
    """
    screenshot_dir_path = get_project_path(project_name='trading_system_autotest') / 'img' / 'screenshots' / img_name
    return str(screenshot_dir_path)


def get_target_img_path(img_name):
    """
    图像识别时，存放需要查找的图片的路径
    :param img_name:
    :return:
    """
    target_img_path = get_project_path(project_name='trading_system_autotest') / 'img' / 'target_imgs' / img_name
    return str(target_img_path)


def get_ele_screenshot_path(ele_screenshot_name):
    """
    元素截图的存放路径
    :param ele_screenshot_name:
    :return:
    """
    # 获取目录路径
    screenshot_dir = get_project_path('trading_system_autotest') / 'img' / 'ele_screenshots'
    # 只创建目录（不包含文件名）
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    # 返回完整文件路径
    return str(screenshot_dir / ele_screenshot_name)

# ele_screenshot_path = get_project_path('trading_system_autotest') / 'img' / 'ele_screenshots' / ele_screenshot_name
# ele_screenshot_path.mkdir(parents=True, exist_ok=True)
# return str(ele_screenshot_path)
# ele_screenshot_path 是一个完整的文件路径（包含文件名）
# 但 mkdir() 方法会创建一个目录
# 当文件名没有扩展名或格式特殊时，可能创建了一个同名目录
# 后续 screenshot() 试图把文件写入一个已存在的目录时，就会报 IsADirectoryError

# if __name__ == '__main__':
#     # print(get_now_time())
#     # print(get_project_path())
#     # "/Users/fengzhaoxi/imooc/code/trading_system_autotest/common"
#     # sep(["config", "environment.yaml"], add_sep_before=True)
#     print(get_every_wallpaper())
#     print(get_img_path('商品图片1一'))
#     print(get_target_img_path('周杰伦头像截图.png'))
