import re
import logging
import datetime
logging.basicConfig(level=logging.INFO)
a = '''XPL Errors:   Trap raised 9780 times;   Last Trap 12/13/2017 08:54:50
    XPL Errors:   Trap raised 9780 times;   Last Trap 12/13/2017 08:54:50
    XPL Errors:   Trap raised 9780 times;   Last Trap 12/13/2017 08:54:50
    XPL Errors:   Trap raised 9780 times;   Last Trap 04/01/2018 08:54:50
    XPL Errors:   Trap raised 9780 times;   Last Trap 12/13/2017 08:54:50
    XPL Errors:   Trap raised 9780 times;   Last Trap 12/13/2017 08:54:50
    XPL Errors:   Trap raised 9780 times;   Last Trap 04/02/2018 08:54:50
    XPL Errors:   Trap raised 9780 times;   Last Trap 12/13/2017 08:54:50
    asdasdasdasdas
    asdasdasdaaaaaertgertrtrtyytuu
    rewterterter ertertyutu yerterterterter
    erterttertertertert
    XPL Errors:   Trap raised 9780 times;   Last Trap 12/13/2017 08:54:50
    XPL Errors:   Trap raised 9780 times;   Last Trap 12/13/2017 08:54:50
    asdasdasddweqweqweqweqw'''

def warn3(res):
    re_obj1 = re.compile(r'(XPL Errors:   Trap raised \d{1,5} times;   Last Trap (\d{2})/(\d{2})/(\d{4}) (\d{2}):(\d{2}):(\d{2}))')
    result1 = re_obj1.findall(res)
    str1 = ''
    datetime_15d_ago = datetime.datetime.now() - datetime.timedelta(days=15)
    for item in result1:
        datetime_befor = datetime.datetime(int(item[3]), int(item[1]), 
            int(item[2]), int(item[4]), int(item[5]), int(item[6]))

        if datetime_befor > datetime_15d_ago:
            str1 += item[0] + '\n'

    if result1:
        return (str1, '注释：XPL(Pchip Qchip) 告警，建议拔插处理，如继续存在，建议更换板卡')
   
    return ('', '')


print(warn3(a))