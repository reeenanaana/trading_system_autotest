#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/6 16:38
# @Author: Rena

class TestAssert:
    def test_assert(self):
        # ==, !=, <, >, <=, >=
        assert "william" == "william"
        assert "william-a" != "william-b"
        assert 0 < 1
        assert 2 > 1
        assert 3 <= 7 - 2
        assert 4 >= 1 + 2
        # 包含和不包含
        assert "william" in "william UI自动化测试"
        assert "william" not in "UI自动化测试"
        # true 和 false
        assert 1    # 断言的是一个确定值或变量，就是True
        assert (9 < 10) is True
        assert not False
