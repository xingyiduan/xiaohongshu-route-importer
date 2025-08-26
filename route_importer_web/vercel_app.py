#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vercel部署专用入口点
"""

from app import app

# 导出Flask应用实例供Vercel使用
app.debug = False

# 确保数据库初始化
try:
    app.db.init_database()
except:
    pass

# 导出应用实例
application = app
