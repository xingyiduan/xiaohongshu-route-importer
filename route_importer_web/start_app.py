#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书路线导入器启动脚本
支持跨平台，自动检查和配置
"""

import os
import sys
import subprocess
import socket
import time
import signal
from pathlib import Path

class AppLauncher:
    """应用启动器"""
    
    def __init__(self):
        self.port = 8080
        self.app_file = "app_integrated.py"
        self.required_files = [
            "volcengine_douban_final.py",
            "smart_parser_final.py", 
            "note_parser.py",
            "route_planner.py",
            "database.py"
        ]
        
    def print_header(self):
        """打印启动头部信息"""
        print("🚀 小红书路线导入器 - AI增强版")
        print("=" * 50)
        print(f"版本: 集成火山引擎豆包API")
        print(f"端口: {self.port}")
        print(f"时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    def check_python_version(self):
        """检查Python版本"""
        print("🔍 检查Python环境...")
        
        if sys.version_info < (3, 7):
            print(f"❌ 错误: Python版本过低 ({sys.version})")
            print("   需要Python 3.7+")
            return False
        
        print(f"✅ Python版本: {sys.version}")
        return True
    
    def check_working_directory(self):
        """检查工作目录"""
        print("🔍 检查工作目录...")
        
        current_dir = Path.cwd()
        app_path = current_dir / self.app_file
        
        if not app_path.exists():
            print(f"❌ 错误: 未找到主应用文件 {self.app_file}")
            print(f"   当前目录: {current_dir}")
            print("   请在项目根目录运行此脚本")
            return False
        
        print(f"✅ 工作目录: {current_dir}")
        return True
    
    def check_dependencies(self):
        """检查依赖文件"""
        print("🔍 检查依赖文件...")
        
        missing_files = []
        for file_name in self.required_files:
            if not Path(file_name).exists():
                missing_files.append(file_name)
        
        if missing_files:
            print("❌ 错误: 缺少以下依赖文件:")
            for file_name in missing_files:
                print(f"   - {file_name}")
            return False
        
        print("✅ 所有依赖文件检查通过")
        return True
    
    def check_port_availability(self):
        """检查端口可用性"""
        print("🔍 检查端口可用性...")
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', self.port))
                print(f"✅ 端口 {self.port} 可用")
                return True
        except OSError:
            print(f"⚠️  警告: 端口 {self.port} 被占用")
            
            # 尝试释放端口
            if self.try_release_port():
                print(f"✅ 端口 {self.port} 已释放")
                return True
            else:
                print(f"❌ 无法释放端口 {self.port}")
                return False
    
    def try_release_port(self):
        """尝试释放端口"""
        try:
            # 在macOS/Linux上使用lsof
            if sys.platform in ['darwin', 'linux']:
                result = subprocess.run(['lsof', '-ti', f':{self.port}'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    pids = result.stdout.strip().split('\n')
                    for pid in pids:
                        if pid:
                            subprocess.run(['kill', '-9', pid])
                            time.sleep(1)
                    return True
            return False
        except Exception:
            return False
    
    def setup_environment(self):
        """设置环境变量"""
        print("🔧 设置环境变量...")
        
        env_vars = {
            'VOLCENGINE_API_KEY': 'daf37bb4-0e7b-42f8-87bb-b780842dd0d8',
            'FLASK_ENV': 'development',
            'SECRET_KEY': 'your_secret_key_here'
        }
        
        for key, value in env_vars.items():
            os.environ[key] = value
            print(f"   - {key}: {value[:10] if len(value) > 10 else value}...")
        
        print("✅ 环境变量设置完成")
    
    def get_network_info(self):
        """获取网络信息"""
        try:
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            return hostname, local_ip
        except Exception:
            return "localhost", "127.0.0.1"
    
    def launch_app(self):
        """启动应用"""
        print("🎯 启动应用...")
        
        hostname, local_ip = self.get_network_info()
        
        print("📱 应用将在以下地址启动:")
        print(f"   - 本地访问: http://localhost:{self.port}")
        print(f"   - 局域网访问: http://{local_ip}:{self.port}")
        print()
        print("按 Ctrl+C 停止应用")
        print("=" * 50)
        print()
        
        try:
            # 启动Flask应用
            subprocess.run([sys.executable, self.app_file], check=True)
        except KeyboardInterrupt:
            print("\n🛑 应用已停止")
        except subprocess.CalledProcessError as e:
            print(f"❌ 应用启动失败: {e}")
            return False
        
        return True
    
    def run(self):
        """运行启动器"""
        try:
            self.print_header()
            
            # 执行检查
            checks = [
                self.check_python_version,
                self.check_working_directory,
                self.check_dependencies,
                self.check_port_availability
            ]
            
            for check in checks:
                if not check():
                    return False
            
            # 设置环境
            self.setup_environment()
            
            # 启动应用
            return self.launch_app()
            
        except KeyboardInterrupt:
            print("\n🛑 启动被用户中断")
            return False
        except Exception as e:
            print(f"❌ 启动过程中发生错误: {e}")
            return False

def main():
    """主函数"""
    launcher = AppLauncher()
    success = launcher.run()
    
    if not success:
        print("\n❌ 启动失败，请检查错误信息")
        input("按回车键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main()
