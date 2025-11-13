#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
爬虫启动脚本
"""
import sys
from scrapy.cmdline import execute

if __name__ == '__main__':
    sys.argv = ['scrapy', 'crawl', 'autohome']
    execute()
