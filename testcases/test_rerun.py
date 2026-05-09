#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/7 11:46
# @Author: Rena

import random

import pytest


class TestRerun:
    # @pytest.mark.flaky(reruns=5, reruns_delay=1)
    # 上面的rerun和pytest.ini文件中的pytest.xdist会有冲突，所以注释掉了
    def test_rerun(self):
        num = random.randint(1, 3)
        print(num)
        if num != 1:
            print("失败")
            raise Exception("出错了")
        else:
            print("成功")

# class TestRerun:
#     # 在命令行添加reruns / reruns-delay参数可以对全局用例做设置
#     # pytest -s testcases/test_rerun.py --reruns 5 --reruns-delay 1
#     def test_rerun(self):
#         num = random.randint(1, 3)
#         print(num)
#         if num != 1:
#             print("失败")
#             raise Exception("出错了")
#         else:
#             print("成功")
