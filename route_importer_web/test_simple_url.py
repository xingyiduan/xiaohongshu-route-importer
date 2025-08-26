#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试不同URL格式的解析
"""

import requests
import json

def test_url_formats():
    """测试不同URL格式"""
    
    test_urls = [
        "https://www.xiaohongshu.com/discovery/item/68ac60e5000000001b035a0b",
        "http://xhslink.com/m/6hZA3tQik5g",
        "https://xhslink.com/m/6hZA3tQik5g"
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
                    if 'routes' in data:
                        print(f"   路线数量: {len(data['routes'])}")
                    if 'places' in data:
                        print(f"   地点数量: {len(data['places'])}")
                else:
                    print(f"❌ 解析失败: {result.get('error', 'N/A')}")
            else:
                print(f"❌ HTTP错误 {response.status_code}")
                print(f"   响应: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求异常: {str(e)}")
        
        print()

if __name__ == '__main__':
    test_url_formats()
