import re
import logging
import datetime
logging.basicConfig(level=logging.INFO)
a = '''XFP/SFP DDM (rxOpticalPower-high-alarm)
    XPL Errors:   Trap raised 9780 times;   Last Trap 12/13/2017 08:54:50
    XPL Errors:   Trap raised 9780 times;   Last Trap 12/13/2017 08:54:50
    XPL Errors:   Trap raised 9780 times;   Last Trap 04/01/2018 08:54:50
    XFP/SFP DDM (rxOpticalPower-low-alarm)
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

def warn4(res):
    re_obj1 = re.compile(r'rxOpticalPower-(low|high)-alarm')
    result1 = re_obj1.search(res)
    logging.info('匹配结果：' + str(result1.group(1)))
    str1 = '高' if result1.group(1) == 'high' else '低'

    return('', '注释：端口%s收光告警,建议检查光路' % str1)


print(warn4(a))