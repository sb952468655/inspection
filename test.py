import re
import logging
import datetime
logging.basicConfig(level=logging.INFO)
a = '''1535045 2017/09/05 13:29:58.79 GMT8 MINOR: PORT #2030 Base Port 1/1/5
    XPL Errors:   Trap raised 9780 times;   Last Trap 12/13/2017 08:54:50
    1535342 2017/04/23 13:29:58.34 GMT8 MINOR: PORT #2030 Base Port 1/2/5
    XPL Errors:   Trap raised 9780 times;   Last Trap 04/01/2018 08:54:50
    XFP/SFP DDM (rxOpticalPower-low-alarm)
    XPL Errors:   Trap raised 9780 times;   Last Trap 12/13/2017 08:54:50
    1567045 2018/04/06 13:29:18.22 GMT8 MINOR: PORT #2030 Base Port 1/1/6
    XPL Errors:   Trap raised 9780 times;   Last Trap 12/13/2017 08:54:50
    asdasdasdasdas
    asdasdasdaaaaaertgertrtrtyytuu
    rewterterter ertertyutu yerterterterter
    erterttertertertert
    XPL Errors:   Trap raised 9780 times;   Last Trap 12/13/2017 08:54:50
    XPL Errors:   Trap raised 9780 times;   Last Trap 12/13/2017 08:54:50
    asdasdasddweqweqweqweqw'''

def warn4(res):
    re_obj1 = re.compile(r'rxOpticalPower-(low|high)-alarm')
    result1 = re_obj1.search(res)
    re_obj2 = re.compile(r'\d{7} \d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}.\d{2} GMT8 MINOR: PORT #\d{4} Base Port \d/\d/\d')
    result2 = re_obj2.findall(res)

    str1 = '高' if result1.group(0) == 'high' else '低'
    str2 = ''
    for i in result2:
        str2 += i + '\n'

    return(str2, '注释：端口%s收光告警,建议检查光路' % str1)

print(warn4(a))