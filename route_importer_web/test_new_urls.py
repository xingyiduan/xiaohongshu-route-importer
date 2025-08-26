#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新的小红书链接
"""

import requests
import json

def test_new_urls():
    """测试新的小红书链接"""
    
    test_urls = [
        "http://xhslink.com/m/3pbHffdSTtI",  # 日本东京city walk旅游线路
        "http://xhslink.com/m/1MdJtuYJKcN"   # 东京自由之丘的慢生活
    ]
    
    for i, url in enumerate(test_urls, 1):
        print(f"🔗 测试URL {i}: {url}")
        print("-" * 50)
        
        try:
            response = requests.post(
                'http://localhost:8081/api/parse-note',
                json={'url': url},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result['success']:
                    print("✅ 解析成功")
                    data = result['data']
                    print(f"   标题: {data.get('title', 'N/A')}")
                    
                    # 检查多路线结构
                    if 'routes' in data and data['routes']:
                        print(f"   🗺️ 路线数量: {len(data['routes'])}")
                        for j, route in enumerate(data['routes'], 1):
                            print(f"     路线{j}: {route.get('route_name', 'N/A')} ({len(route.get('places', []))}个地点)")
                    elif 'places' in data:
                        print(f"   📍 地点数量: {len(data['places'])}")
                    
                    # 显示标签
                    tags = data.get('tags', [])
                    if tags:
                        print(f"   🏷️  标签: {', '.join(tags[:5])}{'...' if len(tags) > 5 else ''}")
                        
                else:
                    print(f"❌ 解析失败: {result.get('error', 'N/A')}")
            else:
                print(f"❌ HTTP错误 {response.status_code}")
                print(f"   响应: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求异常: {str(e)}")
        
        print()

if __name__ == '__main__':
    test_new_urls()
