#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试多路线功能
"""

import requests
import json

def test_multiroute_parsing():
    """测试多路线解析功能"""
    
    # 测试URL（香港city walk笔记）
    test_url = "http://xhslink.com/m/6hZA3tQik5g"
    
    print("🚀 测试多路线解析功能")
    print("=" * 50)
    print(f"测试URL: {test_url}")
    print()
    
    try:
        # 发送解析请求
        response = requests.post(
            'http://localhost:8081/api/parse-note',
            json={'url': test_url},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if result['success']:
                data = result['data']
                print("✅ 解析成功！")
                print(f"标题: {data.get('title', 'N/A')}")
                print(f"内容: {data.get('content', 'N/A')[:100]}...")
                print()
                
                # 检查多路线结构
                if 'routes' in data and data['routes']:
                    print(f"🗺️ 识别到 {len(data['routes'])} 条路线:")
                    print()
                    
                    for i, route in enumerate(data['routes'], 1):
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
                    if 'places' in data:
                        print(f"  单路线地点数量: {len(data['places'])}")
                
                # 显示标签
                tags = data.get('tags', [])
                if tags:
                    print(f"🏷️  标签: {', '.join(tags)}")
                
                print()
                print("📊 数据结构:")
                print(json.dumps(data, ensure_ascii=False, indent=2))
                
            else:
                print(f"❌ 解析失败: {result.get('error', '未知错误')}")
                
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败，请确保服务正在运行")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

if __name__ == '__main__':
    test_multiroute_parsing()
