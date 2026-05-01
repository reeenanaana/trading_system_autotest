#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/1 12:26
# @Author: Rena

import time

from selenium.common.exceptions import ElementNotVisibleException


class ObjectMap:

    def element_get(self, driver, locate_type, locator_expression, timeout=10, must_be_visible=False):
        """
        单个元素获取
        :param driver: 浏览器驱动
        :param locate_type: 定位方式类型
        :param locator_expression: 定位表达式
        :param timeout: 超时时间
        :param must_be_visible: 元素是否必须可见，True必须可见，False是默认值
        :return: 返回的元素
        """
        # 开始时间(13位的毫秒级时间戳)
        start_ms = time.time() * 1000
        # 设置的结束时间
        stop_ms = start_ms + timeout * 1000
        for x in range(int(timeout * 10)):
            # 查找元素
            try:
                element = driver.find_element(by=locate_type, value=locator_expression)
                # 如果元素不是必须可见的，就直接返回元素
                if not must_be_visible:
                    return element
                # 如果元素必须是可见的，则需要先判断元素是否可见
                else:
                    if element.is_displayed():  # find_element里自带的判断元素是否可见的方法
                        return element
                    else:
                        raise Exception()
            except Exception:
                now_ms = time.time() * 1000
                if now_ms >= stop_ms:
                    break
                pass
            time.sleep(0.1)
        raise ElementNotVisibleException(f"元素定位失败，定位方式：{locate_type}, 定位表达式：{locator_expression}")


# if __name__ == '__main__':
#     ObjectMap().element_get()
