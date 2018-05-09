# encoding: utf-8
import datetime
import re
import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

def warn_find_all(res, re_str):
    re_obj = re.compile(re_str)
    result = re_obj.findall(res)
    return result

def mobile_warn1(res):
    re_obj = re.compile(r'(Fan tray number\s{19}: (\d)\s{5}Speed\s{27}: (.{2,10})\s{5}Status\s{26}: (\w{2,5}))')
    result = re_obj.findall(res)

    str1 = ''

    if result:
        logging.debug('mobile_warn1 匹配结果：%s' % result)
        for item in result:
            if item[2] == 'full speed':
                str1 += item[0] + '\n'
            elif int(item[2][:-1]) > 50:
                str1 += item[0] + '\n'
            elif item[3] != 'up':
                str1 += item[0] + '\n'
        
        return(str1, '注：风扇全转速，建议清洗滤尘网。')
    else:
        return None

def mobile_warn2(res):
    re_str = '''(Power supply number               : 1
    Defaulted power supply type     : .{2,10}
    Power supply model              : .{2,10}
    Status                          : (.{2,10}))'''

    result = warn_find_all(res, re_str)

    str1 = ''

    if result:
        logging.debug('mobile_warn2 匹配结果：%s' % result)
        for item in result:
            if item[1] != 'up':
                str1 += item[0] + '\n'
        
        return(str1, '注：电源异常。')
    else:
        return None

def mobile_warn3(res):
    re_str = '''(Critical LED state                : (.{2,10})
  Major LED state                   : (.{2,10})
  Minor LED state                   : (.{2,10}))'''

    result = warn_find_all(res, re_str)

    str1 = ''

    if result:
        logging.debug('mobile_warn3 匹配结果：%s' % result)
        for item in result:
            if item[1] != 'off' or item[2] != 'off' or item[3] != 'off':
                str1 += item[0] + '\n'
        
        return(str1, '注：主控板告警。')
    else:
        return None

def mobile_warn4(res):
    re_obj = re.compile(r'Idle  (.{2,4})')
    result = re_obj.search(res)
    str1 = ''
    if result:
        if int(result.group(1)[:-1]) < 50:
            str1 += result.group() + '\n'

        return (str1, 'cpu闲置值告警。')
    else:
        return None

def mobile_warn5(res):
    re_str = '''Current Total Size :    (.{10,15}) bytes
Total In Use       :    (.{10,15}) bytes
Available Memory   :   (.{10,15}) bytes'''
    re_obj = re.compile(re_str)
    result = re_obj.search(res)
    str1 = ''
    if result:
        logging.debug('mobile_warn5 匹配结果：%s' % result.group())
        current_sotal_size = int(result.group(1).replace(',', ''))
        total_in_use = int(result.group(2).replace(',', ''))
        available_memory = int(result.group(3).replace(',', ''))
        logging.debug('current_sotal_size=%s, total_in_use=%s, available_memory=%s' % (current_sotal_size, total_in_use, available_memory))
        if available_memory < 2*(current_sotal_size + total_in_use):
            str1 += result.group() + '\n'

        return (str1, '内存告警。')
    else:
        return None


def mobile_warn6(res):
    re_str = '''Dynamic Queues \+      \d{2,10}\|       (\d{2,10})\|      (\d{2,10})'''
    re_obj = re.compile(re_str)
    result = re_obj.search(res)
    str1 = ''
    if result:
        logging.debug('mobile_warn6 匹配结果：%s' % result.group())
        if int(result.group(2)) < int(result.group(1)):
            str1 += result.group() + '\n'

        return (str1, '队列资源告警。')
    else:
        return None



def mobile_warn7(res):
    re_str = '''FCS Errors'''

    result = warn_find_all(res, re_str)
    
    if result:
        return('FCS Errors', '注：FCS Errors告警。')
    else:
        return None




