# 部署指南

本文档详细说明如何在不同环境中部署刷题系统。

## 目录
1. [Docker部署](#docker部署)
2. [Linux服务器部署](#linux服务器部署)
3. [Windows本地部署](#windows本地部署)
4. [云服务部署](#云服务部署)
5. [监控和维护](#监控和维护)

---

## Docker部署

### 推荐配置

#### 系统要求
- Docker 20.10+
- Docker Compose 2.0+
- 至少2GB内存
- 至少1GB硬盘空间

#### 部署步骤

##### 1. 拉取项目代码
```bash
# 如果有Git仓库
git clone <your-repo-url>
cd quiz-system

# 或直接复制项目文件
```

##### 2. 构建镜像
```bash
# 使用docker-compose自动构建
docker-compose build

# 或手动构建单个镜像
docker build -t quiz-backend:latest ./backend
docker build -t quiz-frontend:latest ./frontend
```

##### 3. 启动服务
```bash
# 后台启动
docker-compose up -d

# 前台启动（调试用）
docker-compose up
```

##### 4. 初始化数据库
```bash
# 进入后端容器
docker-compose exec backend bash

# 运行初始化脚本
python init_data.py

# 检查数据库
ls -la /data/

# 退出容器
exit
```

##### 5. 验证部署
```bash
# 检查容器状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 测试后端API
curl http://localhost:5000/health

# 测试前端
curl http://localhost
```

#### 常用命令

```bash
# 查看日志
docker-compose logs -f backend    # 后端日志
docker-compose logs -f frontend   # 前端日志

# 进入容器
docker-compose exec backend bash
docker-compose exec frontend bash

# 重启服务
docker-compose restart

# 停止服务
docker-compose stop

# 完全清除
docker-compose down -v  # -v 删除数据卷

# 更新代码后重新部署
docker-compose up -d --build
```

### 自定义Docker配置

#### 修改端口
编辑 `docker-compose.yml`:
```yaml
services:
  backend:
    ports:
      - "8000:5000"  # 改为8000

  frontend:
    ports:
      - "8080:80"    # 改为8080
```

#### 修改环境变量
```yaml
services:
  backend:
    environment:
      - FLASK_ENV=development
      - DATABASE_URL=postgresql://user:pass@db:5432/quiz
```

#### 添加数据库服务
```yaml
version: '3.8'

services:
  backend:
    # ... 其他配置
    depends_on:
      - db

  frontend:
    # ... 其他配置

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: quiz
      POSTGRES_PASSWORD: secure_password
      POSTGRES_DB: quiz
    volumes:
      - db_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  db_data:
  quiz_data:
```

---

## Linux服务器部署

### 系统环境准备

#### 安装依赖
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx curl

# CentOS/RHEL
sudo yum install -y python3 python3-pip nginx curl
```

#### 创建专用用户
```bash
sudo useradd -m -s /bin/bash quiz
sudo su - quiz
```

### 后端部署

#### 1. 克隆代码
```bash
cd /opt
git clone <repo> quiz-system
cd quiz-system/backend
```

#### 2. 创建虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. 安装依赖
```bash
pip install -r requirements.txt
```

#### 4. 初始化数据库
```bash
python init_data.py
```

#### 5. 配置Systemd服务

创建 `/etc/systemd/system/quiz-backend.service`:
```ini
[Unit]
Description=Quiz Backend Service
After=network.target

[Service]
User=quiz
WorkingDirectory=/opt/quiz-system/backend
ExecStart=/opt/quiz-system/backend/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind 127.0.0.1:5000 \
    app:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务:
```bash
sudo systemctl daemon-reload
sudo systemctl start quiz-backend
sudo systemctl enable quiz-backend
sudo systemctl status quiz-backend
```

### 前端部署

#### 1. 部署文件
```bash
sudo mkdir -p /var/www/quiz
sudo cp -r frontend/* /var/www/quiz/
```

#### 2. 配置Nginx

创建 `/etc/nginx/sites-available/quiz`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 重定向HTTP到HTTPS（生产推荐）
    # return 301 https://$server_name$request_uri;

    root /var/www/quiz;
    index index.html;

    # 前端路由处理
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 代理API请求到后端
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 静态文件缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

启用配置:
```bash
sudo ln -s /etc/nginx/sites-available/quiz /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 配置HTTPS（推荐）

#### 使用Let's Encrypt
```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot certonly --nginx -d your-domain.com

# 自动更新
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

#### Nginx配置更新
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # ... 其他配置同上 ...
}

# HTTP重定向到HTTPS
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

---

## Windows本地部署

### 前置条件
- Python 3.8+
- Node.js（可选）
- Visual Studio Code或其他编辑器

### 后端配置

#### 1. 创建虚拟环境
```cmd
cd backend
python -m venv venv
venv\Scripts\activate
```

#### 2. 安装依赖
```cmd
pip install -r requirements.txt
```

#### 3. 初始化数据库
```cmd
python init_data.py
```

#### 4. 运行后端
```cmd
# 开发模式
python app.py

# 或使用Gunicorn
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 app:app
```

### 前端配置

#### 使用Python内置服务器
```cmd
cd frontend
python -m http.server 8000
```

访问：`http://localhost:8000`

#### 或使用VS Code Live Server
- 安装Live Server扩展
- 右键 `index.html` → Open with Live Server

### 修改API地址

如果前后端端口不同，编辑 `frontend/app.js`:
```javascript
const API_BASE = 'http://localhost:5000/api';
```

---

## 云服务部署

### AWS EC2部署

#### 1. 启动EC2实例
- 选择Ubuntu 22.04 LTS
- 至少2GB内存
- 安全组允许80、443端口

#### 2. 连接实例
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

#### 3. 安装Docker
```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
```

#### 4. 部署应用
```bash
git clone <your-repo>
cd quiz-system
docker-compose up -d
```

### Heroku部署

#### 1. 创建Heroku应用
```bash
heroku create your-app-name
```

#### 2. 添加Procfile
```
web: gunicorn --bind 0.0.0.0:$PORT app:app
```

#### 3. 部署
```bash
git push heroku main
```

### DigitalOcean App Platform

1. 连接GitHub仓库
2. 创建新应用
3. 配置环境变量
4. 部署

---

## 监控和维护

### 日志管理

#### 查看日志
```bash
# Docker
docker-compose logs -f

# Linux
journalctl -u quiz-backend -f
tail -f /var/log/nginx/access.log
```

#### 日志轮转
创建 `/etc/logrotate.d/quiz`:
```
/var/log/quiz/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 quiz quiz
    sharedscripts
}
```

### 备份策略

#### 数据库备份
```bash
# SQLite备份
cp /data/questions.db /backup/questions.db.$(date +%Y%m%d)

# PostgreSQL备份（如适用）
pg_dump quiz_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

#### 自动备份脚本
```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/backup"
DB_PATH="/data/questions.db"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
cp $DB_PATH $BACKUP_DIR/questions_db_$DATE.db
find $BACKUP_DIR -name "*.db" -mtime +30 -delete
```

设置Cron定时执行:
```bash
0 2 * * * /path/to/backup.sh
```

### 性能监控

#### CPU和内存使用
```bash
# Docker
docker stats

# Linux
top
htop
```

#### 网络监控
```bash
# 查看并发连接
netstat -an | grep ESTABLISHED | wc -l

# 查看带宽使用
iftop -i eth0
```

### 健康检查

#### 检查脚本
```bash
#!/bin/bash
BACKEND_URL="http://localhost:5000/health"

response=$(curl -s -o /dev/null -w "%{http_code}" $BACKEND_URL)

if [ $response -ne 200 ]; then
    echo "Backend is down!"
    # 重启或告警
    systemctl restart quiz-backend
fi
```

设置定时检查:
```bash
*/5 * * * * /path/to/health-check.sh
```

### 更新维护

#### 更新应用
```bash
# 备份现有数据
cp -r /data /data.backup

# 拉取新代码
git pull origin main

# 重建Docker镜像
docker-compose build
docker-compose up -d

# 数据库迁移（如需要）
docker-compose exec backend python migrate.py
```

---

## 故障排查

### 后端无法启动

```bash
# 检查端口占用
sudo lsof -i :5000

# 查看具体错误
docker-compose logs backend

# 重建容器
docker-compose down -v
docker-compose up -d --build
```

### 前端连接超时

```bash
# 检查后端状态
curl http://localhost:5000/health

# 检查Nginx代理配置
sudo nginx -t

# 查看Nginx错误日志
tail -f /var/log/nginx/error.log
```

### 数据库错误

```bash
# 重新初始化
docker-compose exec backend python init_data.py

# 或清除并重建
docker-compose down -v
docker-compose up -d
docker-compose exec backend python init_data.py
```

---

**最后更新**: 2024年1月
