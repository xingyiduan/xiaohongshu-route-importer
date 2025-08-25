#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
路线规划器
"""

import math
from typing import List, Dict, Optional

class RoutePlanner:
    def __init__(self):
        pass
    
    def plan_walking_route(self, places: List[Dict]) -> Optional[Dict]:
        """
        规划步行路线
        
        Args:
            places: 地点列表
            
        Returns:
            规划的路线数据
        """
        if not places or len(places) < 2:
            return None
        
        try:
            # 计算路线距离和时间
            total_distance = self._calculate_total_distance(places)
            estimated_duration = self._estimate_duration(total_distance)
            
            # 生成路线点
            route_points = self._generate_route_points(places)
            
            return {
                'route': route_points,
                'distance': total_distance,
                'duration': estimated_duration,
                'waypoints': len(places)
            }
            
        except Exception as e:
            print(f"路线规划失败: {e}")
            return None
    
    def _calculate_total_distance(self, places: List[Dict]) -> float:
        """计算总距离（公里）"""
        total_distance = 0.0
        
        for i in range(len(places) - 1):
            current = places[i]
            next_place = places[i + 1]
            
            # 获取坐标
            current_coords = current.get('coordinates', {})
            next_coords = next_place.get('coordinates', {})
            
            if current_coords and next_coords:
                distance = self._calculate_distance_between_points(
                    current_coords.get('lat', 0),
                    current_coords.get('lng', 0),
                    next_coords.get('lat', 0),
                    next_coords.get('lng', 0)
                )
                total_distance += distance
        
        # 如果是环形路线，添加回到起点的距离
        if len(places) > 2:
            first_coords = places[0].get('coordinates', {})
            last_coords = places[-1].get('coordinates', {})
            
            if first_coords and last_coords:
                final_distance = self._calculate_distance_between_points(
                    last_coords.get('lat', 0),
                    last_coords.get('lng', 0),
                    first_coords.get('lat', 0),
                    first_coords.get('lng', 0)
                )
                total_distance += final_distance
        
        return total_distance
    
    def _calculate_distance_between_points(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """计算两点间距离（公里）"""
        # 使用Haversine公式计算球面距离
        R = 6371  # 地球半径（公里）
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def _estimate_duration(self, distance_km: float) -> int:
        """估算步行时间（分钟）"""
        # 假设步行速度为5公里/小时
        walking_speed = 5.0  # 公里/小时
        duration_hours = distance_km / walking_speed
        return int(duration_hours * 60)
    
    def _generate_route_points(self, places: List[Dict]) -> List[Dict]:
        """生成路线点数据"""
        route_points = []
        
        for place in places:
            coords = place.get('coordinates', {})
            if coords:
                route_points.append({
                    'latitude': coords.get('lat', 0),
                    'longitude': coords.get('lng', 0),
                    'elevation': None,
                    'timestamp': None
                })
        
        return route_points
