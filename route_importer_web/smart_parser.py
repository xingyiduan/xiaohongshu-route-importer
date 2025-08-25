#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能解析器管理器
优先使用豆包API，失败时回退到规则解析器
"""

import logging
from typing import Dict, Optional
from douban_parser import DoubanAIParser
from note_parser import XiaohongshuNoteParser

class SmartParser:
    """智能解析器管理器"""
    
    def __init__(self, douban_api_key: str = None):
        """初始化智能解析器"""
        self.logger = logging.getLogger(__name__)
        
        # 初始化豆包AI解析器
        self.douban_parser = DoubanAIParser(douban_api_key)
        
        # 初始化规则解析器（作为备选）
        self.rule_parser = XiaohongshuNoteParser()
        
        # 解析策略配置
        self.use_ai_first = True  # 优先使用AI
        self.fallback_to_rule = True  # 失败时回退到规则解析
        
    def parse_note(self, text: str, url: str = "") -> Optional[Dict]:
        """
        智能解析小红书笔记
        
        Args:
            text: 提取的文本内容
            url: 原始链接
            
        Returns:
            解析后的笔记数据
        """
        # 策略1：优先使用豆包AI解析器
        if self.use_ai_first and self.douban_parser.is_available():
            self.logger.info("尝试使用豆包AI解析器...")
            
            try:
                result = self.douban_parser.parse_note(text, url)
                if result and result.get('places'):
                    self.logger.info("豆包AI解析成功！")
                    return result
                else:
                    self.logger.warning("豆包AI解析失败或无结果")
            except Exception as e:
                self.logger.error(f"豆包AI解析器异常: {str(e)}")
        
        # 策略2：回退到规则解析器
        if self.fallback_to_rule:
            self.logger.info("回退到规则解析器...")
            
            try:
                result = self.rule_parser.parse_note(url)
                if result and result.get('places'):
                    self.logger.info("规则解析器解析成功！")
                    return result
                else:
                    self.logger.warning("规则解析器解析失败或无结果")
            except Exception as e:
                self.logger.error(f"规则解析器异常: {str(e)}")
        
        self.logger.error("所有解析器都失败了")
        return None
    
    def get_parser_info(self) -> Dict:
        """获取解析器信息"""
        douban_stats = self.douban_parser.get_usage_stats() if self.douban_parser.is_available() else {}
        
        return {
            'primary_parser': 'douban_ai' if self.douban_parser.is_available() else 'rule_parser',
            'douban_available': self.douban_parser.is_available(),
            'douban_usage': douban_stats,
            'fallback_enabled': self.fallback_to_rule,
            'strategy': 'ai_first_with_fallback' if self.use_ai_first else 'rule_only'
        }
    
    def set_strategy(self, use_ai_first: bool = True, fallback_to_rule: bool = True):
        """设置解析策略"""
        self.use_ai_first = use_ai_first
        self.fallback_to_rule = fallback_to_rule
        
        self.logger.info(f"解析策略已更新: AI优先={use_ai_first}, 回退到规则={fallback_to_rule}")
    
    def test_parsers(self, test_text: str) -> Dict:
        """测试所有解析器"""
        results = {}
        
        # 测试豆包AI解析器
        if self.douban_parser.is_available():
            try:
                douban_result = self.douban_parser.parse_note(test_text)
                results['douban_ai'] = {
                    'success': douban_result is not None,
                    'places_count': len(douban_result.get('places', [])) if douban_result else 0,
                    'result': douban_result
                }
            except Exception as e:
                results['douban_ai'] = {
                    'success': False,
                    'error': str(e)
                }
        
        # 测试规则解析器
        try:
            rule_result = self.rule_parser.parse_note(test_text)
            results['rule_parser'] = {
                'success': rule_result is not None,
                'places_count': len(rule_result.get('places', [])) if rule_result else 0,
                'result': rule_result
            }
        except Exception as e:
            results['rule_parser'] = {
                'success': False,
                'error': str(e)
            }
        
        return results
