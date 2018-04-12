#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   gaofei
#   E-mail  :   gaofei@xunlei.com
#   Date    :   17/10/24 11:56:09
#   Desc    :
#
import logging
from logging.config import fileConfig

fileConfig('conf/logging_config.ini')
lgLogger = logging.getLogger('lg')
cjLogger = logging.getLogger('cj')

def cjlog(
            start_time,
            cost_time,
            action,
            tsid="",
            weight=0,
            io = "out",
            remote_name = "",
            remote_ip = "",
            version = 1,
            module = "ts_weight_calc",
            result = "",
            msg = "",
            eventid = "",
            device = "",
            userid = ""
            ):
    cjLogger.info('{s}{module}{s}{version}{s}'
                '{action}{s}{io}{s}{remote_name}'
                '{s}{remote_ip}{s}{start_time}{s}'
                '{cost_time}{s}{result}{s}{msg}{s}{eventid}'
                '{s}{device}{s}{userid}'
                '{s}{tsid}{s}{weight}'.format(s='\001',\
                module=module, version=version, action=action,\
                io=io, remote_name=remote_name, remote_ip=remote_ip, \
                start_time=start_time, cost_time=cost_time, \
                result=result, msg=msg, eventid=eventid, \
                device=device, userid=userid, tsid=tsid, weight=weight)
                )

