#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   gaofei
#   Date    :   17/10/24 11:56:09
#   Desc    :
#
#
import logging
from logging.config import fileConfig

fileConfig('conf/logging_config.ini')
lgger = logging.getLogger('lg')
cgger = logging.getLogger('cj')
consoleloger = logging.getLogger('console')
