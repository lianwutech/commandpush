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


import setting
from libs.commandpush import *
from libs.msodbc import ODBC_MS

# 全局变量
# 配置文件
config_file_name = "datasync.cfg"
# 临时文件
timestamp_file_name = "timestamp.txt"

# 初始化日志
logger = logging.getLogger('datasync')

# 配置信息
config_info = load_config(config_file_name)

# 停止标记
run_flag = False

def stop():
    run_flag = False

# 数据库对象
sql_server = ODBC_MS(server=config_info["sqlserver"]["host"],
                     database=config_info["sqlserver"]["database"],
                     uid=config_info["sqlserver"]["uid"],
                     pwd=config_info["sqlserver"]["pwd"])

def run():
    # 测试sql server
    if not sql_server.test_db():
        logger.error("database test fail.")
        sys.exit()

    # 获取平台的设备信息
    component_dict = {}
    project_id = config_info["platform"].get("project_id", 0)
    service_id = config_info["platform"].get("service_id", 0)
    if project_id == 0:
        # 查询所有记录

        pass
    else:
        if service_id == 0:
            pass
        else:
            pass

    timestamp = read_timestamp(timestamp_file_name)

    while True:
        # 获取设备指令
        sql = """
            select cc_custusercode as component_id, cc_note as data, cc_createdata as timestamp
            from ebs_extend..mps_compcustomer
            where cc_createdate > %s
            """ % timestamp
        records = sql_server.exec_query(sql)

        # 提交设备指令

        # 存储时间戳变量
        write_timestamp(timestamp_file_name, timestamp)
        pass

        time.sleep(0.5)




