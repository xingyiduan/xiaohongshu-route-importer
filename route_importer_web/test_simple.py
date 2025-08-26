#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的Flask测试应用
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Flask is working!'

if __name__ == '__main__':
    print("启动简单Flask应用...")
    app.run(
        host='0.0.0.0',
        port=8081,
        debug=True
    )
