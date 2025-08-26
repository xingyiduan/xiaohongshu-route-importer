#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试note_parser
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from note_parser import XiaohongshuNoteParser

def test_note_parser():
    """测试note_parser"""
    
    parser = XiaohongshuNoteParser()
    
    # 测试URL
    test_url = "https://www.xiaohongshu.com/discovery/item/68ac60e5000000001b035a0b"
    
    print(f"🔗 测试URL: {test_url}")
    print("=" * 50)
    
    try:
        result = parser.parse_note(test_url)
        
        if result:
            print("✅ 解析成功")
            print(f"标题: {result.get('title', 'N/A')}")
            print(f"内容长度: {len(result.get('content', ''))}")
            print(f"地点数量: {len(result.get('places', []))}")
            print(f"标签数量: {len(result.get('tags', []))}")
            
            # 显示地点
            places = result.get('places', [])
            for i, place in enumerate(places[:5], 1):
                print(f"  {i}. {place.get('name', 'N/A')}")
            
            if len(places) > 5:
                print(f"  ... 还有 {len(places) - 5} 个地点")
                
        else:
            print("❌ 解析失败，返回None")
            
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_note_parser()
