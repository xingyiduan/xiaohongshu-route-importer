#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
正确的火山引擎豆包API调用器（基于官方示例）
"""

import json
import requests
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta

class VolcengineDoubanParser:
    """使用火山引擎豆包大模型的智能POI解析器"""
    
    def __init__(self, api_key: str = None):
        """初始化火山引擎豆包API解析器"""
        # 优先使用传入的API密钥，其次使用环境变量
        if api_key and api_key != "your_volcengine_api_key_here":
            self.api_key = api_key
        else:
            import os
            self.api_key = os.environ.get('VOLCENGINE_API_KEY') or "your_volcengine_api_key_here"
        
        # 火山引擎豆包API正确端点
        self.api_url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
        
        # 设置日志
        self.logger = logging.getLogger(__name__)
        
        # 设置请求头 - 使用Bearer认证
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 调用次数限制
        self.max_calls_per_day = 100
        self.max_calls_per_minute = 10
        self.call_history = []
        
        # 记录初始化信息
        self.logger.info(f"火山引擎豆包API解析器初始化完成")
        self.logger.info(f"API密钥: {self.api_key[:10]}...")
        self.logger.info(f"API可用性: {self.is_available()}")
        
    def can_make_call(self) -> bool:
        """检查是否可以发起API调用"""
        now = datetime.now()
        self.call_history = [call_time for call_time in self.call_history 
                           if now - call_time < timedelta(days=1)]
        
        if len(self.call_history) >= self.max_calls_per_day:
            return False
        
        recent_calls = [call_time for call_time in self.call_history 
                       if now - call_time < timedelta(minutes=1)]
        if len(recent_calls) >= self.max_calls_per_minute:
            return False
        
        return True
    
    def record_call(self):
        """记录API调用"""
        self.call_history.append(datetime.now())
    
    def parse_note(self, text: str, url: str = "") -> Optional[Dict]:
        """使用火山引擎豆包大模型解析小红书笔记"""
        if not self.can_make_call():
            self.logger.warning("API调用受限")
            return None
        
        # 重试机制
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.logger.info(f"开始使用火山引擎豆包大模型解析笔记 (尝试 {attempt + 1}/{max_retries})")
                
                # 构建提示词
                prompt = self._build_prompt(text)
                
                # 构建请求数据 - 使用官方格式
                request_data = {
                    "model": "doubao-seed-1-6-250615",  # 官方模型名称
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": prompt
                                }
                            ]
                        }
                    ]
                }
                
                # 记录调用
                self.record_call()
                
                print(f"发送请求到: {self.api_url}")
                print(f"请求头: {self.headers}")
                print(f"请求数据: {json.dumps(request_data, ensure_ascii=False, indent=2)}")
                
                # 调用火山引擎豆包API - 使用更长的超时时间
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=request_data,
                    timeout=120  # 增加超时时间到120秒，给API充足的响应时间
                )
                
                print(f"响应状态码: {response.status_code}")
                print(f"响应头: {dict(response.headers)}")
                print(f"响应内容: {response.text[:500]}...")
                
                if response.status_code == 200:
                    try:
                        result = response.json()
                        print(f"解析后的响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
                        
                        if 'choices' in result and len(result['choices']) > 0:
                            ai_response = result['choices'][0]['message']['content']
                            parsed_data = self._parse_ai_response(ai_response)
                            if parsed_data:
                                self.logger.info(f"火山引擎豆包AI解析成功，提取到 {len(parsed_data.get('places', []))} 个POI")
                                return parsed_data
                            else:
                                self.logger.warning("火山引擎豆包AI返回的数据格式无效")
                                return None
                        else:
                            self.logger.error("火山引擎豆包API返回格式异常")
                            return None
                    except json.JSONDecodeError:
                        self.logger.error("响应不是有效的JSON格式")
                        return None
                else:
                    self.logger.error(f"火山引擎豆包API调用失败，状态码: {response.status_code}")
                    return None
                    
            except requests.exceptions.Timeout:
                self.logger.warning(f"第 {attempt + 1} 次尝试超时 (120秒)")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 10  # 递增等待时间：10秒、20秒、30秒
                    self.logger.info(f"等待 {wait_time} 秒后重试...")
                    import time
                    time.sleep(wait_time)
                    continue
                else:
                    self.logger.error("所有重试都超时了，豆包API可能需要更长的响应时间")
                    return None
            except Exception as e:
                self.logger.error(f"火山引擎豆包AI解析失败: {str(e)}")
                return None
        
        return None
    
    def _build_prompt(self, text: str) -> str:
        """构建发送给豆包的提示词"""
        prompt = f"""
你是一个专业的旅游路线分析助手。请分析以下小红书笔记，提取其中的地点信息（POI）。

**任务要求：**
1. 识别笔记中提到的所有具体地点（如车站、景点、餐厅、商店等）
2. 过滤掉描述性文字、人物、情感表达等非地点内容
3. 返回结构化的JSON数据

**重要规则：**
- 只提取有明确名称的地点，如"日暮里站"、"朝仓雕塑馆"、"Museca Times"等
- 不要提取描述性内容，如"土耳其风格的灯具店"、"卖各种包包和伞的店"等
- 如果某个地点没有具体名称，只有描述，则不要提取
- 确保每个提取的地点都有明确的、可识别的名称

**输入文本：**
{text}

**输出格式要求：**
请返回一个JSON对象，包含以下字段：
{{
    "title": "笔记标题",
    "content": "笔记主要内容摘要",
    "places": [
        {{
            "name": "地点名称（必须是明确的地点名）",
            "description": "地点描述",
            "category": "地点类别",
            "address": "地址信息（如果有）"
        }}
    ],
    "tags": ["标签1", "标签2"],
    "route_type": "路线类型（如：步行、观光等）"
}}

**地点提取标准：**
✅ 应该提取的地点类型：
- 车站、机场等交通枢纽（如：日暮里站）
- 景点、博物馆、神社等（如：朝仓雕塑馆、猫猫神社）
- 有具体名称的餐厅、商店（如：Museca Times）
- 有明确名称的商业区、街道（如：谷中银座商业街）

❌ 不应该提取的内容：
- 描述性文字（如："土耳其风格的灯具店"、"卖各种包包和伞的店"）
- 没有具体名称的商店描述
- 情感表达、评价内容
- 人物、时间等非地点信息

**注意事项：**
- 只提取真实存在的地点，不要包含虚拟或描述性内容
- 地点名称要准确，不要包含多余的修饰词
- 如果文本中没有明确的地点信息，返回空的地点列表
- 确保返回的是有效的JSON格式
- 严格遵循地点提取标准，宁可少提取也不要提取不明确的地点

请直接返回JSON，不要包含其他文字说明。
"""
        return prompt
    
    def _parse_ai_response(self, response_text: str) -> Optional[Dict]:
        """解析AI返回的响应"""
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                self.logger.error("AI响应中未找到JSON内容")
                return None
            
            json_text = response_text[json_start:json_end]
            parsed_data = json.loads(json_text)
            
            if not isinstance(parsed_data, dict):
                return None
            
            if 'places' not in parsed_data:
                parsed_data['places'] = []
            
            if 'title' not in parsed_data:
                parsed_data['title'] = "未命名路线"
            
            if 'content' not in parsed_data:
                parsed_data['content'] = ""
            
            if 'tags' not in parsed_data:
                parsed_data['tags'] = []
            
            places = []
            for place in parsed_data['places']:
                if isinstance(place, dict) and 'name' in place:
                    places.append({
                        'name': place['name'],
                        'description': place.get('description', ''),
                        'address': place.get('address', place['name']),
                        'category': self._map_category(place.get('category', '')),
                        'coordinates': self._get_coordinates_from_address(place.get('address', place['name'])),
                        'source': 'volcengine_douban'
                    })
            
            parsed_data['places'] = places
            return parsed_data
            
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON解析失败: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"解析AI响应失败: {str(e)}")
            return None
    
    def _map_category(self, ai_category: str) -> str:
        """将AI返回的类别映射到系统类别"""
        category_mapping = {
            'transportation': 'transportation',
            'station': 'transportation',
            '地铁站': 'transportation',
            '车站': 'transportation',
            'attraction': 'attraction',
            '景点': 'attraction',
            '博物馆': 'attraction',
            '展览馆': 'attraction',
            '雕塑馆': 'attraction',
            'shopping': 'shopping',
            '购物': 'shopping',
            '商业街': 'shopping',
            '商店': 'shopping',
            'restaurant': 'restaurant',
            '餐厅': 'restaurant',
            '美食': 'restaurant',
            '汉堡店': 'restaurant',
            'temple': 'attraction',
            '神社': 'attraction',
            '寺庙': 'attraction',
            'park': 'park',
            '公园': 'park',
            '广场': 'park'
        }
        
        return category_mapping.get(ai_category.lower(), 'other')
    
    def _get_coordinates_from_address(self, address: str) -> Dict[str, float]:
        """从地址获取坐标"""
        return {
            'latitude': 35.7278,
            'longitude': 139.7708
        }
    
    def is_available(self) -> bool:
        """检查火山引擎豆包API是否可用"""
        return self.api_key != "your_volcengine_api_key_here"
    
    def get_usage_stats(self) -> Dict:
        """获取API使用统计"""
        now = datetime.now()
        today_calls = len([call_time for call_time in self.call_history 
                          if now - call_time < timedelta(days=1)])
        minute_calls = len([call_time for call_time in self.call_history 
                           if now - call_time < timedelta(minutes=1)])
        
        return {
            'today_calls': today_calls,
            'max_daily_calls': self.max_calls_per_day,
            'minute_calls': minute_calls,
            'max_minute_calls': self.max_calls_per_minute,
            'remaining_daily': self.max_calls_per_day - today_calls
        }
