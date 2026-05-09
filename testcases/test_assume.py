# #! /usr/bin/python3
# # coding = utf-8
# # @Time: 2026/5/7 12:26
# # @Author: Rena
#
# import pytest
# from pytest_assume.plugin import assume
#
#
# # 当使用 -n auto 并行运行测试时，pytest-xdist 需要将测试数据序列化后发送到不同进程，
# # 但 pytest-assume 插件生成的 ExceptionInfo 对象无法被序列化，
# # 导致进程间通信失败，最终测试崩溃。
#
# class TestAssert:
#     @pytest.mark.xdist_group(name="assume_tests")
#     # 为了不影响按照pytest.ini配置中的pytest.xdist的运行，
#     # 把这个test_assume注释了.(DS:https://chat.deepseek.com/share/1pbx5as7ayppkecpbh)
#     def test_assert(self):
#         with assume: assert "william" in "UI autotest"
#         pytest.assume(1 + 1 == 3)
#         assert 1 + 1 == 2
#         print("over")
