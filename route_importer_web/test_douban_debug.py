#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆包API调试测试脚本
"""

import requests
import json

def test_douban_api_debug():
    """调试测试豆包API"""
    
    # API配置
    api_key = "daf37bb4-0e7b-42f8-87bb-b780842dd0d8"
    
    # 尝试不同的API端点
    api_endpoints = [
        "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
        "https://api.volcengine.com/v1/services/aigc/text-generation/generation",
        "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    ]
    
    # 尝试不同的模型名称
    models = [
        "doubao-seed-1.6",
        "doubao-seed-1.6",
        "doubao-seed-1.6"
    ]
    
    # 请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("🚀 豆包API调试测试")
    print("=" * 50)
    print(f"API密钥: {api_key}")
    print()
    
    for i, (endpoint, model) in enumerate(zip(api_endpoints, models)):
        print(f"测试 {i+1}: {endpoint}")
        print(f"模型: {model}")
        print("-" * 40)
        
        # 请求数据
        request_data = {
            "model": model,
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": "请简单回复'测试成功'"
                    }
                ]
            },
            "parameters": {
                "temperature": 0.1,
                "max_tokens": 100
            }
        }
        
        try:
            print("发送请求...")
            response = requests.post(
                endpoint,
                headers=headers,
                json=request_data,
                timeout=30
            )
            
            print(f"状态码: {response.status_code}")
            print(f"响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                print("✅ 成功！")
                print("响应内容:")
                print(response.text[:200] + "..." if len(response.text) > 200 else response.text)
            else:
                print(f"❌ 失败: {response.status_code}")
                print("错误响应:")
                print(response.text[:200] + "..." if len(response.text) > 200 else response.text)
                
        except Exception as e:
            print(f"❌ 异常: {e}")
        
        print()
        print("=" * 50)
        print()

if __name__ == "__main__":
    test_douban_api_debug()
