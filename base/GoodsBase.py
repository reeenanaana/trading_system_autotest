#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/4 10:27
# @Author: Rena

class GoodsBase:
    def get_goods_title_locator(self):
        """
        取定位表达式之商品标题（多行文本输入）
        :return:
        """
        return "//form[@class='el-form']//textarea[@placeholder='请输入商品标题']"

    def get_goods_details_locator(self):
        """
        取定位表达式之商品详情（多行文本输入）
        :return:
        """
        return "//form[@class='el-form']//textarea[@placeholder='请输入商品详情']"

    def get_goods_quantity_locator(self, symbol):
        """
        取定位表达式之商品数量输入(加减符号或输入框)
        :param symbol: plus / minus
        :return:
        """
        if symbol:
            return f"//label[@for='product_stock']/following-sibling::div//i[@class='el-icon-{symbol}']/parent::span"
        else:
            return "//label[@for='product_stock']/following-sibling::div//input[@placeholder='商品数量']"

    def get_goods_img_locator(self):
        """
        取定位表达式之商品图片输入框
        :return:
        """
        return "//form[@class='el-form']//input[@type='file' and @name='file']"

    def get_goods_price_locator(self):
        """
        取定位表达式之商品单价输入框
        :return:
        """
        return "//form[@class='el-form']/descendant::input[contains(@placeholder, '商品单价')]"

    def get_goods_status_locator(self):
        """
        取定位表达式之商品状态输入框
        :return:
        """
        return "//form[@class='el-form']//input[@placeholder='请选择商品状态']"

    def get_goods_status_option_locator(self, option_name):
        """
        取定位表达式之商品状态选项
        :param option_name: 上架 / 下架
        :return:
        """
        return f"//span[text()='{option_name}']/parent::li"

    def get_add_goods_bottom_button_locator(self, button_name):
        """
        取定位表达式之新增二手商品底部按钮
        :param button_name: 提交 / 重置
        :return: 因为点击的是span的父元素，所以要parent出那个button元素
        """
        return f"//span[text()='{button_name}']/parent::button"
