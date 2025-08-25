#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试豆包大模型API的脚本
"""

import json
import os

def test_douban_api(api_key: str):
    """测试豆包API"""
    try:
        # 导入豆包解析器
        from douban_parser import DoubanAIParser
        
        # 创建解析器实例
        parser = DoubanAIParser(api_key)
        
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
        
        print("🚀 豆包大模型API测试脚本")
        print("=" * 50)
        print(f"使用模型: Doubao-Seed-1.6")
        print(f"API密钥: {api_key[:10]}...")
        print()
        
        # 检查API可用性
        if not parser.is_available():
            print("❌ 豆包API不可用")
            return
        
        # 检查调用限制
        if not parser.can_make_call():
            print("❌ 已达到API调用限制")
            usage = parser.get_usage_stats()
            print(f"今日已调用: {usage['today_calls']}/{usage['max_daily_calls']}")
            return
        
        print("✅ API检查通过，开始解析...")
        print()
        
        # 调用API解析
        result = parser.parse_note(test_text)
        
        if result:
            print("✅ 豆包API解析成功！")
            print()
            print("解析结果:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
            # 统计POI数量
            places_count = len(result.get('places', []))
            print(f"\n📍 提取到 {places_count} 个POI")
            
            # 显示使用统计
            usage = parser.get_usage_stats()
            print(f"\n📊 API使用统计:")
            print(f"   今日已调用: {usage['today_calls']}/{usage['max_daily_calls']}")
            print(f"   剩余调用次数: {usage['remaining_daily']}")
            
        else:
            print("❌ 豆包API解析失败")
            
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保已安装 dashscope 包")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    print("🚀 豆包大模型API测试脚本")
    print("=" * 50)
    
    # 从环境变量获取API密钥
    api_key = os.environ.get('DOUBAN_API_KEY')
    
    if not api_key:
        # 手动输入API密钥
        api_key = input("请输入你的豆包API密钥: ").strip()
    
    if api_key:
        test_douban_api(api_key)
    else:
        print("❌ 未输入API密钥")
        print("请设置环境变量 DOUBAN_API_KEY 或手动输入")
