# encoding: utf-8
import os
import json
import logging
import time
from warn import *
from report import make_report_mob
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

#告警检查列表
warn_check = (mobile_warn1, mobile_warn2, mobile_warn3, mobile_warn4, mobile_warn5, mobile_warn6, mobile_warn7, 
                mobile_warn8, mobile_warn9, mobile_warn10, mobile_warn11, mobile_warn12)
warn_res = []

date_path = time.strftime('%Y-%m-%d', time.localtime(time.time()))

city_list = os.listdir(date_path)

for city in city_list:
    city_path = os.path.join(date_path,city)
    if  not os.path.isfile(city_path):
        log_list = os.listdir(city_path)
    
        for log in log_list:
            if not log.endswith('7750'):
                break
            log_path = os.path.join(city_path,log)
            
            logging.debug('发现日志：%s, 字节数：%s' % (log, os.path.getsize(log_path)))
            f = open(log_path)
            f_result = f.read()
            for func in warn_check:
                info, warn = func(f_result)
                if info and warn:
                    warn_item = [log, info, warn]
                    warn_res.append(warn_item)
            f.close()

        make_report_mob(warn_res)


