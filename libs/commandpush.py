#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import json
import logging
import sqlite3
from httplib2 import Http

from libs.utils import convert


# 初始化日志
logger = logging.getLogger('cmdpush')


# 获取配置项
def load_config(config_file_name):
    if os.path.exists(config_file_name):
        config_file = open(config_file_name, "r+")
        content = config_file.read()
        config_file.close()
        try:
            config_info = convert(json.loads(content.encode("utf-8")))
            logger.debug("load config info success，%s" % content)
            return config_info
        except Exception, e:
            logger.error("load config info fail，%r" % e)
            return None
    else:
        logger.error("config file is not exist. Please check!")
        return None


# 打开临时文件
def read_timestamp(file_name):
    try:
        file = open(file_name, "r")
        content = file.readline()
        if not content:
            return ""
        else:
            return content
    except Exception, e:
        logger.error("read file %s fail, exception:%r." % (file_name, e))


# 存储临时文件
def write_timestamp(file_name, content):
    try:
        file = open(file_name, "w+")
        file.write(content)
    except Exception, e:
        logger.error("read file %s fail, exception:%r." % (file_name, e))


# 获取数据
def get_dict(url, token):
    http_obj = Http(timeout=5)
    try:
        resp, content = http_obj.request(
            uri=url,
            method='GET',
            headers={'Content-Type': 'application/json; charset=UTF-8', "token": token})
    except Exception,e:
        logger.error("get_dict exception:%r" % e)
        return ""

    if resp.status == 200:
        return content

    return ""

# 推送数据
def put_data(url, token, data):
    http_obj = Http(timeout=5)
    try:
        resp, content = http_obj.request(
            uri=url,
            method='PUT',
            headers={'Content-Type': 'application/json; charset=UTF-8', "token": token},
            body=data)
    except Exception, e:
        logger.error("get_dict exception:%r" % e)
        return ""

    if resp.status == 200:
        return True

    return False

