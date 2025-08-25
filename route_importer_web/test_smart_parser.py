#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试智能解析器的完整流程
"""

import os
import sys
import json

def test_smart_parser():
    """测试智能解析器"""
    try:
        # 设置环境变量
        os.environ['VOLCENGINE_API_KEY'] = 'daf37bb4-0e7b-42f8-87bb-b780842dd0d8'
        
        # 导入智能解析器
        from smart_parser_final import SmartParser
        
        print("🚀 测试智能解析器")
        print("=" * 50)
        
        # 创建智能解析器实例
        smart_parser = SmartParser()
        
        # 获取解析器信息
        parser_info = smart_parser.get_parser_info()
        print("📊 解析器信息:")
        print(json.dumps(parser_info, ensure_ascii=False, indent=2))
        print()
        
        # 测试URL
        test_url = "http://xhslink.com/m/3ehl5ukd72F"
        print(f"🔗 测试URL: {test_url}")
        print()
        
        # 测试解析
        print("🔍 开始解析...")
        result = smart_parser.parse_note("", test_url)
        
        if result:
            print("✅ 解析成功!")
            print(f"📍 提取到 {len(result.get('places', []))} 个POI")
            print()
            print("📋 解析结果:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("❌ 解析失败")
            
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保所有依赖文件存在")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_smart_parser()
