#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试AI多路线解析功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from volcengine_douban_final import VolcengineDoubanParser

def test_ai_multiroute():
    """测试AI多路线解析"""
    
    parser = VolcengineDoubanParser()
    
    # 测试文本（模拟香港city walk笔记）
    test_text = """
小红书

熬夜总结的香港小众city walk路线

这个是我来过四五次香港后，总结出的精华 既不会太累，又可以把景点都看到 也可以边走边逛边吃 

Day1:深水埗➡️旺角➡️油麻地➡️尖沙咀➡️维多利亚港➡️星光大道➡️坐天星小伦看维港的夜景 （主要是九龙半岛玩 觉得累可以🚇或者公交🚌 很方便） 

Day2:铜锣湾➡️湾仔➡️西营盘➡️坚尼地城➡️太平山（看日落和山上夜景） 以港岛为主 可以特种兵的玩👉每个地方都去把想打卡的都打卡 也可以悠闲一点👉大致走一遍景点 重点去2-3个打卡 

day1和day2可以更换一下顺序 然后临走前可以去买一点手信（比如蝴蝶酥、曲奇饼干🍪、冰箱贴这些东西，小巧精致很适合送给家人朋友） 

小tips：有的酒店是没有转换插头🔌 保险一点自己准备 要带💰 提前注册八达通也会更方便

#香港 #香港旅游 #香港生活 #香港美食 #香港旅游攻略 #手信 #香港手信 #蝴蝶酥
"""
    
    print("🧪 测试AI多路线解析功能")
    print("=" * 50)
    print("测试文本:")
    print(test_text[:200] + "..." if len(test_text) > 200 else test_text)
    print("=" * 50)
    
    try:
        result = parser.parse_note(test_text, "test_url")
        
        if result:
            print("✅ AI解析成功！")
            print(f"标题: {result.get('title', 'N/A')}")
            print(f"内容: {result.get('content', 'N/A')[:100]}...")
            print()
            
            # 检查多路线结构
            if 'routes' in result and result['routes']:
                print(f"🗺️ 识别到 {len(result['routes'])} 条路线:")
                print()
                
                for i, route in enumerate(result['routes'], 1):
                    print(f"路线 {i}: {route.get('route_name', 'N/A')}")
                    print(f"  ID: {route.get('route_id', 'N/A')}")
                    print(f"  描述: {route.get('route_description', 'N/A')}")
                    print(f"  地点数量: {len(route.get('places', []))}")
                    
                    # 显示地点
                    places = route.get('places', [])
                    for j, place in enumerate(places[:5], 1):  # 只显示前5个
                        print(f"    {j}. {place.get('name', 'N/A')} ({place.get('category', 'N/A')})")
                    
                    if len(places) > 5:
                        print(f"    ... 还有 {len(places) - 5} 个地点")
                    print()
            else:
                print("⚠️  未识别到多路线结构")
                if 'places' in result:
                    print(f"  单路线地点数量: {len(result['places'])}")
            
            # 显示标签
            tags = result.get('tags', [])
            if tags:
                print(f"🏷️  标签: {', '.join(tags)}")
            
            print()
            print("📊 数据结构:")
            import json
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
        else:
            print("❌ AI解析失败，返回None")
            
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_ai_multiroute()
