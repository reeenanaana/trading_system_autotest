#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/9 15:32
# @Author: Rena

import aircv as ac
import cv2
from common.tools import get_screenshot_path, get_target_img_path, get_now_date_time_str, get_diff_img_path
from common.report_add_img import add_specific_img_to_report


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
        :param screenshot_path:截图路径
        :param target_img_path: 需要查找的图片的路径
        :return:
        """
        img_src = self.img_imread(screenshot_path)
        img_tar = self.img_imread(target_img_path)
        result = ac.find_template(img_src, img_tar)
        if not result:
            return 0
        # aircv 返回的 rectangle 四个点顺序为：左上、右上、右下、左下；cv2.rectangle 需要 左上+右下
        cv2.rectangle(img_src, result["rectangle"][0], result["rectangle"][2], (255, 0, 0), 2)
        diff_img_path = get_diff_img_path(f"{get_now_date_time_str()}-对比的图.png")
        # 把已经高亮了目标图片的截图，编码成 PNG 格式的 NumPy 字节数组，然后使用 NumPy 的 .tofile()方法，
        # 将该数组原样写入指定路径，生成最终的对比截图文件
        cv2.imencode(".png", img_src)[1].tofile(diff_img_path)
        add_specific_img_to_report(diff_img_path, "查找到的图")
        return result['confidence']


if __name__ == '__main__':
    screenshot_path = get_screenshot_path("ScreenShot_2026-05-10_172147_894.png")
    target_img_path = get_target_img_path("周杰伦头像截图.png")
    FindImg().get_confidence(screenshot_path, target_img_path)
