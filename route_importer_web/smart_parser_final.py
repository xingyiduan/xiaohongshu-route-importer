#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终版本的智能解析器管理器
优先使用火山引擎豆包API，失败时回退到规则解析器
"""

import logging
from typing import Dict, Optional
from volcengine_douban_final import VolcengineDoubanParser
from note_parser import XiaohongshuNoteParser

class SmartParser:
    """智能解析器管理器"""
    
    def __init__(self, volcengine_api_key: str = None):
        """初始化智能解析器"""
        self.logger = logging.getLogger(__name__)
        
        # 初始化火山引擎豆包AI解析器
        self.volcengine_parser = VolcengineDoubanParser(volcengine_api_key)
        
        # 初始化规则解析器（作为备选）
        self.rule_parser = XiaohongshuNoteParser()
        
        # 解析策略配置 - 暂时禁用规则解析器回退，专注豆包API
        self.use_ai_first = True  # 优先使用AI
        self.fallback_to_rule = False  # 暂时禁用回退到规则解析器
        
        self.logger.info("智能解析器初始化完成")
        self.logger.info(f"AI优先: {self.use_ai_first}")
        self.logger.info(f"规则解析器回退: {self.fallback_to_rule}")
        self.logger.info("注意: 当前配置下，如果豆包API失败，将不会回退到规则解析器")
    
    def parse_note(self, text: str, url: str = "") -> Optional[Dict]:
        """
        智能解析小红书笔记
        
        Args:
            text: 提取的文本内容（如果为空，将从URL中提取）
            url: 原始链接
            
        Returns:
            解析后的笔记数据
        """
        # 如果text为空，先从URL中提取文本
        if not text and url:
            self.logger.info("文本内容为空，从URL中提取文本...")
            try:
                # 使用规则解析器的方法提取原始文本
                # 先尝试解析一次，获取提取的文本
                temp_result = self.rule_parser.parse_note(url)
                if temp_result:
                    # 从debug文件中读取提取的文本
                    try:
                        with open('debug_extracted_text.txt', 'r', encoding='utf-8') as f:
                            raw_text = f.read()
                        if raw_text:
                            text = raw_text
                            self.logger.info(f"从URL提取到文本，长度: {len(text)} 字符")
                        else:
                            self.logger.warning("无法从debug文件读取文本")
                    except FileNotFoundError:
                        self.logger.warning("debug文件不存在，无法提取文本")
                else:
                    self.logger.warning("无法从URL提取文本")
            except Exception as e:
                self.logger.error(f"从URL提取文本失败: {str(e)}")
        
        # 策略1：优先使用火山引擎豆包AI解析器
        if self.use_ai_first and self.volcengine_parser.is_available() and text:
            self.logger.info("尝试使用火山引擎豆包AI解析器...")
            
            try:
                result = self.volcengine_parser.parse_note(text, url)
                # 检查多路线结构或单路线结构
                places_count = 0
                if result and result.get('routes'):
                    # 多路线结构：统计所有路线的地点总数
                    for route in result['routes']:
                        if route.get('places'):
                            places_count += len(route['places'])
                elif result and result.get('places'):
                    # 单路线结构：直接统计地点数量
                    places_count = len(result['places'])
                
                if result and places_count > 0:
                    self.logger.info(f"火山引擎豆包AI解析成功！提取到 {places_count} 个POI")
                    return result
                else:
                    self.logger.warning("火山引擎豆包AI解析失败或无POI结果")
            except Exception as e:
                self.logger.error(f"火山引擎豆包AI解析器异常: {str(e)}")
        
        # 策略2：回退到规则解析器
        if self.fallback_to_rule:
            self.logger.info("回退到规则解析器...")
            
            try:
                result = self.rule_parser.parse_note(url)
                # 检查多路线结构或单路线结构
                places_count = 0
                if result and result.get('routes'):
                    # 多路线结构：统计所有路线的地点总数
                    for route in result['routes']:
                        if route.get('places'):
                            places_count += len(route['places'])
                elif result and result.get('places'):
                    # 单路线结构：直接统计地点数量
                    places_count = len(result['places'])
                
                if result and places_count > 0:
                    self.logger.info(f"规则解析器解析成功！提取到 {places_count} 个POI")
                    return result
                else:
                    self.logger.warning("规则解析器解析失败或无结果")
            except Exception as e:
                self.logger.error(f"规则解析器异常: {str(e)}")
        
        self.logger.error("所有解析器都失败了")
        return None
    
    def get_parser_info(self) -> Dict:
        """获取解析器信息"""
        volcengine_stats = self.volcengine_parser.get_usage_stats() if self.volcengine_parser.is_available() else {}
        
        return {
            'primary_parser': 'volcengine_douban' if self.volcengine_parser.is_available() else 'rule_parser',
            'volcengine_available': self.volcengine_parser.is_available(),
            'volcengine_usage': volcengine_stats,
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
        
        # 测试火山引擎豆包AI解析器
        if self.volcengine_parser.is_available():
            try:
                volcengine_result = self.volcengine_parser.parse_note(test_text)
                results['volcengine_douban'] = {
                    'success': volcengine_result is not None,
                    'places_count': len(volcengine_result.get('places', [])) if volcengine_result else 0,
                    'result': volcengine_result
                }
            except Exception as e:
                results['volcengine_douban'] = {
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
