#!/usr/bin/env python3
import google.generativeai as genai
import json
import logging
from typing import Dict, Optional

class GeminiAIParser:
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.logger = logging.getLogger(__name__)
    
    def parse_note(self, text: str) -> Optional[Dict]:
        try:
            prompt = f"""
分析以下小红书笔记，提取地点信息，返回JSON格式：
{text}

返回格式：
{{
    "title": "标题",
    "places": [
        {{"name": "地点名", "description": "描述"}}
    ]
}}
"""
            response = self.model.generate_content(prompt)
            if response.text:
                data = json.loads(response.text)
                return data
        except Exception as e:
            self.logger.error(f"AI解析失败: {e}")
        return None
