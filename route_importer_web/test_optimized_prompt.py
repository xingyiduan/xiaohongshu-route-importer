#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试优化后的豆包API Prompt
验证是否能正确过滤描述性内容
"""

import os
import json
import time

def test_optimized_prompt():
    """测试优化后的Prompt"""
    try:
        # 设置环境变量
        os.environ['VOLCENGINE_API_KEY'] = 'daf37bb4-0e7b-42f8-87bb-b780842dd0d8'
        
        print("🚀 测试优化后的豆包API Prompt")
        print("=" * 60)
        print("目标: 只提取明确的地点名称，过滤描述性内容")
        print()
        
        # 导入智能解析器
        from smart_parser_final import SmartParser
        
        # 创建智能解析器实例
        smart_parser = SmartParser()
        
        # 获取解析器信息
        parser_info = smart_parser.get_parser_info()
        print("📊 解析器配置:")
        print(json.dumps(parser_info, ensure_ascii=False, indent=2))
        print()
        
        # 测试URL
        test_url = "http://xhslink.com/m/3ehl5ukd72F"
        print(f"🔗 测试URL: {test_url}")
        print()
        
        # 测试解析
        print("🔍 开始测试优化后的Prompt...")
        print("⏰ 超时时间: 120秒")
        print("🎯 期望结果: 只提取5个明确的地点")
        print("   - 日暮里站")
        print("   - 朝仓雕塑馆") 
        print("   - 谷中银座商业街")
        print("   - Museca Times")
        print("   - 猫猫神社")
        print()
        
        start_time = time.time()
        result = smart_parser.parse_note("", test_url)
        end_time = time.time()
        
        total_time = end_time - start_time
        print(f"⏱️  总耗时: {total_time:.2f} 秒")
        print()
        
        if result:
            print("✅ 豆包API解析成功!")
            places = result.get('places', [])
            print(f"📍 提取到 {len(places)} 个POI")
            print()
            
            # 分析提取的地点
            print("📋 提取的地点分析:")
            for i, place in enumerate(places, 1):
                name = place.get('name', '')
                category = place.get('category', '')
                description = place.get('description', '')
                
                # 判断是否是明确的地点
                is_explicit = (
                    '站' in name or 
                    '馆' in name or 
                    '神社' in name or
                    'Museca Times' in name or
                    '谷中银座' in name
                )
                
                status = "✅ 明确地点" if is_explicit else "❌ 描述性内容"
                print(f"  {i}. {name}")
                print(f"     类别: {category}")
                print(f"     描述: {description[:50]}...")
                print(f"     状态: {status}")
                print()
            
            # 统计结果
            explicit_places = sum(1 for place in places if (
                '站' in place.get('name', '') or 
                '馆' in place.get('name', '') or 
                '神社' in place.get('name', '') or
                'Museca Times' in place.get('name', '') or
                '谷中银座' in place.get('name', '')
            ))
            
            print(f"📊 结果统计:")
            print(f"   总POI数量: {len(places)}")
            print(f"   明确地点: {explicit_places}")
            print(f"   描述性内容: {len(places) - explicit_places}")
            print()
            
            if explicit_places == 5 and len(places) == 5:
                print("🎉 完美！所有提取的都是明确的地点")
            elif explicit_places == 5:
                print("✅ 明确地点数量正确，但仍有描述性内容")
            else:
                print("⚠️  需要进一步优化Prompt")
                
        else:
            print("❌ 豆包API解析失败")
            
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保所有依赖文件存在")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_optimized_prompt()
