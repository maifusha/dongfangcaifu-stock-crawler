# -*- coding: utf-8 -*-

""" 公用助手函数 """


def filter_value(value, datatype, encode=None):
    strips = ['', '-', '--', None]

    if value in strips:
        return None
    elif encode:
        return datatype(value.encode(encode))
    else:
        return datatype(value)
