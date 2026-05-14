#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/4/28 18:03
# @Author: Rena
class LoginBase:

    def login_input(self, input_placeholder: str) -> str:
        """
        登录用户名、密码输入框
        :param input_placeholder: placeholder 属性值，如 "用户名"、"密码"
        :return: XPath 定位表达式
        """
        return f"//input[@placeholder='{input_placeholder}']"

    def login_button(self, input_placeholder: str) -> str:
        """
        登录按钮
        :param input_placeholder:
        :return:
        """
        return f"//span[text()='{input_placeholder}']/parent::button"

    def login_success(self):
        """
        登录成功的标签提示
        :return:
        """
        return "//p[text()='登录成功']"

    def select_captcha(self):
        """
        是否需要验证码的单选框
        :return:
        """
        return "//span[contains(text(),'验证码')]/preceding-sibling::span/span"

    def captcha(self):
        """
        验证码
        :return:
        """
        return "//div[@class='el-image']"

    def input_captcha(self):
        """
        输入验证码的输入框
        :return:
        """
        return "//input[@placeholder='请输入验证码']"


if __name__ == '__main__':
    print(LoginBase().login_input("用户名"))  # 输出: //input[@placeholder='用户名']
    print(LoginBase().login_input("密码"))  # 输出: //input[@placeholder='密码']
    print(LoginBase().login_button('登录'))
