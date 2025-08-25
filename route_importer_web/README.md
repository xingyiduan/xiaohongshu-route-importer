# 路线导入器 Web应用

这是一个独立的Web应用程序，用于解析小红书笔记链接，提取地点信息，并生成步行路线规划。

## 功能特性

- 🔗 解析小红书笔记链接
- 📍 自动提取笔记中提到的地点信息
- 🗺️ 调用地图API进行路线规划
- 🚶 生成优化的步行路线
- 📱 响应式设计，支持移动端
- 💾 保存和分享路线

## 技术架构

- **前端**: HTML5 + CSS3 + JavaScript (ES6+)
- **后端**: Python Flask
- **地图服务**: 高德地图API / 百度地图API
- **数据存储**: SQLite / JSON文件
- **部署**: 可部署到云服务器或本地

## 项目结构

```
route_importer_web/
├── static/                 # 静态资源
│   ├── css/               # 样式文件
│   ├── js/                # JavaScript文件
│   └── images/            # 图片资源
├── templates/             # HTML模板
├── app.py                 # Flask主应用
├── route_planner.py       # 路线规划逻辑
├── note_parser.py         # 笔记解析逻辑
├── database.py            # 数据库操作
├── requirements.txt       # Python依赖
└── config.py              # 配置文件
```

## 安装和运行

1. 安装Python依赖：
```bash
pip install -r requirements.txt
```

2. 配置API密钥：
```bash
cp config.example.py config.py
# 编辑config.py，填入您的地图API密钥
```

3. 运行应用：
```bash
python app.py
```

4. 访问应用：
```
http://localhost:5000
```

## API接口

### 解析笔记
- **POST** `/api/parse-note`
- 请求体: `{"url": "小红书笔记链接"}`
- 返回: 解析后的地点和标签信息

### 规划路线
- **POST** `/api/plan-route`
- 请求体: `{"places": [地点坐标数组]}`
- 返回: 规划的路线数据

### 保存路线
- **POST** `/api/save-route`
- 请求体: 路线信息
- 返回: 保存成功状态

## 开发计划

- [x] 项目架构设计
- [ ] 基础Web界面
- [ ] 小红书笔记解析器
- [ ] 地图API集成
- [ ] 路线规划算法
- [ ] 数据存储功能
- [ ] 用户界面优化
- [ ] 部署和测试

## 许可证

MIT License
