#!/usr/bin/env python
#-*- coding:utf-8 -*-

basedigits='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
BASE=len(basedigits)
 
 
def decode(s):
    ret,mult = 0,1
    for c in reversed(s):
        ret += mult*basedigits.index(c)
        mult *= BASE
    return ret
 
def encode(num):
    if num <0: raise Exception("positive number "+ num)
    if num ==0: return '0'
    ret=''
    while num != 0:
        ret = (basedigits[num%BASE])+ret
        num = int(num/BASE)
    return ret


def url_to_mid(url):

    url = str(url)[::-1]
    size = len(url) / 4 if len(url) % 4 == 0 else len(url) / 4 + 1
    result = []
    for i in range(size):
        s = url[i * 4: (i + 1) * 4][::-1]
        s = str(decode(str(s)))
        s_len = len(s)
        if i < size - 1 and s_len < 7:
            s = (7 - s_len) * '0' + s
        result.append(s)
    result.reverse()
    return int(''.join(result))


def mid_to_url(midint):

    midint = str(midint)[::-1]
    size = len(midint) / 7 if len(midint) % 7 == 0 else len(midint) / 7 + 1
    result = []
    for i in range(size):
        s = midint[i * 7: (i + 1) * 7][::-1]
        s = encode(int(s))
        s_len = len(s)
        if i < size - 1 and len(s) < 4:
            s = '0' * (4 - s_len) + s
        result.append(s)
    result.reverse()
    return ''.join(result)

if __name__ == '__main__':
    #print encode(3621772148983960)
    print url_to_mid("A8NzeAdSG")