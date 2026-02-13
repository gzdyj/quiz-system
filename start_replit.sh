#!/bin/bash

# Replit 启动脚本
# 启动后端和前端服务

echo "🚀 启动刷题系统..."
echo ""

# 进入后端目录
cd backend

# 安装依赖
echo "📦 安装 Python 依赖..."
pip install -q -r requirements.txt

# 初始化数据库
echo "🗄️ 初始化数据库..."
python3 init_data.py

# 启动后端（后台）
echo "⚙️ 启动后端 API 服务..."
python3 -c "
from app import app, db
from flask import Flask
import threading
import time

def run_backend():
    app.run(host='0.0.0.0', port=5000, debug=False)

# 在后台线程启动后端
backend_thread = threading.Thread(target=run_backend, daemon=True)
backend_thread.start()

# 保持主线程运行
time.sleep(100000)
" &

# 等待后端启动
sleep 3

# 启动前端（主进程）
echo "📱 启动前端服务..."
cd ../frontend
python3 -m http.server 8000
