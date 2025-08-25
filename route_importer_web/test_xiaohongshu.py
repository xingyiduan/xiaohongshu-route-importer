#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试小红书链接解析
"""

import requests
from bs4 import BeautifulSoup
import json
import time

def test_xiaohongshu_link():
    """测试小红书链接"""
    url = "http://xhslink.com/m/3ehl5ukd72F"
    
    print(f"正在测试链接: {url}")
    
    # 设置请求头，模拟真实浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        print("1. 发送请求...")
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        
        print(f"2. 响应状态码: {response.status_code}")
        print(f"3. 最终URL: {response.url}")
        print(f"4. 响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("5. 获取内容成功，开始解析...")
            
            # 保存原始HTML用于调试
            with open('debug_response.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("6. 已保存原始HTML到 debug_response.html")
            
            # 尝试解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找可能的标题
            title = soup.find('title')
            if title:
                print(f"7. 页面标题: {title.get_text().strip()}")
            
            # 查找可能的正文内容
            content_elements = soup.find_all(['p', 'div', 'span'], class_=lambda x: x and ('content' in x.lower() or 'text' in x.lower() or 'desc' in x.lower()))
            
            print(f"8. 找到 {len(content_elements)} 个可能的内容元素")
            
            # 查找可能的图片
            images = soup.find_all('img')
            print(f"9. 找到 {len(images)} 张图片")
            
            # 查找可能的链接
            links = soup.find_all('a')
            print(f"10. 找到 {len(links)} 个链接")
            
            # 尝试查找地点相关信息
            place_keywords = ['地点', '地址', '位置', '坐标', '经纬度', 'latitude', 'longitude']
            place_info = []
            
            for keyword in place_keywords:
                elements = soup.find_all(text=lambda text: text and keyword in text)
                if elements:
                    place_info.extend(elements)
            
            if place_info:
                print(f"11. 找到地点相关信息: {place_info[:5]}")  # 只显示前5个
            
            # 查找所有文本内容，尝试识别地点
            all_text = soup.get_text()
            print(f"12. 页面总文本长度: {len(all_text)} 字符")
            
            # 保存提取的文本
            with open('extracted_text.txt', 'w', encoding='utf-8') as f:
                f.write(all_text)
            print("13. 已保存提取的文本到 extracted_text.txt")
            
            # 尝试查找JSON数据
            scripts = soup.find_all('script')
            json_data = []
            
            for script in scripts:
                if script.string:
                    try:
                        # 尝试解析JSON
                        data = json.loads(script.string)
                        json_data.append(data)
                    except:
                        # 尝试查找包含特定关键词的JSON片段
                        if 'location' in script.string or 'place' in script.string or '坐标' in script.string:
                            print(f"14. 找到可能包含位置信息的脚本: {script.string[:200]}...")
            print(f"15. 找到 {len(json_data)} 个JSON数据块")
            
        else:
            print(f"请求失败，状态码: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
    except Exception as e:
        print(f"其他异常: {e}")

def test_with_different_headers():
    """使用不同的请求头测试"""
    url = "http://xhslink.com/m/3ehl5ukd72F"
    
    headers_list = [
        # 移动端Chrome
        {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36'
        },
        # 移动端Safari
        {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1'
        },
        # 桌面端Chrome
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    ]
    
    for i, headers in enumerate(headers_list):
        print(f"\n=== 测试请求头 {i+1} ===")
        try:
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            print(f"状态码: {response.status_code}")
            print(f"最终URL: {response.url}")
            print(f"内容长度: {len(response.text)}")
            
            # 检查是否被重定向到登录页面
            if 'login' in response.url.lower() or 'signin' in response.url.lower():
                print("⚠️  被重定向到登录页面")
            elif 'block' in response.text.lower() or 'forbidden' in response.text.lower():
                print("⚠️  可能被阻止访问")
            else:
                print("✅ 看起来可以正常访问")
                
        except Exception as e:
            print(f"请求失败: {e}")
        
        time.sleep(2)  # 避免请求过快

if __name__ == "__main__":
    print("开始测试小红书链接解析...")
    print("=" * 50)
    
    test_xiaohongshu_link()
    
    print("\n" + "=" * 50)
    print("测试不同请求头...")
    test_with_different_headers()
    
    print("\n测试完成！")
