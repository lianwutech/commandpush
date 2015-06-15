#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
业务平台与lianwuyun间的命令同步

实时扫描sqlserver指定表，然后将数据发送给lianwuyun

"""

from __future__ import print_function


import os
import sys
import time
import json
import threading
import logging
import pyodbc

from libs.commandpush import load_config
from libs.msodbc import ODBC_MS

# 全局变量
config_file_name = "datasync.cfg"

# 初始化日志
logger = logging.getLogger('datasync')

# 配置信息
config_info = load_config(config_file_name)

# 数据库对象
sql_server = ODBC_MS(server=config_info["sqlserver"]["host"],
                     database=config_info["sqlserver"]["database"],
                     uid=config_info["sqlserver"]["uid"],
                     pwd=config_info["sqlserver"]["pwd"])

def main():
    # 测试sql server
    if not sql_server.test_db():
        logger.error("database test fail.")
        sys.exit()

    while True:
        pass

        time.sleep(0.5)

def entry_point():
    """Zero-argument entry point for use with setuptools/distribute."""
    raise SystemExit(main(sys.argv))

if __name__ == '__main__':
    main()




