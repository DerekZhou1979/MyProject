#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
小红书笔记查询系统启动脚本
"""

from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 