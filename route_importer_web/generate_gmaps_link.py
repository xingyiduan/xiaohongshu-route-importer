#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成Google Maps导航链接
"""

import urllib.parse

def generate_google_maps_link():
    """基于提取的POI信息生成Google Maps导航链接"""
    
    # 从小红书笔记中提取的地点信息
    places = [
        {
            "name": "日暮里站",
            "address": "Nippori Station, Tokyo, Japan",
            "coordinates": "35.7278,139.7708"  # 日暮里站的大致坐标
        },
        {
            "name": "朝仓雕塑馆",
            "address": "7 Chome-18-10 Yanaka, Taito City, Tokyo 110-0001, Japan",
            "coordinates": "35.7265,139.7690"
        },
        {
            "name": "谷中银座商业街",
            "address": "Yanaka Ginza Shopping Street, Tokyo, Japan",
            "coordinates": "35.7260,139.7680"
        },
        {
            "name": "Museca Times 牛肉汉堡店",
            "address": "3 Chome-41-16 Sendagi, Bunkyo City, Tokyo 113-0022, Japan",
            "coordinates": "35.7280,139.7650"
        },
        {
            "name": "猫猫神社",
            "address": "2 Chome-1-4 Yanaka, Taito City, Tokyo 110-0001, Japan",
            "coordinates": "35.7255,139.7670"
        }
    ]
    
    print("📍 提取的地点信息：")
    for i, place in enumerate(places, 1):
        print(f"{i}. {place['name']}")
        print(f"   地址: {place['address']}")
        print(f"   坐标: {place['coordinates']}")
        print()
    
    # 生成Google Maps导航链接
    # 起点：日暮里站
    origin = places[0]['coordinates']
    
    # 终点：猫猫神社
    destination = places[-1]['coordinates']
    
    # 途经点：中间的地点
    waypoints = "|".join([place['coordinates'] for place in places[1:-1]])
    
    # 构建Google Maps导航链接
    base_url = "https://www.google.com/maps/dir/"
    params = {
        'api': '1',
        'origin': origin,
        'destination': destination,
        'waypoints': waypoints,
        'travelmode': 'walking'  # 步行模式
    }
    
    # 构建查询字符串
    query_string = urllib.parse.urlencode(params)
    full_url = base_url + "?" + query_string
    
    print("🗺️ 生成的Google Maps导航链接：")
    print(full_url)
    print()
    
    # 生成简化版本的链接（只包含起点和终点）
    simple_params = {
        'api': '1',
        'origin': origin,
        'destination': destination,
        'travelmode': 'walking'
    }
    simple_query = urllib.parse.urlencode(simple_params)
    simple_url = base_url + "?" + simple_query
    
    print("🗺️ 简化版Google Maps导航链接（仅起点和终点）：")
    print(simple_url)
    print()
    
    # 生成每个地点的单独链接
    print("📍 各地点单独的Google Maps链接：")
    for place in places:
        place_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(place['address'])}"
        print(f"{place['name']}: {place_url}")
    
    return full_url, simple_url

def generate_alternative_links():
    """生成其他格式的Google Maps链接"""
    
    print("\n" + "="*60)
    print("🔄 其他格式的Google Maps链接：")
    
    # 1. 使用地址而不是坐标的链接
    places_addresses = [
        "Nippori Station, Tokyo, Japan",
        "7 Chome-18-10 Yanaka, Taito City, Tokyo 110-0001, Japan",
        "Yanaka Ginza Shopping Street, Tokyo, Japan", 
        "3 Chome-41-16 Sendagi, Bunkyo City, Tokyo 113-0022, Japan",
        "2 Chome-1-4 Yanaka, Taito City, Tokyo 110-0001, Japan"
    ]
    
    # 起点到终点的导航链接
    origin_addr = urllib.parse.quote(places_addresses[0])
    dest_addr = urllib.parse.quote(places_addresses[-1])
    
    address_based_url = f"https://www.google.com/maps/dir/{origin_addr}/{dest_addr}/data=!4m2!4m1!3e2"
    
    print("📍 基于地址的导航链接：")
    print(address_based_url)
    print()
    
    # 2. 生成搜索链接（用户可以在Google Maps中搜索）
    print("🔍 搜索链接（用户可以在Google Maps中搜索地点）：")
    for i, address in enumerate(places_addresses):
        search_url = f"https://www.google.com/maps/search/{urllib.parse.quote(address)}"
        place_names = ["日暮里站", "朝仓雕塑馆", "谷中银座商业街", "Museca Times", "猫猫神社"]
        print(f"{place_names[i]}: {search_url}")
    
    return address_based_url

if __name__ == "__main__":
    print("🚀 生成Google Maps导航链接")
    print("="*60)
    
    # 生成主要链接
    full_url, simple_url = generate_google_maps_link()
    
    # 生成替代链接
    alt_url = generate_alternative_links()
    
    print("\n" + "="*60)
    print("📱 测试建议：")
    print("1. 在手机浏览器中打开上述链接")
    print("2. 检查是否能正确跳转到Google Maps应用")
    print("3. 验证路线规划是否准确")
    print("4. 测试步行导航功能")
    print("\n💡 如果链接无法正常工作，可能需要：")
    print("- 确保手机已安装Google Maps应用")
    print("- 检查网络连接")
    print("- 尝试使用坐标版本的链接")
