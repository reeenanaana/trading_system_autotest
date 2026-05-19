#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/15 15:53
# @Author: Rena

from time import sleep

import allure

from logs.log import log


class TestUserBalanceMysqlCheck:
    def test_user_balance_mysql_check(self, driver, test_objects):
        with allure.step("登录"):
            test_objects.login_page.login(driver, 'jay')
            sleep(2)

        with allure.step("获取当前登录用户的账户余额"):
            user_balance = test_objects.home_page.get_user_balance(driver)
            log.info(user_balance)

        with allure.step("从Mysql中读取账户余额"):
            sql = 'select balance from wallet where user_id = 12;'
            db_balance = test_objects.mysql_operate.query(sql)[0][0]
            log.info(db_balance)

        with allure.step("断言数据库中的数据是否与页面数据一致"):
            assert str(user_balance) == str(db_balance)
