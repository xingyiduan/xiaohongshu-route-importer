#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Gemini API的脚本
"""

import google.generativeai as genai
import json

def test_gemini_api(api_key: str):
    """测试Gemini API"""
    try:
        # 配置API
        genai.configure(api_key=api_key)
        
        # 创建模型
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 测试文本
        test_text = """
小红书笔记：东京｜日暮里 City Walk 散步路线
从日暮里站🚉出来直走
1️⃣ p2–p3 大概走3-4分钟 拐到巷子里有一个朝仓雕塑馆
2️⃣ 逛完雕塑馆直走到谷中银座商业街
3️⃣ 🍔 午餐推荐：p12 是一家叫 Museca Times 的牛肉汉堡店 好吃！
4️⃣ ⛩️ 猫猫神社
5️⃣ 从神社一路走回日暮里站
"""
        
        # 构建提示词
        prompt = f"""
你是一个专业的旅游路线分析助手。请分析以下小红书笔记，提取其中的地点信息（POI）。

**任务要求：**
1. 识别笔记中提到的所有具体地点（如车站、景点、餐厅、商店等）
2. 过滤掉描述性文字、人物、情感表达等非地点内容
3. 返回结构化的JSON数据

**输入文本：**
{test_text}

**输出格式要求：**
请返回一个JSON对象，包含以下字段：
{{
    "title": "笔记标题",
    "content": "笔记主要内容摘要",
    "places": [
        {{
            "name": "地点名称",
            "description": "地点描述",
            "category": "地点类别",
            "address": "地址信息（如果有）"
        }}
    ],
    "tags": ["标签1", "标签2"],
    "route_type": "路线类型（如：步行、观光等）"
}}

**注意事项：**
- 只提取真实存在的地点，不要包含虚拟或描述性内容
- 地点名称要准确，不要包含多余的修饰词
- 如果文本中没有明确的地点信息，返回空的地点列表
- 确保返回的是有效的JSON格式

请直接返回JSON，不要包含其他文字说明。
"""
        
        print("正在调用Gemini API...")
        
        # 调用API
        response = model.generate_content(prompt)
        
        if response.text:
            print("✅ API调用成功！")
            print("原始响应:")
            print(response.text)
            
            # 尝试解析JSON
            try:
                json_start = response.text.find('{')
                json_end = response.text.rfind('}') + 1
                
                if json_start != -1 and json_end != 0:
                    json_text = response.text[json_start:json_end]
                    parsed_data = json.loads(json_text)
                    
                    print("\n✅ JSON解析成功！")
                    print("解析结果:")
                    print(json.dumps(parsed_data, ensure_ascii=False, indent=2))
                    
                    # 统计POI数量
                    places_count = len(parsed_data.get('places', []))
                    print(f"\n📍 提取到 {places_count} 个POI")
                    
                else:
                    print("❌ 响应中未找到JSON内容")
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失败: {e}")
                
        else:
            print("❌ API未返回内容")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    print("🚀 Gemini API 测试脚本")
    print("=" * 50)
    
    # 请在这里输入你的Gemini API密钥
    api_key = input("请输入你的Gemini API密钥: ").strip()
    
    if api_key:
        test_gemini_api(api_key)
    else:
        print("❌ 未输入API密钥")
