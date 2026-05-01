#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/1 12:26
# @Author: Rena

import time

from selenium.common.exceptions import ElementNotVisibleException, WebDriverException, NoSuchElementException


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
        stop_ms = start_ms + (timeout * 1000)
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

    def wait_for_ready_state_complete(self, driver, timeout=30):
        """
        等待页面完全加载完成
        :param driver: 浏览器驱动
        :param timeout: 超时时间
        :return:
        """
        # 开始时间
        start_ms = time.time() * 1000
        # 设置的结束时间
        stop_ms = start_ms + (timeout * 1000)
        for x in range(int(timeout * 10)):
            try:
                # 获取页面的状态
                ready_state = driver.execute_script("return document.readyState;")
            except WebDriverException:
                # 如果有driver的错误，执行js会失败，就直接跳过
                time.sleep(0.1)
                continue
            # 如果页面元素全部加载完成，返回True
            if ready_state == 'complete':
                time.sleep(0.1)
                return True
            else:
                now_ms = time.time() * 1000
                # 如果超时了就break
                if now_ms >= stop_ms:
                    break
                time.sleep(0.1)
        raise Exception(f"打开页面时，页面元素在{timeout}后仍然没有完全加载完。")

    def element_disappear(self, driver, locate_type, locator_expression, timeout=30):
        # 代码修改前后对比，见笔记Typora
        """
        等待页面元素消失
        :param driver:浏览器驱动
        :param locate_type:定位方式类型
        :param locator_expression:定位表达式
        :param timeout:超时时间
        :return:
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                element = driver.find_element(by=locate_type, value=locator_expression)
                # 元素存在且可见 → 继续等待
                if element.is_displayed():
                    time.sleep(0.1)
                    continue
                else:
                    # 元素存在但不可见 → 认为已消失
                    return True
            except NoSuchElementException:
                # 元素不存在 → 认为已消失
                return True
            except WebDriverException:
                # driver 异常 → 继续等待
                time.sleep(0.1)

        raise Exception(f"元素没有消失，定位方式：{locate_type}，定位表达式：{locator_expression}")

    def element_appear(self, driver, locate_type, locator_expression, timeout=30):
        # DS老师分析原本的代码并修改成如下：https://chat.deepseek.com/share/1hosash4yg8ml2n3uj
        """
        等待页面元素出现并可见
        :return: WebElement 对象
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                element = driver.find_element(by=locate_type, value=locator_expression)
                if element.is_displayed():
                    return element
                # 元素存在但不可见，继续等待
                time.sleep(0.1)
            except NoSuchElementException:
                # 元素未找到，继续等待
                time.sleep(0.1)
            except WebDriverException:
                # driver 异常，继续等待
                time.sleep(0.1)

        raise ElementNotVisibleException(
            f"元素没有出现，定位方式：{locate_type}，定位表达式：{locator_expression}"
        )
