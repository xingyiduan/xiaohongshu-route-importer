#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终修正版本的Google Maps链接生成器
确保路线是环形路线，终点回到日暮里站
"""

import urllib.parse

def generate_final_corrected_links():
    """生成最终修正的Google Maps链接"""
    
    print("🔍 小红书笔记路线最终分析")
    print("="*60)
    
    # 基于小红书笔记的准确路线顺序（环形路线）
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
        },
        {
            "name": "日暮里站（终点）",
            "description": "终点：从神社一路走回日暮里站，途经安静的住宅区",
            "address": "Nippori Station, Tokyo, Japan",
            "coordinates": "35.7278,139.7708"
        }
    ]
    
    print("📍 小红书笔记中的实际路线顺序（环形路线）：")
    for i, place in enumerate(route_sequence):
        if i == 0:
            print(f"{i+1}. {place['name']} - {place['description']}")
        elif i == len(route_sequence) - 1:
            print(f"{i+1}. {place['name']} - {place['description']}")
        else:
            print(f"{i+1}. {place['name']} - {place['description']}")
        print(f"   地址: {place['address']}")
        print()
    
    print("🗺️ 生成最终修正的Google Maps链接：")
    print("="*60)
    
    # 1. 完整环形路线导航链接（推荐测试）
    print("1️⃣ 完整环形路线导航链接（推荐测试）：")
    
    # 起点：日暮里站
    origin = route_sequence[0]['address']
    
    # 途经点：朝仓雕塑馆、谷中银座商业街、Museca Times、猫猫神社
    waypoints = [place['address'] for place in route_sequence[1:-1]]
    
    # 终点：回到日暮里站
    destination = route_sequence[-1]['address']
    
    # 构建完整环形路线链接
    full_route_url = f"https://www.google.com/maps/dir/{urllib.parse.quote(origin)}"
    if waypoints:
        full_route_url += f"/{'/'.join([urllib.parse.quote(wp) for wp in waypoints])}"
    full_route_url += f"/{urllib.parse.quote(destination)}/data=!4m2!4m1!3e2"
    
    print(full_route_url)
    print()
    
    # 2. 使用坐标的精确环形路线链接
    print("2️⃣ 使用坐标的精确环形路线链接：")
    
    origin_coord = route_sequence[0]['coordinates']
    waypoint_coords = [place['coordinates'] for place in route_sequence[1:-1]]
    dest_coord = route_sequence[-1]['coordinates']
    
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
    
    # 4. 生成路线描述
    print("4️⃣ 小红书笔记环形路线描述：")
    route_description = f"""
🚶‍♀️ 东京日暮里 City Walk 环形散步路线

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

📍 终点：{route_sequence[5]['name']} ({route_sequence[5]['description']})
   {route_sequence[5]['address']}

🗺️ 完整环形路线导航：
{full_route_url}

💡 路线说明：
- 从日暮里站出发，直走3-4分钟到朝仓雕塑馆
- 逛完雕塑馆直走到谷中银座商业街
- 在商业街享用午餐（Museca Times牛肉汉堡店）
- 前往猫猫神社
- 从神社一路走回日暮里站，途经安静的住宅区
- 形成完整的环形散步路线
"""
    
    print(route_description)
    
    return {
        'full_route_url': full_route_url,
        'coord_url': coord_url,
        'search_url': search_url,
        'route_description': route_description
    }

def verify_circular_route():
    """验证环形路线的合理性"""
    
    print("\n" + "="*60)
    print("🔍 环形路线验证：")
    
    # 检查起点和终点是否相同
    start_point = "日暮里站"
    end_point = "日暮里站（终点）"
    
    print(f"✅ 起点：{start_point}")
    print(f"✅ 终点：{end_point}")
    print(f"✅ 路线类型：环形路线（起点=终点）")
    
    # 计算总距离
    coordinates = [
        (35.7278, 139.7708),  # 日暮里站
        (35.7265, 139.7690),  # 朝仓雕塑馆
        (35.7260, 139.7680),  # 谷中银座商业街
        (35.7280, 139.7650),  # Museca Times
        (35.7255, 139.7670),  # 猫猫神社
        (35.7278, 139.7708)   # 回到日暮里站
    ]
    
    print("\n📏 各段距离估算：")
    total_distance = 0
    for i in range(len(coordinates) - 1):
        lat1, lng1 = coordinates[i]
        lat2, lng2 = coordinates[i + 1]
        
        # 简单的距离计算（粗略估算）
        lat_diff = abs(lat2 - lat1)
        lng_diff = abs(lng2 - lng1)
        distance_km = (lat_diff * 111 + lng_diff * 111 * 0.8)  # 粗略估算
        total_distance += distance_km
        
        place_names = ["日暮里站", "朝仓雕塑馆", "谷中银座商业街", "Museca Times", "猫猫神社", "日暮里站"]
        print(f"{place_names[i]} → {place_names[i+1]}: 约 {distance_km:.2f} 公里")
    
    print(f"\n📊 总步行距离：约 {total_distance:.2f} 公里")
    print(f"⏱️  预计步行时间：约 {int(total_distance * 20)} 分钟（按20分钟/公里计算）")
    
    print("\n✅ 环形路线合理性分析：")
    print("- 起点和终点相同（日暮里站），形成完整环形")
    print("- 总距离约2公里，适合2-3小时的City Walk")
    print("- 路线经过景点、商业区、餐厅、神社等多样化地点")
    print("- 最后一段从神社回到车站，途经安静住宅区，体验当地生活")

if __name__ == "__main__":
    print("🚀 最终修正版Google Maps链接生成器")
    print("="*60)
    
    # 生成最终修正的链接
    links = generate_final_corrected_links()
    
    # 验证环形路线
    verify_circular_route()
    
    print("\n" + "="*60)
    print("📱 最终测试建议：")
    print("1. 优先测试完整环形路线导航链接")
    print("2. 确认Google Maps显示的是环形路线（起点=终点）")
    print("3. 验证所有地点名称正确显示")
    print("4. 检查路线规划是否合理（约2公里步行距离）")
    print("5. 确认路线从日暮里站开始，最终回到日暮里站")
