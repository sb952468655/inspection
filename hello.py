# 我的第一个Python程序
# -*- coding: utf-8 -*-

def my_abs(x):
    if not isinstance(x, (int,float)):
        raise TypeError('bad operand type')
    if x > 0:
        return x
    else:
        return -x


def get_pos():
    x = 2
    y = 3
    return x,y

def add(x, y, f):
    return f(x) + f(y)
