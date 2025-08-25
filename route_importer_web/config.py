#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件
"""

import os
from datetime import timedelta

class Config:
    """应用配置"""
    
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    APP_NAME = '小红书路线导入器'
    DEBUG = True
    
    # 地图服务配置
    MAP_SERVICE = 'google_maps'  # 支持: google_maps, baidu_maps, amap
    
    # 数据库配置
    DATABASE_PATH = 'routes.db'
    
    # 解析和规划超时设置
    PARSING_TIMEOUT = 30  # 秒
    PLANNING_TIMEOUT = 60  # 秒
    
    # Gemini API配置
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or 'your_gemini_api_key_here'
    GEMINI_MODEL = 'gemini-1.5-flash'  # 使用最新的Gemini模型
    
    # 解析器配置
    USE_AI_PARSER = True  # 是否使用AI解析器
    FALLBACK_TO_RULE_PARSER = True  # AI失败时是否回退到规则解析器
    
    # 日志配置
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'app.log'
