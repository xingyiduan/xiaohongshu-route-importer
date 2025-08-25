#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的豆包API测试脚本
"""

import requests
import json

def test_douban_api_simple():
    """简单测试豆包API"""
    
    # API配置
    api_key = "daf37bb4-0e7b-42f8-87bb-b780842dd0d8"
    api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    
    # 请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 请求数据
    request_data = {
        "model": "doubao-seed-1.6",
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
    
    print("🚀 豆包API简单测试")
    print("=" * 40)
    print(f"API地址: {api_url}")
    print(f"模型: doubao-seed-1.6")
    print(f"API密钥: {api_key[:10]}...")
    print()
    
    try:
        print("正在发送请求...")
        
        # 发送请求
        response = requests.post(
            api_url,
            headers=headers,
            json=request_data,
            timeout=30
        )
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print()
        
        if response.status_code == 200:
            print("✅ API调用成功！")
            print("响应内容:")
            print(response.text)
            
            # 尝试解析JSON
            try:
                result = response.json()
                print("\n解析后的JSON:")
                print(json.dumps(result, ensure_ascii=False, indent=2))
            except Exception as e:
                print(f"JSON解析失败: {e}")
                
        else:
            print(f"❌ API调用失败，状态码: {response.status_code}")
            print("错误响应:")
            print(response.text)
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

if __name__ == "__main__":
    test_douban_api_simple()
