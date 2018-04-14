#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

json_data = {
    '南京': {
        'username':'zyyc',
        'password':'Zyuc@@2014',
        'ip':[]
    },
    '泰州': {
        'username':'zyyc',
        'password':'Zyuc@@2014',
        'ip':[]
    },
    '镇江': {
        'username':'zyyc',
        'password':'Zyuc@@2014',
        'ip':[]
    },
    '徐州': {
        'username':'zyyc',
        'password':'Zyuc@@2014',
        'ip':[]
    },
    '无锡': {
        'username':'zyyc',
        'password':'Zyuc@@2014',
        'ip':[]
    },
    '扬州': {
        'username':'zyyc',
        'password':'Zyuc@@2014',
        'ip':[]
    },
    '常州': {
        'username':'zyyc',
        'password':'Zyuc@@2014',
        'ip':[]
    },
    '苏州': {
        'username':'zyyc',
        'password':'Zyuc@@2014',
        'ip':[]
    },
    '南通': {
        'username':'zyyc',
        'password':'Zyuc@@2014',
        'ip':[]
    },
    '连云港': {
        'username':'zyyc',
        'password':'Zyuc@@2014',
        'ip':[]
    },
    '淮安': {
        'username':'zyyc',
        'password':'Zyuc@@2014',
        'ip':[]
    },
    '盐城': {
        'username':'zyyc',
        'password':'Zyuc@@2014',
        'ip':[]
    },
    '宿迁': {
        'username':'zyyc',
        'password':'Zyuc@@2014',
        'ip':[]
    },
}

f = open('iplist.ini','r')

res = f.read()
list1 = res.split('\n\n')

index = 0

for key, value in json_data.items():
    for ip in list1[index].split('\n'):
        if ']' not in ip and 'username' not in ip and 'password' not in ip:
            json_data[key]['ip'].append(ip.strip())

    index += 1
json_res = json.dumps(json_data,ensure_ascii=False)

c = open('config.json','w',encoding='utf-8')

c.write(json_res)
c.close()
f.close()
print(json_res)

# print(json_data['TZ']['ip'])