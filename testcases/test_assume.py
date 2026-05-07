#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/7 12:26
# @Author: Rena

import pytest
from pytest_assume.plugin import assume


class TestAssert:
    def test_assert(self):
        with assume: assert "william" in "UI autotest"
        pytest.assume(1 + 1 == 3)
        assert 1 + 1 == 2
        print("over")
