#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库操作模块
"""

import sqlite3
import json
from typing import List, Dict, Optional
from datetime import datetime

class Database:
    def __init__(self, db_path: str = 'routes.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 创建路线表
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS routes (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        description TEXT,
                        source TEXT,
                        source_url TEXT,
                        places TEXT,
                        route TEXT,
                        distance REAL,
                        duration INTEGER,
                        tags TEXT,
                        created_at TEXT,
                        updated_at TEXT
                    )
                ''')
                
                conn.commit()
                print("数据库初始化成功")
                
        except Exception as e:
            print(f"数据库初始化失败: {e}")
    
    def save_route(self, route_info: Dict) -> bool:
        """保存路线"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 准备数据
                places_json = json.dumps(route_info.get('places', []), ensure_ascii=False)
                route_json = json.dumps(route_info.get('route', []), ensure_ascii=False)
                tags_json = json.dumps(route_info.get('tags', []), ensure_ascii=False)
                
                # 插入或更新路线
                cursor.execute('''
                    INSERT OR REPLACE INTO routes 
                    (id, name, description, source, source_url, places, route, distance, duration, tags, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    route_info.get('id'),
                    route_info.get('name'),
                    route_info.get('description'),
                    route_info.get('source'),
                    route_info.get('source_url'),
                    places_json,
                    route_json,
                    route_info.get('distance'),
                    route_info.get('duration'),
                    tags_json,
                    route_info.get('created_at'),
                    datetime.now().isoformat()
                ))
                
                conn.commit()
                print(f"路线保存成功: {route_info.get('name')}")
                return True
                
        except Exception as e:
            print(f"保存路线失败: {e}")
            return False
    
    def get_route(self, route_id: str) -> Optional[Dict]:
        """获取特定路线"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('SELECT * FROM routes WHERE id = ?', (route_id,))
                row = cursor.fetchone()
                
                if row:
                    return self._row_to_dict(row)
                return None
                
        except Exception as e:
            print(f"获取路线失败: {e}")
            return None
    
    def get_all_routes(self) -> List[Dict]:
        """获取所有路线"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('SELECT * FROM routes ORDER BY created_at DESC')
                rows = cursor.fetchall()
                
                return [self._row_to_dict(row) for row in rows]
                
        except Exception as e:
            print(f"获取所有路线失败: {e}")
            return []
    
    def delete_route(self, route_id: str) -> bool:
        """删除路线"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('DELETE FROM routes WHERE id = ?', (route_id,))
                conn.commit()
                
                if cursor.rowcount > 0:
                    print(f"路线删除成功: {route_id}")
                    return True
                else:
                    print(f"路线不存在: {route_id}")
                    return False
                
        except Exception as e:
            print(f"删除路线失败: {e}")
            return False
    
    def search_routes(self, keyword: str) -> List[Dict]:
        """搜索路线"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                search_pattern = f'%{keyword}%'
                cursor.execute('''
                    SELECT * FROM routes 
                    WHERE name LIKE ? OR description LIKE ? OR tags LIKE ?
                    ORDER BY created_at DESC
                ''', (search_pattern, search_pattern, search_pattern))
                
                rows = cursor.fetchall()
                return [self._row_to_dict(row) for row in rows]
                
        except Exception as e:
            print(f"搜索路线失败: {e}")
            return []
    
    def _row_to_dict(self, row) -> Dict:
        """将数据库行转换为字典"""
        columns = ['id', 'name', 'description', 'source', 'source_url', 'places', 'route', 'distance', 'duration', 'tags', 'created_at', 'updated_at']
        
        route_dict = {}
        for i, column in enumerate(columns):
            value = row[i]
            
            # 解析JSON字段
            if column in ['places', 'route', 'tags'] and value:
                try:
                    route_dict[column] = json.loads(value)
                except:
                    route_dict[column] = []
            else:
                route_dict[column] = value
        
        return route_dict
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 总路线数
                cursor.execute('SELECT COUNT(*) FROM routes')
                total_routes = cursor.fetchone()[0]
                
                # 总距离
                cursor.execute('SELECT SUM(distance) FROM routes')
                total_distance = cursor.fetchone()[0] or 0
                
                # 总时间
                cursor.execute('SELECT SUM(duration) FROM routes')
                total_duration = cursor.fetchone()[0] or 0
                
                # 平均距离
                avg_distance = total_distance / total_routes if total_routes > 0 else 0
                
                return {
                    'total_routes': total_routes,
                    'total_distance': round(total_distance, 2),
                    'total_duration': total_duration,
                    'avg_distance': round(avg_distance, 2)
                }
                
        except Exception as e:
            print(f"获取统计信息失败: {e}")
            return {}
