#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/13 14:23
# @Author: Rena

import logging
import time

from common.tools import get_project_path


def get_log(logger_name):
    # 创建一个logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    # logger.propagate = True
    # 没有默认的系统日志，没有log.info()，logger.propagate = True的情况Pytest也收集不到日志

    # 设置日志存放路径，日志文件名
    # 获取本地时间
    rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    # 设置日志存放路径
    all_log_path = get_project_path('trading_system_autotest') / 'logs' / 'all_logs'
    all_log_path.mkdir(parents=True, exist_ok=True)
    all_log_path = str(all_log_path)
    # 设置日志文件名
    all_log_name = all_log_path + rq + ".log"

    # 创建handler
    # 创建一个handler写入所有日志
    fh = logging.FileHandler(all_log_name)
    fh.setLevel(logging.INFO)

    # 定义日志输出格式
    all_log_formatter = logging.Formatter(
        '%(asctime)s - %(filename)s - %(module)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # 将定义好的输出格式，添加到handler
    fh.setFormatter(all_log_formatter)

    # 给logger添加handler
    logger.addHandler(fh)
    return logger


log = get_log("自动化测试")

if __name__ == '__main__':
    # get_log('自动化测试')
    log.debug("I am debug message.")
    log.info("I am info message.")
    log.warning("I am warning message.")
    log.error("I am error message.")
    log.critical("I am critical message.")
