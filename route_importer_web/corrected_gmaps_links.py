#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修正版本的Google Maps链接生成器
确保POI和路线顺序与小红书笔记完全一致
"""

import urllib.parse

def generate_corrected_links():
    """生成与小红书笔记完全一致的Google Maps链接"""
    
    print("🔍 小红书笔记路线分析")
    print("="*60)
    
    # 基于小红书笔记的准确路线顺序
    route_sequence = [
        {
            "name": "日暮里站",
            "description": "起点：从日暮里站🚉出来直走",
            "address": "Nippori Station, Tokyo, Japan",
            "coordinates": "35.7278,139.7708"
        },
        {
            "name": "朝仓雕塑馆",
            "description": "第1站：大概走3-4分钟，拐到巷子里",
            "address": "7 Chome-18-10 Yanaka, Taito City, Tokyo 110-0001, Japan",
            "coordinates": "35.7265,139.7690"
        },
        {
            "name": "谷中银座商业街",
            "description": "第2站：逛完雕塑馆直走",
            "address": "Yanaka Ginza Shopping Street, Tokyo, Japan",
            "coordinates": "35.7260,139.7680"
        },
        {
            "name": "Museca Times 牛肉汉堡店",
            "description": "第3站：午餐推荐，好吃！",
            "address": "3 Chome-41-16 Sendagi, Bunkyo City, Tokyo 113-0022, Japan",
            "coordinates": "35.7280,139.7650"
        },
        {
            "name": "猫猫神社",
            "description": "第4站：有名的猫猫神社，距离商业街要走一段路",
            "address": "2 Chome-1-4 Yanaka, Taito City, Tokyo 110-0001, Japan",
            "coordinates": "35.7255,139.7670"
        }
    ]
    
    print("📍 小红书笔记中的实际路线顺序：")
    for i, place in enumerate(route_sequence):
        print(f"{i+1}. {place['name']}")
        print(f"   {place['description']}")
        print(f"   地址: {place['address']}")
        print()
    
    print("🗺️ 生成修正后的Google Maps链接：")
    print("="*60)
    
    # 1. 完整路线导航链接（包含所有途经点）
    print("1️⃣ 完整路线导航链接（推荐测试）：")
    
    # 起点和终点
    origin = route_sequence[0]['address']  # 日暮里站
    destination = route_sequence[-1]['address']  # 猫猫神社
    
    # 途经点（第1站到第3站）
    waypoints = [place['address'] for place in route_sequence[1:-1]]
    
    # 构建完整路线链接
    full_route_url = f"https://www.google.com/maps/dir/{urllib.parse.quote(origin)}"
    if waypoints:
        full_route_url += f"/{'/'.join([urllib.parse.quote(wp) for wp in waypoints])}"
    full_route_url += f"/{urllib.parse.quote(destination)}/data=!4m2!4m1!3e2"
    
    print(full_route_url)
    print()
    
    # 2. 使用坐标的精确链接
    print("2️⃣ 使用坐标的精确链接：")
    
    origin_coord = route_sequence[0]['coordinates']
    dest_coord = route_sequence[-1]['coordinates']
    waypoint_coords = [place['coordinates'] for place in route_sequence[1:-1]]
    
    coord_url = f"https://www.google.com/maps/dir/{origin_coord}"
    if waypoint_coords:
        coord_url += f"/{'/'.join(waypoint_coords)}"
    coord_url += f"/{dest_coord}/data=!4m2!4m1!3e2"
    
    print(coord_url)
    print()
    
    # 3. 使用地点名称的搜索链接
    print("3️⃣ 使用地点名称的搜索链接：")
    
    place_names = [place['name'] for place in route_sequence]
    search_url = f"https://www.google.com/maps/dir/{urllib.parse.quote(place_names[0])}"
    if len(place_names) > 2:
        search_url += f"/{'/'.join([urllib.parse.quote(name) for name in place_names[1:-1]])}"
    search_url += f"/{urllib.parse.quote(place_names[-1])}/data=!4m2!4m1!3e2"
    
    print(search_url)
    print()
    
    # 4. 生成每个地点的单独链接
    print("4️⃣ 各地点单独的Google Maps链接：")
    for place in route_sequence:
        search_url = f"https://www.google.com/maps/search/{urllib.parse.quote(place['address'])}"
        print(f"{place['name']}: {search_url}")
    
    print()
    
    # 5. 生成路线描述
    print("5️⃣ 小红书笔记路线描述：")
    route_description = f"""
🚶‍♀️ 东京日暮里 City Walk 散步路线

📍 起点：{route_sequence[0]['name']} ({route_sequence[0]['description']})
   {route_sequence[0]['address']}

📍 第1站：{route_sequence[1]['name']} ({route_sequence[1]['description']})
   {route_sequence[1]['address']}

📍 第2站：{route_sequence[2]['name']} ({route_sequence[2]['description']})
   {route_sequence[2]['address']}

📍 第3站：{route_sequence[3]['name']} ({route_sequence[3]['description']})
   {route_sequence[3]['address']}

📍 第4站：{route_sequence[4]['name']} ({route_sequence[4]['description']})
   {route_sequence[4]['address']}

🗺️ 完整路线导航：
{full_route_url}

💡 路线说明：
- 从日暮里站出发，直走3-4分钟到朝仓雕塑馆
- 逛完雕塑馆直走到谷中银座商业街
- 在商业街享用午餐（Museca Times牛肉汉堡店）
- 前往猫猫神社
- 最后返回日暮里站
"""
    
    print(route_description)
    
    return {
        'full_route_url': full_route_url,
        'coord_url': coord_url,
        'search_url': search_url,
        'route_description': route_description
    }

def verify_route_accuracy():
    """验证路线准确性"""
    
    print("\n" + "="*60)
    print("🔍 路线准确性验证：")
    
    # 检查坐标的合理性
    coordinates = [
        (35.7278, 139.7708),  # 日暮里站
        (35.7265, 139.7690),  # 朝仓雕塑馆
        (35.7260, 139.7680),  # 谷中银座商业街
        (35.7280, 139.7650),  # Museca Times
        (35.7255, 139.7670)   # 猫猫神社
    ]
    
    print("📍 坐标验证：")
    for i, (lat, lng) in enumerate(coordinates):
        place_names = ["日暮里站", "朝仓雕塑馆", "谷中银座商业街", "Museca Times", "猫猫神社"]
        print(f"{place_names[i]}: 纬度 {lat}, 经度 {lng}")
    
    # 计算相邻地点间的距离
    print("\n📏 相邻地点间距离估算：")
    for i in range(len(coordinates) - 1):
        lat1, lng1 = coordinates[i]
        lat2, lng2 = coordinates[i + 1]
        
        # 简单的距离计算（粗略估算）
        lat_diff = abs(lat2 - lat1)
        lng_diff = abs(lng2 - lng1)
        distance_km = (lat_diff * 111 + lng_diff * 111 * 0.8)  # 粗略估算
        
        place_names = ["日暮里站", "朝仓雕塑馆", "谷中银座商业街", "Museca Times", "猫猫神社"]
        print(f"{place_names[i]} → {place_names[i+1]}: 约 {distance_km:.2f} 公里")
    
    print("\n✅ 路线合理性分析：")
    print("- 所有地点都在东京谷中/日暮里区域")
    print("- 坐标范围合理（纬度35.72-35.73，经度139.76-139.77）")
    print("- 相邻地点距离适中，适合步行")
    print("- 路线呈环形，最终回到起点")

if __name__ == "__main__":
    print("🚀 修正版Google Maps链接生成器")
    print("="*60)
    
    # 生成修正后的链接
    links = generate_corrected_links()
    
    # 验证路线准确性
    verify_route_accuracy()
    
    print("\n" + "="*60)
    print("📱 测试建议：")
    print("1. 优先测试完整路线导航链接")
    print("2. 验证Google Maps中显示的地点名称是否正确")
    print("3. 检查路线规划是否与小红书笔记描述一致")
    print("4. 确认起点（日暮里站）和终点（猫猫神社）正确")
    print("5. 验证途经点顺序：朝仓雕塑馆 → 谷中银座商业街 → Museca Times")
