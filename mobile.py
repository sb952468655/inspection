# encoding: utf-8
import os
import json
import logging
from warn import *

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

#告警检查列表
warn_check = (mobile_warn1, mobile_warn2, mobile_warn3, mobile_warn4, mobile_warn5, mobile_warn6, mobile_warn7)
warn_res = []

f_path = 'log'
if not os.path.exists(f_path):
        logging.debug('文件夹: %s 不存在' % f_path)

log_list = os.listdir(f_path)

for log in log_list:
    log_path = os.path.join(f_path,log)
    if log.endswith('.log'):
        logging.debug('发现日志：%s, 字节数：%s' % (log, os.path.getsize(log_path)))
        f = open(log_path)
        f_result = f.read()
        for func in warn_check:
            info, warn = func(f_result)
            if info and warn:
                warn_item = [log[:-4], info, warn]
                logging.debug('告警信息：%s' % warn_item)
                warn_res.append(warn_item)
        f.close()



