#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门测试豆包API的脚本
禁用规则解析器回退，专注豆包API性能
"""

import os
import json
import time

def test_douban_api_only():
    """只测试豆包API，不测试规则解析器"""
    try:
        # 设置环境变量
        os.environ['VOLCENGINE_API_KEY'] = 'daf37bb4-0e7b-42f8-87bb-b780842dd0d8'
        
        print("🚀 豆包API专项测试")
        print("=" * 50)
        print("配置: 禁用规则解析器回退，专注豆包API性能")
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
        
        # 测试解析 - 只使用豆包API
        print("🔍 开始豆包API解析测试...")
        print("⏰ 超时时间: 120秒，重试次数: 3次")
        print("🔄 重试间隔: 10秒、20秒、30秒")
        print()
        
        start_time = time.time()
        result = smart_parser.parse_note("", test_url)
        end_time = time.time()
        
        total_time = end_time - start_time
        print(f"⏱️  总耗时: {total_time:.2f} 秒")
        print()
        
        if result:
            print("✅ 豆包API解析成功!")
            print(f"📍 提取到 {len(result.get('places', []))} 个POI")
            print()
            print("📋 解析结果:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("❌ 豆包API解析失败")
            print("💡 建议:")
            print("   - 检查网络连接")
            print("   - 确认API密钥有效")
            print("   - 考虑增加超时时间")
            
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保所有依赖文件存在")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_douban_api_only()
