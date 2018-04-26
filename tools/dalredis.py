#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   gaofei
#   Date    :   18/04/26 11:17:34
#   Desc    :

from redis_sentinel import *
from logger import *

sentinel_addr = ("10.33.21.80", int(11000))

redisentinel = RedisSentinel([sentinel_addr])

g_match_dev = "*891X*"

def find_login_device(match_dev, addr, db=14):
    r = redis.Redis(host=addr[0], port=int(addr[1]), db=db)
    cnt = 0
    for key in r.scan_iter(match=match_dev, count=5000):
        cnt = cnt + 1
        dev_info = r.hgetall(key)
        if int(dev_info["login_status"]) != 0:
            lgger.info("{key} {info}".format(key=key, info=dev_info))
    if cnt > 0:
        lgger.info("matched {cnt} keys in {addr}".format(cnt=cnt, addr=addr))
    return cnt


def find_login_device_in_cluster(match_dev):
    tot_num = 0
    for name,addr in redisentinel.m_slaves.items():
        # print name,addr
        lgger.info("scan {name} {addr}".format(name=name,addr=addr))
        consoleloger.info("scan {name} {addr}".format(name=name,addr=addr))
        tot_num = tot_num + find_login_device(match_dev, addr)
        # break
    consoleloger.info("tot_num={tot_num}".format(tot_num=tot_num))


if __name__ == '__main__':
    find_login_device_in_cluster(g_match_dev)

