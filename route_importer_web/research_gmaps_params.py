#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
研究Google Maps URL参数
寻找显示地点名称的方法
"""

import urllib.parse

def research_gmaps_parameters():
    """研究Google Maps的各种URL参数"""
    
    print("🔍 研究Google Maps URL参数")
    print("="*60)
    
    # 基础坐标
    origin = "35.7278,139.7708"  # 日暮里站
    destination = "35.7255,139.7670"  # 猫猫神社
    waypoints = [
        "35.7265,139.7690",  # 朝仓雕塑馆
        "35.7260,139.7680",  # 谷中银座商业街
        "35.7280,139.7650"   # Museca Times
    ]
    
    print("📍 测试不同的URL格式：")
    print()
    
    # 1. 使用地址而不是坐标
    print("1️⃣ 使用地址格式（可能显示地点名称）：")
    addresses = [
        "Nippori Station, Tokyo, Japan",
        "7 Chome-18-10 Yanaka, Taito City, Tokyo 110-0001, Japan",
        "Yanaka Ginza Shopping Street, Tokyo, Japan",
        "3 Chome-41-16 Sendagi, Bunkyo City, Tokyo 113-0022, Japan",
        "2 Chome-1-4 Yanaka, Taito City, Tokyo 110-0001, Japan"
    ]
    
    # 构建地址格式的导航链接
    origin_addr = urllib.parse.quote(addresses[0])
    dest_addr = urllib.parse.quote(addresses[-1])
    waypoint_addrs = "|".join([urllib.parse.quote(addr) for addr in addresses[1:-1]])
    
    address_url = f"https://www.google.com/maps/dir/{origin_addr}/{dest_addr}/data=!4m2!4m1!3e2"
    if waypoint_addrs:
        address_url = f"https://www.google.com/maps/dir/{origin_addr}/{waypoint_addrs}/{dest_addr}/data=!4m2!4m1!3e2"
    
    print(f"完整地址链接：{address_url}")
    print()
    
    # 2. 使用地点名称搜索
    print("2️⃣ 使用地点名称搜索格式：")
    place_names = [
        "日暮里站",
        "朝仓雕塑馆", 
        "谷中银座商业街",
        "Museca Times 牛肉汉堡店",
        "猫猫神社"
    ]
    
    # 构建搜索格式的链接
    search_waypoints = "|".join([urllib.parse.quote(name) for name in place_names[1:-1]])
    search_url = f"https://www.google.com/maps/dir/{urllib.parse.quote(place_names[0])}/{search_waypoints}/{urllib.parse.quote(place_names[-1])}/data=!4m2!4m1!3e2"
    
    print(f"搜索格式链接：{search_url}")
    print()
    
    # 3. 使用Google Maps的place_id（如果可用）
    print("3️⃣ 尝试使用Google Maps Place ID：")
    print("注意：这需要Google Places API来获取准确的place_id")
    
    # 4. 使用自定义标签
    print("4️⃣ 尝试使用自定义标签参数：")
    
    # 构建带标签的URL
    labeled_waypoints = []
    for i, (name, coord) in enumerate(zip(place_names[1:-1], waypoints)):
        labeled_waypoints.append(f"{coord}|{urllib.parse.quote(name)}")
    
    labeled_url = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&waypoints={'|'.join(labeled_waypoints)}&travelmode=walking"
    
    print(f"带标签的链接：{labeled_url}")
    print()
    
    # 5. 使用Google Maps的共享链接格式
    print("5️⃣ 尝试Google Maps共享链接格式：")
    
    # 构建共享格式的URL
    share_url = f"https://www.google.com/maps/dir/{origin}/{destination}/data=!4m2!4m1!3e2"
    if waypoints:
        share_url = f"https://www.google.com/maps/dir/{origin}/{'/'.join(waypoints)}/{destination}/data=!4m2!4m1!3e2"
    
    print(f"共享格式链接：{share_url}")
    print()
    
    # 6. 使用Google Maps的嵌入格式
    print("6️⃣ 尝试Google Maps嵌入格式：")
    
    embed_url = f"https://www.google.com/maps/embed/v1/directions?key=YOUR_API_KEY&origin={origin}&destination={destination}&waypoints={'|'.join(waypoints)}&mode=walking"
    
    print(f"嵌入格式链接（需要API密钥）：{embed_url}")
    print()
    
    return {
        'address_url': address_url,
        'search_url': search_url,
        'labeled_url': labeled_url,
        'share_url': share_url
    }

def generate_alternative_solutions():
    """生成替代解决方案"""
    
    print("🔄 替代解决方案：")
    print("="*60)
    
    # 1. 生成每个地点的单独链接，然后手动组合
    print("1️⃣ 生成每个地点的单独链接：")
    places = [
        ("日暮里站", "Nippori Station, Tokyo, Japan"),
        ("朝仓雕塑馆", "7 Chome-18-10 Yanaka, Taito City, Tokyo 110-0001, Japan"),
        ("谷中银座商业街", "Yanaka Ginza Shopping Street, Tokyo, Japan"),
        ("Museca Times", "3 Chome-41-16 Sendagi, Bunkyo City, Tokyo 113-0022, Japan"),
        ("猫猫神社", "2 Chome-1-4 Yanaka, Taito City, Tokyo 110-0001, Japan")
    ]
    
    for name, address in places:
        search_url = f"https://www.google.com/maps/search/{urllib.parse.quote(address)}"
        print(f"{name}: {search_url}")
    
    print()
    
    # 2. 使用Google My Maps创建自定义地图
    print("2️⃣ 使用Google My Maps创建自定义地图：")
    print("https://www.google.com/mymaps")
    print("可以手动创建包含所有地点的自定义地图，然后分享链接")
    print()
    
    # 3. 生成路线描述文本
    print("3️⃣ 生成路线描述文本：")
    route_description = """
🚶‍♀️ 东京日暮里City Walk路线：

📍 起点：日暮里站 (Nippori Station)
   https://www.google.com/maps/search/Nippori+Station,+Tokyo,+Japan

📍 第1站：朝仓雕塑馆 (Asakura Museum of Sculpture)
   https://www.google.com/maps/search/7+Chome-18-10+Yanaka,+Taito+City,+Tokyo+110-0001,+Japan

📍 第2站：谷中银座商业街 (Yanaka Ginza Shopping Street)
   https://www.google.com/maps/search/Yanaka+Ginza+Shopping+Street,+Tokyo,+Japan

📍 第3站：Museca Times 牛肉汉堡店
   https://www.google.com/maps/search/3+Chome-41-16+Sendagi,+Bunkyo+City,+Tokyo+113-0022,+Japan

📍 终点：猫猫神社 (Cat Shrine)
   https://www.google.com/maps/search/2+Chome-1-4+Yanaka,+Taito+City,+Tokyo+110-0001,+Japan

🗺️ 完整路线导航：
https://www.google.com/maps/dir/Nippori+Station,+Tokyo,+Japan/2+Chome-1-4+Yanaka,+Taito+City,+Tokyo+110-0001,+Japan/data=!4m2!4m1!3e2
"""
    
    print(route_description)
    
    # 4. 建议的Web应用改进
    print("4️⃣ Web应用改进建议：")
    print("- 在Web页面中显示每个地点的名称和描述")
    print("- 提供每个地点的单独Google Maps链接")
    print("- 生成包含地点名称的路线描述文本")
    print("- 考虑集成Google My Maps API")
    print("- 提供路线导出的多种格式选择")

if __name__ == "__main__":
    print("🚀 研究Google Maps URL参数")
    print("="*60)
    
    # 研究各种参数
    urls = research_gmaps_parameters()
    
    print("\n" + "="*60)
    
    # 生成替代解决方案
    generate_alternative_solutions()
    
    print("\n" + "="*60)
    print("📱 测试建议：")
    print("1. 优先测试地址格式的链接（可能显示地点名称）")
    print("2. 测试搜索格式的链接（使用地点名称）")
    print("3. 如果都不行，考虑使用Google My Maps")
    print("4. 在Web应用中提供每个地点的单独链接")
