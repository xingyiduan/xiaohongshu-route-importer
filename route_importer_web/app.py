#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
路线导入器 Web应用
主应用文件
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import json
import os
from datetime import datetime
from note_parser import XiaohongshuNoteParser
from route_planner import RoutePlanner
from database import Database

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

# 初始化组件
note_parser = XiaohongshuNoteParser()
route_planner = RoutePlanner()
db = Database()

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/import')
def import_page():
    """导入页面"""
    return render_template('import.html')

@app.route('/routes')
def routes_page():
    """路线列表页面"""
    return render_template('routes.html')

@app.route('/route/<route_id>')
def route_detail(route_id):
    """路线详情页面"""
    return render_template('route_detail.html', route_id=route_id)

# API接口

@app.route('/api/parse-note', methods=['POST'])
def parse_note():
    """解析小红书笔记"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': '请提供有效的链接'}), 400
        
        # 解析笔记
        note_data = note_parser.parse_note(url)
        
        if not note_data:
            return jsonify({'error': '无法解析该笔记'}), 400
        
        # 保存到session
        session['parsed_note'] = note_data
        
        return jsonify({
            'success': True,
            'data': note_data
        })
        
    except Exception as e:
        app.logger.error(f"解析笔记失败: {str(e)}")
        return jsonify({'error': f'解析失败: {str(e)}'}), 500

@app.route('/api/plan-route', methods=['POST'])
def plan_route():
    """规划路线"""
    try:
        data = request.get_json()
        places = data.get('places', [])
        
        if not places or len(places) < 2:
            return jsonify({'error': '至少需要2个地点来规划路线'}), 400
        
        # 规划路线
        route_data = route_planner.plan_walking_route(places)
        
        if not route_data:
            return jsonify({'error': '路线规划失败'}), 500
        
        # 保存到session
        session['planned_route'] = route_data
        
        return jsonify({
            'success': True,
            'data': route_data
        })
        
    except Exception as e:
        app.logger.error(f"路线规划失败: {str(e)}")
        return jsonify({'error': f'路线规划失败: {str(e)}'}), 500

@app.route('/api/save-route', methods=['POST'])
def save_route():
    """保存路线"""
    try:
        data = request.get_json()
        
        # 获取解析的笔记和规划的路线
        parsed_note = session.get('parsed_note')
        planned_route = session.get('planned_route')
        
        if not parsed_note or not planned_route:
            return jsonify({'error': '没有可保存的路线数据'}), 400
        
        # 构建完整的路线信息
        route_info = {
            'id': f"route_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'name': data.get('name', parsed_note.get('title', '未命名路线')),
            'description': data.get('description', parsed_note.get('content', '')),
            'source': '小红书',
            'source_url': data.get('source_url', ''),
            'places': parsed_note.get('places', []),
            'route': planned_route.get('route', []),
            'distance': planned_route.get('distance', 0),
            'duration': planned_route.get('duration', 0),
            'created_at': datetime.now().isoformat(),
            'tags': parsed_note.get('tags', [])
        }
        
        # 保存到数据库
        db.save_route(route_info)
        
        # 清除session
        session.pop('parsed_note', None)
        session.pop('planned_route', None)
        
        return jsonify({
            'success': True,
            'message': '路线保存成功',
            'route_id': route_info['id']
        })
        
    except Exception as e:
        app.logger.error(f"保存路线失败: {str(e)}")
        return jsonify({'error': f'保存失败: {str(e)}'}), 500

@app.route('/api/routes', methods=['GET'])
def get_routes():
    """获取所有保存的路线"""
    try:
        routes = db.get_all_routes()
        return jsonify({
            'success': True,
            'data': routes
        })
    except Exception as e:
        app.logger.error(f"获取路线列表失败: {str(e)}")
        return jsonify({'error': f'获取失败: {str(e)}'}), 500

@app.route('/api/route/<route_id>', methods=['GET'])
def get_route(route_id):
    """获取特定路线详情"""
    try:
        route = db.get_route(route_id)
        if not route:
            return jsonify({'error': '路线不存在'}), 404
        
        return jsonify({
            'success': True,
            'data': route
        })
    except Exception as e:
        app.logger.error(f"获取路线详情失败: {str(e)}")
        return jsonify({'error': f'获取失败: {str(e)}'}), 500

@app.route('/api/route/<route_id>', methods=['DELETE'])
def delete_route(route_id):
    """删除路线"""
    try:
        success = db.delete_route(route_id)
        if not success:
            return jsonify({'error': '路线不存在'}), 404
        
        return jsonify({
            'success': True,
            'message': '路线删除成功'
        })
    except Exception as e:
        app.logger.error(f"删除路线失败: {str(e)}")
        return jsonify({'error': f'删除失败: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # 确保数据库初始化
    db.init_database()
    
    # 启动应用
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=True
    )
