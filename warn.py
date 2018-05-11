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
    re_str = r'''(Fan tray number                   : (\d)
    Speed                           : (\w{3,4} speed( \(0-\d\d%\))?)
    Status                          : (\w{2,5}))'''
    re_obj = re.compile(re_str)
    result = re_obj.findall(res)

    msg = ''
    atn = ''
    if result:
        logging.debug('mobile_warn1 匹配结果：%s' % result)
        for item in result:
            if item[2] == 'full speed':
                msg += 'Fan tray number: %s\nSpeed: full speed\n' % item[1]
                atn += '风扇%s全转速，建议清洗滤尘网。' % item[1]
            elif int(item[3][-4:-2]) >= 50:
                msg += 'Fan tray number: %s\nSpeed: %s\n' % (item[1], item[2])
                atn += '风扇%s转速大于50。' % item[1]
            elif item[3] != 'up':
                msg += 'Fan tray number: %s\nStatus: %s\n' % item[4]
                atn += '风扇%s状态不正常。' % item[1]
        return(msg, atn)
    else:
        return ('','')

def mobile_warn2(res):
    re_str = r'''(Power supply number               : \d
    Defaulted power supply type     : .{2,10}
    Power supply model              : .{2,10}
    Status                          : (.{2,10}))'''

    re_obj = re.compile(re_str)
    result = re_obj.findall(res)

    msg = ''

    if result:
        logging.debug('mobile_warn2 匹配结果：%s' % result)
        for item in result:
            if item[1] != 'up':
                msg += item[0] + '\n'
        
        return(msg, '电源异常。')
    else:
        return ('','')

def mobile_warn3(res):
    re_str = r'''(Critical LED state                : (.{2,10})
  Major LED state                   : (.{2,10})
  Minor LED state                   : (.{2,10}))'''

    re_obj = re.compile(re_str)     
    result = re_obj.findall(res)

    msg = ''

    if result:
        logging.debug('mobile_warn3 匹配结果：%s' % result)
        for item in result:
            if item[1] != 'Off' or item[2] != 'Off' or item[3] != 'Off':
                msg += item[0] + '\n'
        
        return(msg, '主控指示灯告警')
    else:
        return ('','')

def mobile_warn4(res):
    re_str = r'''Total                                 [,0-9]{1,11}         \d{1,3}\.\d\d%                
   Idle                               [,0-9]{1,11}          (\d{1,3})\.\d\d%                
   Usage                                [,0-9]{1,11}           \d{1,3}\.\d\d%'''
    re_obj = re.compile(re_str)
    result = re_obj.search(res)
    msg = ''
    if result:
        logging.debug('mobile_warn4 匹配结果：%s' % result.group())
        if int(result.group(1)) < 50:
            msg += result.group() + '\n'

        return (msg, 'cpu利用率高。')
    else:
        return ('','')

def mobile_warn5(res):
    re_str = '''Current Total Size :    (.{10,15}) bytes
Total In Use       :    (.{10,15}) bytes
Available Memory   :   (.{10,15}) bytes'''
    re_obj = re.compile(re_str)
    result = re_obj.search(res)
    msg = ''
    if result:
        logging.debug('mobile_warn5 匹配结果：%s' % result.group())
        current_sotal_size = int(result.group(1).replace(',', ''))
        total_in_use = int(result.group(2).replace(',', ''))
        available_memory = int(result.group(3).replace(',', ''))
        logging.debug('current_sotal_size=%s, total_in_use=%s, available_memory=%s' % (current_sotal_size, total_in_use, available_memory))
        if available_memory < 2*(current_sotal_size + total_in_use):
            msg += result.group() + '\n'

        return (msg, '内存利用率高。')
    else:
        return ('','')


def mobile_warn6(res):
    re_str = r'''((Dynamic|Ingress|Egress) Queues (\+|\|)\s{1,11}\d{2,10}\|\s{1,11}(\d{2,10})\|\s{1,11}(\d{2,10}))'''
    re_obj = re.compile(re_str)     
    result = re_obj.findall(res)
    msg = ''
    if result:
        logging.debug('mobile_warn6 匹配结果：%s' % result)
        for item in result:
            if int(item[4]) < int(item[3]):
                msg += item[0] + '\n'
        
        return (msg, '空闲队列资源不足。')
    else:
        return ('','')



def mobile_warn7(res):
    re_str = '''FCS Errors'''

    re_obj = re.compile(re_str)     
    result = re_obj.findall(res)
    
    if result:
        logging.debug('mobile_warn7 匹配结果：%s' % result)
        return('FCS Errors', 'FCS Errors告警。')
    else:
        return ('','')


def mobile_warn8(res):
    re_str = r'''(Temperature                   : (\d\d)C)'''

    re_obj = re.compile(re_str)     
    result = re_obj.findall(res)
    msg = ''
    if result:
        logging.debug('mobile_warn8 匹配结果：%s' % result)
        for item in result:
            if int(item[1]) > 62:
                msg += item[0] + '\n'
        
        return (msg, '板卡温度高，建议清洗防尘网，若清洗之后还没变化或建议降低机房环境温度。')
    else:
        return ('','')



def mobile_warn9(res):
    re_str = r'''Flash - cf3:
    Administrative State          : [a-zA-Z]{2,4}
    (Operational state             : ([a-zA-Z]{2,4}))'''

    re_obj = re.compile(re_str)     
    result = re_obj.findall(res)
    msg = ''
    atn = '注：'
    if result:
        logging.debug('mobile_warn9 匹配结果：%s' % result)
        
        for index, item in enumerate(result):
            if item[1] != 'up':
                card_id = 'A'
                if index == 1:
                    card_id = 'B'
                msg += item[0] + '\n'
                atn += '%s槽位CF卡退服。' % card_id
        return (msg, atn)
    else:
        return ('','')


def mobile_warn10(res):
    re_str = '''FCS Errors'''

    re_obj = re.compile(re_str)     
    result = re_obj.findall(res)
    
    if result:
        return('FCS Errors', 'FCS Errors告警。')
    else:
        return ('','')


def mobile_warn11(res):
    re_str = r'''(Totals for pool\s{1,9}\d{2,5}\s{1,8}(\d{1,3})%)'''

    re_obj = re.compile(re_str)     
    result = re_obj.findall(res)
    msg = ''
    if result:
        logging.debug('mobile_warn11 匹配结果：%s' % result)
        for item in result:
            if int(item[1]) <= 20:
                msg += item[0] + '\n'
        
        return (msg, '地址池空闲值低于20%。')
    else:
        return ('','')

def mobile_warn12(res):
    re_str = r'''Block usage \(\%\)                       : (\d{1,3})'''
    re_obj = re.compile(re_str)
    result = re_obj.search(res)
    msg = ''
    if result:
        logging.debug('mobile_warn12 匹配结果：%s' % result.group())
        if int(result.group(1)) >= 90:
            msg += result.group() + '\n'

        return (msg, 'NAT公网地址池空闲值低于10%。')
    else:
        return ('','')