@echo off
chcp 65001 >nul
title 小红书路线导入器 - AI增强版

echo 🚀 小红书路线导入器 - AI增强版
echo ==================================

REM 检查Python版本
python --version >nul 2>&1
if errorlevel 1 (
    python3 --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ 错误: 未找到 Python 命令
        echo 请确保已安装 Python 3.7+
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=python3
    )
) else (
    set PYTHON_CMD=python
)

REM 检查是否在正确的目录
if not exist "app_integrated.py" (
    echo ❌ 错误: 请在项目根目录运行此脚本
    echo 当前目录: %CD%
    pause
    exit /b 1
)

REM 检查环境变量文件
if not exist ".env" (
    echo ⚠️  警告: 未找到 .env 文件
    echo 将使用默认配置
) else (
    echo ✅ 找到环境配置文件
)

REM 检查依赖文件
echo 🔍 检查依赖文件...
set missing_files=0
for %%f in (volcengine_douban_final.py smart_parser_final.py note_parser.py route_planner.py database.py) do (
    if not exist "%%f" (
        echo   缺少文件: %%f
        set /a missing_files+=1
    )
)

if %missing_files% gtr 0 (
    echo ❌ 错误: 缺少 %missing_files% 个依赖文件
    pause
    exit /b 1
)

echo ✅ 所有依赖文件检查通过

REM 检查端口占用
set PORT=8080
netstat -an | find ":%PORT%" >nul 2>&1
if not errorlevel 1 (
    echo ⚠️  警告: 端口 %PORT% 可能被占用
    echo 如果启动失败，请检查端口占用情况
)

REM 设置环境变量
set VOLCENGINE_API_KEY=daf37bb4-0e7b-42f8-87bb-b780842dd0d8
set FLASK_ENV=development
set SECRET_KEY=your_secret_key_here

echo 🔧 环境变量已设置
echo    - VOLCENGINE_API_KEY: %VOLCENGINE_API_KEY:~0,10%...
echo    - FLASK_ENV: %FLASK_ENV%
echo    - 端口: %PORT%

REM 启动应用
echo.
echo 🎯 正在启动应用...
echo 📱 应用将在以下地址启动:
echo    - 本地访问: http://localhost:%PORT%
echo    - 局域网访问: http://%COMPUTERNAME%:%PORT%
echo.
echo 按 Ctrl+C 停止应用
echo ==================================

REM 启动应用
%PYTHON_CMD% app_integrated.py

pause
