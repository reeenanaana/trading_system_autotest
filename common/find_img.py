#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/9 15:32
# @Author: Rena

import aircv as ac

from common.tools import get_screenshot_path, get_target_img_path


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

#
# if __name__ == '__main__':
#     source_path = get_target_img_path("周杰伦头像截图.png")
#     search_path = get_screenshot_path("ScreenShot_2026-05-10_172147_894.png")
#     FindImg().get_confidence(source_path, search_path)
