#!/bin/bash

# 刷题系统快速启动脚本

set -e

echo "================================"
echo "计算机刷题系统启动脚本"
echo "================================"
echo ""

# 检查Docker和Docker Compose
if ! command -v docker &> /dev/null; then
    echo "❌ 未发现Docker，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ 未发现Docker Compose，请先安装Docker Compose"
    exit 1
fi

echo "✓ Docker已安装"
echo "✓ Docker Compose已安装"
echo ""

# 启动服务
echo "正在启动服务..."
docker-compose up -d

# 等待服务启动
echo "等待服务启动..."
sleep 5

# 检查后端健康
echo "检查后端服务..."
for i in {1..30}; do
    if curl -s http://localhost:5000/health > /dev/null; then
        echo "✓ 后端服务已启动"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ 后端服务启动失败"
        exit 1
    fi
    sleep 1
done

# 初始化数据库
echo ""
echo "初始化数据库..."
docker-compose exec -T backend python init_data.py

echo ""
echo "================================"
echo "✓ 启动完成！"
echo "================================"
echo ""
echo "访问地址:"
echo "  前端: http://localhost"
echo "  后端API: http://localhost:5000"
echo ""
echo "常用命令:"
echo "  查看日志:     docker-compose logs -f"
echo "  停止服务:     docker-compose down"
echo "  重启服务:     docker-compose restart"
echo ""
