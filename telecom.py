# $language = "python"
# $interface = "1.0"

import time
import datetime
import os
import sys
import json
import re
# 跳板配置
g_tb_config = [
    ('202.102.19.253', '9527', 'alang', 'May4th@)!%'), # 电信
    ('202.102.19.254', '9527', 'xunjian', 'noc@1304'), # 电信教育网
    ('202.102.19.253', '9527', 'alang', 'May4th@)!%',  # CE
        ('telnet 59.43.5.135',
        'jiangsu', 'NOC@1501',
        'telnet 115.168.128.180 /source-interface loopback0',
        'jituan', 'jstelecom1234!@'))
]


def warn1(res):

    b = res.split('-------------------------------------------------------------------------------')

    re_obj = re.compile(r'Fan tray number                   : (\d)')
    result = re_obj.findall(b[1])
    re_obj2 = re.compile(r'Speed                           : (.*)\n')
    result2 = re_obj2.findall(b[1])

    if not result or not result2:
        return ('', '')

    fan_list = []
    for i in range(len(result2)):
        if result2[i].strip('\r\n') == 'full speed':
            fan_list.append(result[i])

    str1 = '1.Environment Information\nFan tray number ：' + ','.join(fan_list).encode('utf-8') + ' full speed'
    str2 = '%s个风扇满运行，建议降低机房温度或更换增强型风扇' % str(len(result))

    return (str1, str2)


def warn2(res):
    #先判断是否为mda卡
    mda_obj = re.compile(r'MDA (.*) detail')
    result_mda = mda_obj.findall(res)

    result1 = None
    result2 = None
    if result_mda:
        re_obj1 = re.compile(r'(\d?\d)?\s{4,5}(\d)\s{5}(.*)\s+up        up')
    else:
        re_obj1 = re.compile(r'(\w?\w)?\s{5,6}(.*)\s+up    up')

    result1 = re_obj1.findall(res)
    re_obj2 = re.compile(r'Temperature                   : (\d\d)C')
    result2 = re_obj2.findall(res)

    if not result1 or not result2:
        return ('', '')

    dict1 = dict(zip(result2, result1))
    str1 = ''

    for key,val in dict1.items():
        if int(key) >= 60:
            if result_mda:
                if ('imm12' in val[2] or 'imm48' in val[2]) and int(key) < 65:
                    continue
                str1 += 'mda %s/%s     %s\nTemperature        : %sC\n' % (val[0], val[1], val[2].strip(), key)
            else:
                if ('imm12' in val[1] or 'imm48' in val[1]) and int(key) < 65:
                    continue
                str1 += 'Card %s     %s\nTemperature        : %sC\n' % (val[0], val[1].strip(), key)

    str2 = '板卡温度过高，建议清洗滤网。'
    if result_mda:
        str2 = 'mda' + str2 
    
    return (str1, str2)

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
        return (str1, '注释：XPL 告警，建议拔插处理，如继续存在，建议更换板卡')
   
    return ('', '')

def warn4(res):
    re_obj1 = re.compile(r'rxOpticalPower-(low|high)-alarm')
    result1 = re_obj1.search(res)
    re_obj2 = re.compile(r'(\d{6} (\d{4})/(\d{2})/(\d{2}) (\d{2}):(\d{2}):(\d{2})\.\d{2} GMT8 MINOR: PORT #\d{4} Base Port \d/\d/\d\s+"SFF DDM \(rxOpticalPower-(low|high)-alarm\) \w+")')
    result2 = re_obj2.findall(res)
    
    str1 = '高' if result1.group(0) == 'high' else '低'
    str2 = ''
    datetime_15d_ago = datetime.datetime.now() - datetime.timedelta(days=15)

    for item in result2:
        datetime_befor = datetime.datetime(int(item[1]), int(item[2]), 
            int(item[3]), int(item[4]), int(item[5]), int(item[6]))
            
        if datetime_befor > datetime_15d_ago:
            str2 += item[0] + '\n'

    return(str2, '注释：端口%s收光告警,建议检查光路' % str1)

def warn5(res):
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


# 故障配置
g_gz_config = {
    r'XPL Errors': warn3,
    r'(P|Q)chip Errors': warn5,
    r'full speed': warn1,
    r'Temperature\s+: [6-9][0-9]C': warn2,
    r'rxOpticalPower-(low|high)-alarm': warn4
}

g_host = g_tb_config[0][0]
g_port = g_tb_config[0][1]
g_user = g_tb_config[0][2]
g_passwd = g_tb_config[0][3]
g_time_out = 60
# error_code = 0
g_prompt = '#'
g_unconnect_ip = []
g_date_path = ''
g_gz = []

# 指令列表
g_commands = []

CURRENT_TAB = crt.GetScriptTab()

def init():
    if not check_config_file():
        crt.Dialog.MessageBox('配置文件config.json或command.txt不存在，请检查')
        return False

    f_command = open('command.txt')
    global g_commands, g_date_path
    g_commands = f_command.readlines()
    f_command.close()
    if not g_commands:
        crt.Dialog.MessageBox('读取command内容为空，请检查')
        return False

    g_date_path = os.path.join(os.getcwd(), time.strftime(
    '%Y-%m-%d', time.localtime(time.time())))

    if not g_date_path:
        crt.Dialog.MessageBox('获取路径失败')
        return False

    return True
    

def check_config_file():
    if not os.path.exists('config.json'):
        return False
    if not os.path.exists('command.txt'):
        return False
    return True

def check_gz(result):
    for regex_str, make in g_gz_config.items():  
        gz_regex = re.compile(regex_str)
        res = gz_regex.search(result)
        if res:
            global g_gz
            info, warn = make(result)
            if not warn or not info:
                return
            gz_msg = [get_mid(g_prompt).encode('utf-8'), info, warn]
            if not gz_msg in g_gz:
                g_gz.append(gz_msg)



def connect_fail(ip):
    g_unconnect_ip.append(ip)
    CURRENT_TAB.Session.Disconnect()


def connect(cmd):
    error_code = 0
    try:
        CURRENT_TAB.Session.Connect(cmd)
    except ScriptError:
        error_code = crt.GetLastError()
    if error_code != 0:
        return False
    return True


def run_command(command):
    # 执行巡检命令
    CURRENT_TAB.Screen.Send(command + '\r')
    CURRENT_TAB.Screen.WaitForString('\r', g_time_out)
    CURRENT_TAB.Screen.WaitForString('\n', g_time_out)
    # 获取执行结果
    result = CURRENT_TAB.Screen.ReadString(g_prompt, g_time_out)
    return result


def login(ip, user, pwd):
    CURRENT_TAB.Screen.Send(ip+'\r')
    if CURRENT_TAB.Screen.WaitForStrings(["Login:", "username:"], 5, True) == 0:
        return False

    CURRENT_TAB.Screen.Send(user+'\r')
    CURRENT_TAB.Screen.WaitForString("Password:", g_time_out, True)
    CURRENT_TAB.Screen.Send(pwd+'\r')

    if not CURRENT_TAB.Screen.WaitForStrings(["#", ">"], g_time_out):
        return False

    return True

def make_path(city):

    if not os.path.exists(g_date_path):
        os.mkdir(g_date_path)
    city_path = os.path.join(g_date_path, city)
    if not os.path.exists(city_path):
        os.mkdir(city_path)

    return city_path


def save_from_list(file_name, data_list):
    f = open(file_name, 'w')
    for ip in data_list:
        f.write(ip + '\n')
    f.close()


def get_mid(prompt):
    mid = prompt.strip()
    mid = prompt.replace('.', '-')
    mid = mid.replace(':', '-')
    mid = mid.replace('*', '')
    mid = mid.replace('#', '')
    mid = mid.replace('<', '')
    mid = mid.replace('>', '')
    mid = mid.replace('/', '-')
    return mid


def run(login_name, password, ip, city):
    global g_user, g_passwd, g_host, g_port
    connect_str = ip
    city_path = make_path(city)
    if city.encode('utf-8') == '教育网':
        g_user = g_tb_config[1][2]
        g_passwd = g_tb_config[1][3]
        g_host = g_tb_config[1][0]
        g_port = g_tb_config[1][1]
    cmd = "/SSH2 /L %s /PASSWORD %s /C 3DES /M MD5 %s /P %s" % (
        g_user, g_passwd, g_host, g_port)
    if not connect(cmd):
        # crt.Dialog.MessageBox("跳板ip: %s, 连接失败" % host.encode('utf-8'))
        return
    if city == 'CE':
        for command in g_tb_config[2][4]:
            CURRENT_TAB.Screen.Send(command + '\r')
        if not CURRENT_TAB.Screen.WaitForString('CE', g_time_out):
            return False
        connect_str = 'telnet ' + ip
    if not login(connect_str, login_name, password):
        connect_fail(ip)
        # crt.Dialog.MessageBox('设备ip: %s, 登陆失败' % ip.encode('utf-8'))
        return
    global g_prompt
    g_prompt = CURRENT_TAB.Screen.Get(CURRENT_TAB.Screen.CurrentRow, 1, CURRENT_TAB.Screen.CurrentRow,
                                    CURRENT_TAB.Screen.CurrentColumn)

    mid = get_mid(g_prompt)
    file_name = os.path.join(city_path, mid+'.txt')
    # f_command = open('command.txt')
    f_result = open(file_name, 'w')
    for command in g_commands:
        result = run_command(command.strip('\n'))
        if not result:
            break
        check_gz(result)
        f_result.write(command + os.linesep + result + os.linesep)
        # time.sleep(1)
    # f_command.close()
    f_result.close()
    CURRENT_TAB.Session.Disconnect()


def test():
    CURRENT_TAB.Screen.IgnoreEscape = True
    CURRENT_TAB.Screen.Synchronous = True

    ip = '61.177.100.123'
    username = 'zyyc'
    password = 'Zyuc@@2014'
    city = '无锡'
    run(username, password, ip, city)


def main():
    
    if not init():
        return

    CURRENT_TAB.Screen.IgnoreEscape = True
    CURRENT_TAB.Screen.Synchronous = True

    f = open('config.json', 'r')
    json_data = json.loads(f.read())
    for city, data in json_data.items():
        for ip in data['ip']:
            run(data['username'], data['password'], ip, city)
        city_path = make_path(city)
        unconnect_file_name = os.path.join(city_path, 'unconnect_ip.txt')
        gz_file_name = os.path.join(city_path, 'gz.json')
       
        global g_unconnect_ip, g_gz
        save_from_list(unconnect_file_name, g_unconnect_ip)

        f = open(gz_file_name,'w')
        f.write(json.dumps(g_gz))
        f.close()
        # save_from_list(gz_file_name, g_gz)
        g_unconnect_ip = []
        g_gz = []


main()
# test()
