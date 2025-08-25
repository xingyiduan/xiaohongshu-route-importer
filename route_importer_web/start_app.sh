#!/bin/bash

# 小红书路线导入器启动脚本
# 集成火山引擎豆包API版本

echo "🚀 小红书路线导入器 - AI增强版"
echo "=================================="

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3 命令"
    echo "请确保已安装 Python 3.7+"
    exit 1
fi

# 检查是否在正确的目录
if [ ! -f "app_integrated.py" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    echo "当前目录: $(pwd)"
    exit 1
fi

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "⚠️  警告: 未找到 .env 文件"
    echo "将使用默认配置"
else
    echo "✅ 找到环境配置文件"
fi

# 检查依赖文件
echo "🔍 检查依赖文件..."
required_files=("volcengine_douban_final.py" "smart_parser_final.py" "note_parser.py" "route_planner.py" "database.py")
missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo "❌ 错误: 缺少以下依赖文件:"
    for file in "${missing_files[@]}"; do
        echo "   - $file"
    done
    exit 1
fi

echo "✅ 所有依赖文件检查通过"

# 检查端口占用
PORT=8080
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  警告: 端口 $PORT 已被占用"
    echo "正在尝试停止占用进程..."
    
    # 尝试停止占用端口的进程
    PID=$(lsof -ti:$PORT)
    if [ ! -z "$PID" ]; then
        echo "停止进程 PID: $PID"
        kill -9 $PID 2>/dev/null
        sleep 2
    fi
    
    # 再次检查端口
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
        echo "❌ 无法释放端口 $PORT，请手动停止占用进程"
        exit 1
    else
        echo "✅ 端口 $PORT 已释放"
    fi
fi

# 设置环境变量
export VOLCENGINE_API_KEY="daf37bb4-0e7b-42f8-87bb-b780842dd0d8"
export FLASK_ENV=development
export SECRET_KEY="your_secret_key_here"

echo "🔧 环境变量已设置"
echo "   - VOLCENGINE_API_KEY: ${VOLCENGINE_API_KEY:0:10}..."
echo "   - FLASK_ENV: $FLASK_ENV"
echo "   - 端口: $PORT"

# 启动应用
echo ""
echo "🎯 正在启动应用..."
echo "📱 应用将在以下地址启动:"
echo "   - 本地访问: http://localhost:$PORT"
echo "   - 局域网访问: http://$(hostname -I | awk '{print $1}'):$PORT"
echo ""
echo "按 Ctrl+C 停止应用"
echo "=================================="

# 启动应用
python3 app_integrated.py
