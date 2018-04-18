import re
import logging
import datetime
logging.basicConfig(level=logging.INFO)
a = '''===============================================================================

MDA 1/1 detail

===============================================================================

Slot  Mda   Provisioned Type                            Admin     Operational

                Equipped Type (if different)            State     State

-------------------------------------------------------------------------------

1     1     imm12-10gb-xp-sf+                           up        up





MDA Specific Data

    Maximum port count            : 12

    Number of ports equipped      : 12

    Network ingress queue policy  : default

    Capabilities                  : Ethernet

    Fail On Error                 : Disabled

    Egress XPL error threshold    : 1000

    Egress XPL error window       : 60

    Ingress XPL error threshold   : 1000

    Ingress XPL error window      : 60

    Min channel size              : Sonet STS-192

    Max channel size              : Sonet STS-192

    Max number of channels        : 12

    Channels in use               : 0



Hardware Data

    Platform type                 : 7750

    Part number                   : 3HE04743AAAD01

    CLEI code                     : IPUCAZHFAA

    Serial number                 : NS123464673

    Manufacture date              : 09172012

    Manufacturing deviations      : (Not Specified)

    Manufacturing assembly number : 

    Administrative state          : up

    Operational state             : up

    Temperature                   : 60C

    Temperature threshold         : 75C

    Software boot (rom) version   : (Not Specified)

    Software version              : (Not Specified)

    Time of last boot             : 2016/04/07 23:59:50

    Current alarm state           : alarm cleared

    Base MAC address              : 0c:a4:02:be:48:83

    Firmware version              : I-12.0.R13



-------------------------------------------------------------------------------

QOS Settings

-------------------------------------------------------------------------------

Ing. Named Pool Policy            : None

Egr. Named Pool Policy            : None



-------------------------------------------------------------------------------

Egress  XPL Errors:   Trap raised 93 times;   Last Trap 01/26/2018 09:06:46

-------------------------------------------------------------------------------



===============================================================================

MDA 2/1 detail

===============================================================================

Slot  Mda   Provisioned Type                            Admin     Operational

                Equipped Type (if different)            State     State

-------------------------------------------------------------------------------

2     1     imm12-10gb-xp-sf+                           up        up





MDA Specific Data

    Maximum port count            : 12

    Number of ports equipped      : 12

    Network ingress queue policy  : default

    Capabilities                  : Ethernet

    Fail On Error                 : Disabled

    Egress XPL error threshold    : 1000

    Egress XPL error window       : 60

    Ingress XPL error threshold   : 1000

    Ingress XPL error window      : 60

    Min channel size              : Sonet STS-192

    Max channel size              : Sonet STS-192

    Max number of channels        : 12

    Channels in use               : 0



Hardware Data

    Platform type                 : 7750

    Part number                   : 3HE04743AAAF01

    CLEI code                     : IPUCAZHFAA

    Serial number                 : NS1320F0859

    Manufacture date              : 05162013

    Manufacturing deviations      : (Not Specified)

    Manufacturing assembly number : 

    Administrative state          : up

    Operational state             : up

    Temperature                   : 58C

    Temperature threshold         : 75C

    Software boot (rom) version   : (Not Specified)

    Software version              : (Not Specified)

    Time of last boot             : 2016/04/07 23:59:57

    Current alarm state           : alarm cleared

    Base MAC address              : 8c:90:d3:a0:da:61

    Firmware version              : I-12.0.R13



-------------------------------------------------------------------------------

QOS Settings

-------------------------------------------------------------------------------

Ing. Named Pool Policy            : None

Egr. Named Pool Policy            : None



===============================================================================

MDA 3/1 detail

===============================================================================

Slot  Mda   Provisioned Type                            Admin     Operational

                Equipped Type (if different)            State     State

-------------------------------------------------------------------------------

3     1     imm12-10gb-xp-sf+                           up        up





MDA Specific Data

    Maximum port count            : 12

    Number of ports equipped      : 12

    Network ingress queue policy  : default

    Capabilities                  : Ethernet

    Fail On Error                 : Disabled

    Egress XPL error threshold    : 1000

    Egress XPL error window       : 60

    Ingress XPL error threshold   : 1000

    Ingress XPL error window      : 60

    Min channel size              : Sonet STS-192

    Max channel size              : Sonet STS-192

    Max number of channels        : 12

    Channels in use               : 0



Hardware Data

    Platform type                 : 7750

    Part number                   : 3HE04743AAAF01

    CLEI code                     : IPUCAZHFAA

    Serial number                 : NS132566727

    Manufacture date              : 06232013

    Manufacturing deviations      : (Not Specified)

    Manufacturing assembly number : 

    Administrative state          : up

    Operational state             : up

    Temperature                   : 57C

    Temperature threshold         : 75C

    Software boot (rom) version   : (Not Specified)

    Software version              : (Not Specified)

    Time of last boot             : 2016/04/08 00:00:04

    Current alarm state           : alarm cleared

    Base MAC address              : 00:d0:f6:81:0a:50

    Firmware version              : I-12.0.R13



-------------------------------------------------------------------------------

QOS Settings

-------------------------------------------------------------------------------

Ing. Named Pool Policy            : None

Egr. Named Pool Policy            : None

===============================================================================



Wed Apr 18 11:39:56 GMT8 2018'''

def warn3(res):
    re_obj1 = re.compile(r'(XPL Errors:   Trap raised \d{1,6} times;   Last Trap (\d{2})/(\d{2})/(\d{4}) (\d{2}):(\d{2}):(\d{2}))')
    result1 = re_obj1.findall(res)

    str1 = ''
    datetime_15d_ago = datetime.datetime.now() - datetime.timedelta(days=15)
    for item in result1:
        datetime_befor = datetime.datetime(int(item[3]), int(item[1]), 
            int(item[2]), int(item[4]), int(item[5]), int(item[6]))

        if datetime_befor > datetime_15d_ago:
            str1 += item[0] + '\n'

    if str1:
        return (str1, '注释：XPL(Pchip Qchip) 告警，建议拔插处理，如继续存在，建议更换板卡')
   
    return ('', '')

print(warn3(a))