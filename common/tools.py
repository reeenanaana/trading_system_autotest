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

def get_project_path(project_name: str = "trading_system_autotest") -> Path:
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
    img_dir_path = get_project_path() + sep(["img", img_name], add_sep_before=True)
    return img_dir_path


def get_every_wallpaper():
    """
    从bing获取每日壁纸
    :return:
    """
    everyday_wallpaper_url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=10&mkt=zh-CN"
    try:
        res = requests.get(url=everyday_wallpaper_url)
        wallpaper_url = "https://cn.bing.com" + res.json()["images"][0]["url"][:-7]
    except Exception as e:
        print(e)
        wallpaper_url = ""
    return wallpaper_url


if __name__ == '__main__':
    # print(get_now_time())
    # print(get_project_path())
    # "/Users/fengzhaoxi/imooc/code/trading_system_autotest/common"
    # sep(["config", "environment.yaml"], add_sep_before=True)
    print(get_every_wallpaper())
