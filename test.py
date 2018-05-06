import re
import logging
import datetime
logging.basicConfig(level=logging.INFO)
a = '''Pchip Errors Detected
    Complex 0 (parity error): Trap raised 300 times; Last Trap 05/06/2018 07:33:44
    Pchip Errors Detected
    Complex 0 (parity error): Trap raised 300 times; Last Trap 05/06/2018 07:33:44'''

def warn3(res):
    re_obj1 = re.compile(r'((Q|P)chip Errors Detected\n\s{4}Complex \d \(parity error\): Trap raised \d{1,6} times; Last Trap (\d{2})/(\d{2})/(\d{4}) (\d{2}):(\d{2}):(\d{2}))')
    result1 = re_obj1.findall(res)
    
    str1 = ''
    warn_type = 'P'
    datetime_15d_ago = datetime.datetime.now() - datetime.timedelta(days=15)
    for item in result1:
        datetime_befor = datetime.datetime(int(item[4]), int(item[2]), 
            int(item[3]), int(item[5]), int(item[6]), int(item[7]))

        if datetime_befor > datetime_15d_ago:
            str1 += item[0] + '\n'
        warn_type = item[1]

    if str1:
        return (str1, '注释：%schip 告警，建议拔插处理，如继续存在，建议更换板卡' % warn_type)
   
    return ('', '')

print(warn3(a))