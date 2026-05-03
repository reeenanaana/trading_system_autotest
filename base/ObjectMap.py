#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/1 12:26
# @Author: Rena

import time

from selenium.common.exceptions import ElementNotVisibleException, WebDriverException, NoSuchElementException, \
    StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

from common.yaml_config import GetConf


class ObjectMap:
    # 获取基准地址
    url = GetConf().get_url()

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
        if locate_type is None:
            return True
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
        if locate_type is None:
            return True
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
            f"元素没有 出现，定位方式：{locate_type}，定位表达式：{locator_expression}"
        )

    def element_to_url(
            self,
            driver,
            url,
            locate_type_disappear=None,
            locator_expression_disappear=None,
            locate_type_appear=None,
            locator_expression_appear=None,
            timeout=30):
        """
        跳转地址
        :param driver: 浏览器驱动
        :param url: 跳转的地址
        :param locate_type_disappear: 等待页面元素消失的定位方式
        :param locator_expression_disappear: 等待页面元素消失的定位表达式
        :param locate_type_appear: 等待页面元素出现的定位方式
        :param locator_expression_appear: 等待页面元素出现的定位表达式
        :param timeout:
        :return:
        """
        try:
            driver.get(self.url + url)  # "https://www.example.com/login"
            # 等待页面元素都加载完成
            self.wait_for_ready_state_complete(driver)
            # 跳转地址后等待元素消失
            self.element_disappear(
                driver,
                locate_type_disappear,
                locator_expression_disappear
            )
            # 跳转地址后等待元素出现
            self.element_appear(
                driver,
                locate_type_appear,
                locator_expression_appear
            )
        except Exception as e:
            print(f"跳转地址出现异常，异常原因：{e}")
            return False
        return True

    def element_is_display(self, driver, locate_type, locator_expression):
        """
        元素是否显示（可用于断言是否找到了元素，区别于之前element_appear的方法，该方法如果未找到元素抛出错误）
        :param driver:
        :param locate_type:
        :param locator_expression:
        :return:
        """
        try:
            driver.find_element(by=locate_type, value=locator_expression).is_displayed()
            return True
        except NoSuchElementException:
            # 发生了NoSuchElementException异常，说明页面中未找到该元素，返回false
            return False

    def element_fill_value(self, driver, locate_type, locator_expression, fill_value, timeout=30):
        """
        元素填值
        :param driver: 浏览器驱动
        :param locate_type: 定位方式
        :param locator_expression: 定位表达式
        :param fill_value: 填入的值
        :param timeout: 超时时间
        :return: bool
        """
        fill_value = str(fill_value)  # 统一转为字符串

        def get_element():
            """获取元素，支持重试"""
            return self.element_appear(
                driver,
                locate_type=locate_type,
                locator_expression=locator_expression,
                timeout=timeout
            )

        def clear_element(element):
            """清除元素内容，处理StaleElementReferenceException"""
            try:
                element.clear()
                return True
            except StaleElementReferenceException:
                self.wait_for_ready_state_complete(driver)
                time.sleep(0.1)
                new_element = get_element()
                try:
                    new_element.clear()
                    return True
                except Exception:
                    return False
            except Exception:
                return False

        def send_value(element, value):
            """发送值，支持回车提交"""
            self.wait_for_ready_state_complete(driver)
            if value.endswith("\n"):
                element.send_keys(value[:-1])
                element.send_keys(Keys.RETURN)
            else:
                element.send_keys(value)
            self.wait_for_ready_state_complete(driver)

        # 获取元素
        element = get_element()

        # 清除原有值
        clear_element(element)

        # 重新获取元素（避免清除后元素失效）
        try:
            element = get_element()
            send_value(element, fill_value)
        except StaleElementReferenceException:
            self.wait_for_ready_state_complete(driver)
            time.sleep(0.1)
            element = get_element()
            clear_element(element)
            send_value(element, fill_value)
        except Exception as e:
            raise Exception(f"元素填值失败: {locator_expression}, 错误: {e}")

        return True

    def element_click(
            self,
            driver,
            locate_type,
            locator_expression,
            locate_type_disappear=None,
            locator_expression_disappear=None,
            locate_type_appear=None,
            locator_expression_appear=None,
            timeout=30
    ):
        """
        点击元素，并在点击后等待指定元素出现/消失

        :param driver:浏览器驱动
        :param locate_type:定位方式类型
        :param locator_expression:定位表达式
        :param locate_type_disappear:等待元素消失的定位方式类型
        :param locator_expression_disappear:等待元素消失的定位表达式
        :param locate_type_appear:等待元素出现的定位方式类型
        :param locator_expression_appear:等待元素出现的定位表达式
        :param timeout:超时时间（秒）
        :return: bool，点击成功返回True，失败返回False
        """
        # 参数校验：必填参数不能为空
        if not all([locate_type, locator_expression]):
            raise ValueError("locate_type 和 locator_expression 为必填参数")

        # 重试次数，处理元素过时异常
        max_retries = 2
        for attempt in range(max_retries):
            try:
                # 等待元素可见
                element = self.element_appear(
                    driver=driver,
                    locate_type=locate_type,
                    locator_expression=locator_expression,
                    timeout=timeout
                )
                # 点击元素
                element.click()
                break  # 点击成功，跳出重试循环
            except StaleElementReferenceException:
                if attempt == max_retries - 1:
                    print(f"元素在 {max_retries} 次重试后仍然过时，点击失败")
                    return False
                # 等待页面稳定后重试
                self.wait_for_ready_state_complete(driver=driver)
                time.sleep(0.1)
                continue
            except Exception as e:
                print(f"页面出现异常，元素不可点击：{e}")
                return False

        # 点击后的元素出现/消失校验（仅当参数提供时执行）
        try:
            if locate_type_appear and locator_expression_appear:
                self.element_appear(
                    driver,
                    locate_type_appear,
                    locator_expression_appear,
                    timeout=timeout
                )

            if locate_type_disappear and locator_expression_disappear:
                self.element_disappear(
                    driver,
                    locate_type_disappear,
                    locator_expression_disappear,
                    timeout=timeout
                )
        except Exception as e:
            print(f"等待元素消失或出现失败：{e}")
            return False

        return True