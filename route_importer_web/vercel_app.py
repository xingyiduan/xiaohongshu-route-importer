#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vercel部署专用入口点
"""

from app import app

# 导出Flask应用实例供Vercel使用
app.debug = False
