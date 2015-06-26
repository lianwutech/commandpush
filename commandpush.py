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
    platform_token = config_info["platform"].get("auth_key", "")
    command_code_config = config_info.get("command_code", {})

    # 组件操作指令字典处理，component_type_id:operation_code
    comand_code_dict = {}
    for str_device_type in command_code_config:
        str_type_id = str_device_type.split("_")[-1]
        if str_type_id.isdigit():
            comand_code_dict[int(str_type_id)] = command_code_config[str_device_type]
        else:
            logger.error("error type: %s" % str_device_type)

    platform_url = config_info["platform"].get("url", "http://www.lianwuyun.cn/api/v1/")
    if project_id == 0:
        # 查询所有记录
        projects_url = platform_url + "projects"
        result = get_dict(projects_url, platform_token)
        if len(result) > 0:
            projects = json.loads(result)
        for project in projects:
            services_url = projects_url + "/%d/services" % project["project_id"]
            result = get_dict(services_url, platform_token)
            if len(result) > 0:
                services = json.loads(result)
                for service in services:
                    components_url = services_url + "/%d/components" % service["service_id"]
                    result = get_dict(components_url, platform_token)
                    if len(result) > 0:
                        components = json.loads(result)
                        for component in components:
                            component_dict[component["component_id"]] = component
                pass
    else:
        if service_id == 0:
            services_url = platform_url + "projects/%d/services" % project_id
            result = get_dict(services_url, platform_token)
            if len(result) > 0:
                services = json.loads(result)
                for service in services:
                    components_url = services_url + "/%d/components" % service["service_id"]
                    result = get_dict(components_url, platform_token)
                    if len(result) > 0:
                        components = json.loads(result)
                        for component in components:
                            component_dict[component["component_id"]] = component
        else:
            components_url = platform_url + "projects/%d/services/%d/components" % (project_id, service_id)
            result = get_dict(components_url, platform_token)
            if len(result) > 0:
                components = json.loads(result)
                for component in components:
                    component_dict[component["component_id"]] = component

    logger.debug("component_dict: %r" % component_dict)

    timestamp = read_timestamp(timestamp_file_name)

    while True:
        # 获取设备指令
        sql = """
            select cc_custusercode as component_id, cc_note as data, cc_createdata as timestamp
            from ebs_extend..mps_compcustomer
            where cc_createdate > %s
            """ % timestamp
        commands_records = sql_server.exec_query(sql)

        # 提交设备指令
        for command in commands_records:
            component_id = command[0]
            comand_data = command[1]
            component = component_dict[component_id]
            put_url = platform_url + "projects/%d/services/%d/components/%d/action" % \
                                     (component["project_id"], component["service_id"], component_id)
            data = {"component_id": component_id,
                    "operation_code": comand_code_dict[component["component_type_id"]],
                    "action_params": json.loads(comand_data)}
            result = put_data(put_url, platform_token, data)

        # 存储时间戳变量
        write_timestamp(timestamp_file_name, timestamp)
        time.sleep(0.5)

if __name__ == '__main__':
    run()
