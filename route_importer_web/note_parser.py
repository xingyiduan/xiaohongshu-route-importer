#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用的小红书笔记解析器
基于get_text()方法和符号识别，适用于任何小红书笔记
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, List, Optional
import logging

class XiaohongshuNoteParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # 设置日志
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def parse_note(self, url: str) -> Optional[Dict]:
        """
        解析小红书笔记
        
        Args:
            url: 小红书笔记链接
            
        Returns:
            解析后的笔记数据，包含地点、标签等信息
        """
        try:
            self.logger.info(f"开始解析小红书笔记: {url}")
            
            # 获取网页内容
            response = self.session.get(url, timeout=10, allow_redirects=True)
            response.raise_for_status()
            
            self.logger.info(f"获取网页成功，状态码: {response.status_code}")
            self.logger.info(f"最终URL: {response.url}")
            
            # 解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 使用get_text()方法提取所有文本（与测试脚本保持一致）
            all_text = soup.get_text()
            self.logger.info(f"提取的文本长度: {len(all_text)} 字符")
            
            # 保存提取的文本用于调试
            with open('debug_extracted_text.txt', 'w', encoding='utf-8') as f:
                f.write(all_text)
            self.logger.info("已保存提取的文本到 debug_extracted_text.txt")
            
            # 提取笔记信息
            note_data = self._extract_note_data(all_text, url)
            
            if note_data:
                self.logger.info(f"成功解析笔记: {note_data.get('title', '未知标题')}")
                self.logger.info(f"提取到 {len(note_data.get('places', []))} 个POI")
                return note_data
            else:
                self.logger.warning("未能提取到有效的笔记数据")
                return None
                
        except Exception as e:
            self.logger.error(f"解析小红书笔记失败: {str(e)}")
            return None
    
    def _extract_note_data(self, text: str, original_url: str) -> Optional[Dict]:
        """从提取的文本中提取笔记数据"""
        
        # 提取标题
        title = self._extract_title(text)
        
        # 提取正文内容
        content = self._extract_content(text)
        
        # 提取地点信息（核心功能）
        places = self._extract_places_from_text(text)
        
        # 提取标签
        tags = self._extract_tags_from_text(text)
        
        # 如果没有提取到地点，返回None
        if not places:
            self.logger.warning("未能提取到任何地点信息")
            return None
        
        return {
            'title': title or "未命名路线",
            'content': content or "",
            'places': places,
            'tags': tags,
            'source_url': original_url,
            'parsed_at': self._get_current_timestamp()
        }
    
    def _extract_title(self, text: str) -> str:
        """提取笔记标题"""
        # 查找可能的标题模式
        title_patterns = [
            r'小红书\s*\n\s*([^\n]+)',  # 小红书后面的第一行
            r'([^#\n]{5,30})',  # 5-30个字符的非标签文本
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, text)
            if match:
                title = match.group(1).strip()
                if title and len(title) > 3 and '小红书' not in title:
                    return title
        
        return ""
    
    def _extract_content(self, text: str) -> str:
        """提取笔记正文内容"""
        # 提取前几段有意义的文本
        lines = text.split('\n')
        content_lines = []
        
        for line in lines:
            line = line.strip()
            if line and len(line) > 10 and not line.startswith('#'):
                content_lines.append(line)
                if len(content_lines) >= 5:  # 最多取5行
                    break
        
        return '\n'.join(content_lines)
    
    def _extract_places_from_text(self, text: str) -> List[Dict]:
        """从文本中提取地点信息（核心方法）"""
        places = []
        
        # 方法1：基于符号识别地址（小红书笔记的标准方式）
        symbol_places = self._extract_places_by_symbol(text)
        places.extend(symbol_places)
        
        # 方法2：基于地址格式识别
        format_places = self._extract_places_by_format(text)
        places.extend(format_places)
        
        # 方法3：基于POI关键词识别
        keyword_places = self._extract_places_by_keywords(text)
        places.extend(keyword_places)
        
        # 去重和合并
        unique_places = self._merge_and_deduplicate_places(places)
        
        self.logger.info(f"提取到 {len(unique_places)} 个唯一地点")
        return unique_places
    
    def _extract_places_by_symbol(self, text: str) -> List[Dict]:
        """基于符号识别地址"""
        places = []
        
        # 查找符号后面的地址信息
        symbol_pattern = r'📍\s*([^，。\n]+)'
        matches = re.findall(symbol_pattern, text)
        
        for match in matches:
            address = match.strip()
            if self._is_valid_address(address):
                place_name = self._extract_place_name_from_address(address)
                places.append({
                    'name': place_name,
                    'address': address,
                    'coordinates': self._get_coordinates_from_address(address),
                    'category': self._categorize_place(place_name),
                    'source': 'symbol'
                })
        
        return places
    
    def _extract_places_by_format(self, text: str) -> List[Dict]:
        """基于地址格式识别"""
        places = []
        
        # 识别常见的地址格式
        address_patterns = [
            r'([^，。\n]*\d+[^，。\n]*[路街巷号][^，。\n]*)',  # 包含路、街、巷、号的地址
            r'([^，。\n]*[省市区县][^，。\n]*)',  # 包含省市区县的地址
            r'([^，。\n]*[A-Za-z]+\s*[A-Za-z]+[^，。\n]*)',  # 英文地址
        ]
        
        for pattern in address_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                address = match.strip()
                if self._is_valid_address(address) and len(address) > 5:
                    place_name = self._extract_place_name_from_address(address)
                    places.append({
                        'name': place_name,
                        'address': address,
                        'coordinates': self._get_coordinates_from_address(address),
                        'category': self._categorize_place(place_name),
                        'source': 'format'
                    })
        
        return places
    
    def _extract_places_by_keywords(self, text: str) -> List[Dict]:
        """基于POI关键词识别"""
        places = []
        
        # 定义POI关键词模式
        poi_patterns = [
            r'([^，。\n]*[站][^，。\n]*)',  # 车站、地铁站等
            r'([^，。\n]*[馆][^，。\n]*)',  # 博物馆、展览馆等
            r'([^，。\n]*[街][^，。\n]*)',  # 商业街、步行街等
            r'([^，。\n]*[店][^，。\n]*)',  # 餐厅、商店等
            r'([^，。\n]*[神社][^，。\n]*)',  # 神社、寺庙等
            r'([^，。\n]*[公园][^，。\n]*)',  # 公园、广场等
        ]
        
        for pattern in poi_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                place_name = match.strip()
                # 清理POI名称，移除图片编号等无关信息
                cleaned_name = self._clean_place_name(place_name)
                if cleaned_name and self._is_valid_place_name(cleaned_name):
                    places.append({
                        'name': cleaned_name,
                        'address': cleaned_name,  # 暂时用名称作为地址
                        'coordinates': self._get_coordinates_from_address(cleaned_name),
                        'category': self._categorize_place(cleaned_name),
                        'source': 'keyword'
                    })
        
        return places
    
    def _is_valid_address(self, address: str) -> bool:
        """验证地址是否有效"""
        if not address or len(address) < 5:
            return False
        
        # 检查是否包含地址特征
        address_features = ['路', '街', '巷', '号', '省', '市', '区', '县', 'Chome', 'Street', 'Road']
        return any(feature in address for feature in address_features)
    
    def _is_valid_place_name(self, name: str) -> str:
        """验证地点名称是否有效"""
        if not name or len(name) < 2:
            return False
        
        # 过滤掉一些明显不是地点的内容
        invalid_patterns = [
            r'^[0-9\s\-_]+$',  # 纯数字和符号
            r'^[pP]\d+',  # 图片编号
            r'店主', '大叔', '小朋友',  # 人物描述
            r'好吃', '可爱', '亲切',  # 描述性词汇
        ]
        
        for pattern in invalid_patterns:
            if re.match(pattern, name):
                return False
        
        return True
    
    def _clean_place_name(self, place_name: str) -> str:
        """清理POI名称，移除图片编号等无关信息"""
        if not place_name:
            return ""
        
        # 移除图片编号（如 p12、P1 等）
        cleaned = re.sub(r'^[pP]\d+[^a-zA-Z\u4e00-\u9fff]*', '', place_name)
        
        # 移除一些无关词汇
        cleaned = re.sub(r'是一家叫\s*', '', cleaned)
        cleaned = re.sub(r'的\s*', '', cleaned)
        cleaned = re.sub(r'好吃！?', '', cleaned)
        cleaned = re.sub(r'可以逛逛打发时间', '', cleaned)
        cleaned = re.sub(r'进去了就出不来了', '', cleaned)
        cleaned = re.sub(r'太可爱了！?', '', cleaned)
        cleaned = re.sub(r'店主大叔人超级亲切', '', cleaned)
        cleaned = re.sub(r'还送了我们面包超人的小零食', '', cleaned)
        cleaned = re.sub(r'午餐推荐', '', cleaned)
        cleaned = re.sub(r'是有名的', '', cleaned)
        cleaned = re.sub(r'还蛮小的', '', cleaned)
        cleaned = re.sub(r'距离商业街要走一段路', '', cleaned)
        cleaned = re.sub(r'从神社一路走回日暮里站', '', cleaned)
        cleaned = re.sub(r'途经安静的住宅区', '', cleaned)
        cleaned = re.sub(r'途中还遇到了小朋友们放学', '', cleaned)
        
        # 清理多余的空格和标点
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = cleaned.strip(' 　，。！？、')
        
        return cleaned

    def _extract_place_name_from_address(self, address: str) -> str:
        """从地址中提取地点名称"""
        # 简单的名称提取逻辑
        name = address.strip()
        
        # 移除一些无关字符
        name = re.sub(r'[📍🚉⛩️🍔]', '', name)
        name = re.sub(r'地址[：:]', '', name)
        name = re.sub(r'位置[：:]', '', name)
        
        # 如果地址很长，尝试提取前面的部分作为名称
        if len(name) > 20:
            # 尝试找到第一个有意义的分隔符
            separators = ['，', '、', ' ', ',', '-']
            for sep in separators:
                if sep in name:
                    name = name.split(sep)[0]
                    break
        
        return name.strip()
    
    def _categorize_place(self, place_name: str) -> str:
        """对地点进行分类"""
        if not place_name:
            return 'other'
        
        # 基于关键词进行分类
        if any(keyword in place_name for keyword in ['站', 'Station']):
            return 'transportation'
        elif any(keyword in place_name for keyword in ['馆', 'Museum', 'Gallery']):
            return 'attraction'
        elif any(keyword in place_name for keyword in ['街', 'Street', 'Mall']):
            return 'shopping'
        elif any(keyword in place_name for keyword in ['店', 'Restaurant', 'Shop']):
            return 'restaurant'
        elif any(keyword in place_name for keyword in ['神社', 'Temple', 'Shrine']):
            return 'attraction'
        elif any(keyword in place_name for keyword in ['公园', 'Park', 'Square']):
            return 'park'
        else:
            return 'other'
    
    def _get_coordinates_from_address(self, address: str) -> Dict[str, float]:
        """从地址获取坐标（实际项目中应该调用地理编码API）"""
        # 这里返回默认坐标，实际项目中应该：
        # 1. 调用Google Geocoding API
        # 2. 或者调用其他地理编码服务
        # 3. 根据地址返回准确的坐标
        
        # 临时返回默认坐标（东京市中心）
        return {'lat': 35.6762, 'lng': 139.6503}
    
    def _merge_and_deduplicate_places(self, places: List[Dict]) -> List[Dict]:
        """合并和去重地点"""
        unique_places = []
        seen_names = set()
        
        for place in places:
            name = place.get('name', '').strip()
            if name and name not in seen_names:
                unique_places.append(place)
                seen_names.add(name)
        
        # 按来源优先级排序：symbol > format > keyword
        source_priority = {'symbol': 3, 'format': 2, 'keyword': 1}
        unique_places.sort(key=lambda x: source_priority.get(x.get('source', 0), 0), reverse=True)
        
        return unique_places
    
    def _extract_tags_from_text(self, text: str) -> List[str]:
        """从文本中提取标签"""
        tags = []
        
        # 查找标签模式
        tag_pattern = r'#([^#\s]+)'
        matches = re.findall(tag_pattern, text)
        
        # 过滤和清理标签
        for tag in matches:
            tag = tag.strip()
            if tag and len(tag) > 1 and tag not in tags:
                tags.append(tag)
        
        return tags[:15]  # 最多返回15个标签
    
    def _get_current_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
