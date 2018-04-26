#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   gaofei
#   Date    :   18/04/26 11:07:27
#   Desc    :

import redis
from redis.sentinel import Sentinel

class RedisSentinel(object):
    """docstring for RedisSentinel"""
    def __init__(self, sentinel_addrs):
        super(RedisSentinel, self).__init__()
        self.m_sentinel = Sentinel(sentinel_addrs)
        self.m_sentinelIns = self.m_sentinel.sentinels[0]
        self.m_masters = self.get_masters()
        self.m_slaves = self.get_slaves()

    def get_masters(self):
        masters = {}
        masterDetail = self.m_sentinelIns.sentinel_masters()
        for name in masterDetail:
            masters[name] = (masterDetail[name]['ip'], masterDetail[name]['port'])
        return masters


    def get_slaves(self):
        slaves = {}
        for name in self.m_masters:
            slave = self.m_sentinel.discover_slaves(name)
            if len(slave) > 0:
                slaves[name] = (slave[0][0], slave[0][1])
        return slaves

