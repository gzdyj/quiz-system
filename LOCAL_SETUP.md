# 🖥️ 本地开发运行指南

本指南帮助你在本地计算机上运行刷题系统。

## 前置要求

### 选项 A: 使用 Docker（推荐）
- **Docker**: https://docs.docker.com/get-docker/
- **Docker Compose**: https://docs.docker.com/compose/install/

### 选项 B: 直接运行
- **Python 3.8+**: https://www.python.org/downloads/
- **Node.js**（可选，用于简单 HTTP 服务）

---

## 🚀 方案 1：Docker 方式（推荐 - 完整生产环境）

### 步骤 1: 安装 Docker

**Windows/Mac/Linux** - 访问 https://www.docker.com/products/docker-desktop 下载安装

验证安装：
```bash
docker --version
docker-compose --version
```

### 步骤 2: 克隆或下载项目

```bash
# 克隆 GitHub 仓库
git clone https://github.com/gzdyj/quiz-system.git
cd quiz-system
```

### 步骤 3: 启动服务

```bash
# 启动所有服务（后端 + 前端）
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 步骤 4: 初始化数据库

```bash
# 在后端容器中运行初始化脚本
docker-compose exec backend python init_data.py
```

### 步骤 5: 访问应用

打开浏览器访问：
```
http://localhost
```

### 停止服务

```bash
# 停止但保留数据
docker-compose stop

# 停止并删除所有数据
docker-compose down -v

# 重启服务
docker-compose restart
```

---

## 🚀 方案 2：直接运行（快速体验）

### 步骤 1: 安装 Python

确保你已安装 Python 3.8 或更高版本。验证：
```bash
python --version
# 或
python3 --version
```

### 步骤 2: 克隆项目

```bash
git clone https://github.com/gzdyj/quiz-system.git
cd quiz-system
```

### 步骤 3: 启动后端

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt
# 或
pip3 install -r requirements.txt

# 初始化数据库
python init_data.py

# 启动 Flask 服务
python app.py
```

后端应该在 `http://localhost:5000` 运行

### 步骤 4: 启动前端（新终端）

```bash
# 进入前端目录
cd frontend

# 方式 A: Python HTTP 服务器
python -m http.server 8000
# 或
python3 -m http.server 8000

# 方式 B: 如果你有 Node.js
npx http-server
```

前端应该在 `http://localhost:8000` 运行

### 步骤 5: 打开浏览器

访问：
```
http://localhost:8000
```

---

## 📱 使用应用

### 1️⃣ 首页 - 题目列表
- 查看所有可用题目
- 使用筛选器按难度或题型筛选
- 点击"查看详情"进入答题页面

### 2️⃣ 答题页面
- 阅读题目内容
- 选择答案
- 提交答案查看是否正确
- 查看解析

### 3️⃣ 成绩页面
- 查看答题统计
- 查看正确率
- 查看答题历史

---

## 🔧 环境变量配置

创建 `backend/.env` 文件（可选）：

```
FLASK_ENV=development
DATABASE_URL=sqlite:///questions.db
DEBUG=True
```

---

## 📊 API 测试

### 获取题目列表
```bash
curl http://localhost:5000/api/questions
```

### 获取单个题目
```bash
curl http://localhost:5000/api/questions/1
```

### 提交答案
```bash
curl -X POST http://localhost:5000/api/answers \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "question_id": 1,
    "selected_options": ["A"]
  }'
```

### 获取用户统计
```bash
curl http://localhost:5000/api/stats/user123
```

详细见 `API_EXAMPLES.md`

---

## ❌ 常见问题

### Q1: "ModuleNotFoundError: No module named 'flask'"
**解决**: 确保已安装依赖
```bash
pip install -r requirements.txt
```

### Q2: "port already in use"
**解决**: 更改端口
```bash
# 后端
python app.py  # 改为其他端口
# 或修改 app.py 中的 port=5001

# 前端
python -m http.server 9000  # 改为 9000
```

### Q3: 前端无法连接到后端
**解决**: 
1. 确保后端已启动
2. 检查 `frontend/app.js` 中的 API 地址是否正确
3. 确保 CORS 已启用（已在 Flask 中配置）

### Q4: 数据库错误
**解决**: 删除旧数据库并重新初始化
```bash
cd backend
rm -f questions.db  # 删除旧数据库
python init_data.py  # 重新初始化
```

---

## 📁 项目结构

```
quiz-system/
├── backend/
│   ├── app.py           # Flask 应用主文件
│   ├── init_data.py     # 数据初始化脚本
│   ├── requirements.txt  # Python 依赖
│   ├── Dockerfile       # Docker 配置
│   └── .env             # 环境变量（可选）
├── frontend/
│   ├── index.html       # HTML 页面
│   ├── app.js          # JavaScript 逻辑
│   ├── styles.css      # 样式表
│   ├── Dockerfile      # Docker 配置
│   └── nginx.conf      # Nginx 配置
├── docker-compose.yml   # Docker Compose 编排
└── 文档文件...
```

---

## 🎯 开发流程

### 修改后端代码
1. 修改 `backend/app.py`
2. 重启后端服务：`docker-compose restart backend` 或重新运行 `python app.py`
3. 测试新功能

### 修改前端代码
1. 修改 `frontend/index.html/app.js/styles.css`
2. 刷新浏览器即可看到改动（无需重启）

### 添加新题目
修改 `backend/init_data.py` 并重新运行：
```bash
docker-compose exec backend python init_data.py
```

---

## 📚 更多资源

- **完整文档**: 查看 `README.md`
- **API 文档**: 查看 `API_EXAMPLES.md`
- **架构设计**: 查看 `ARCHITECTURE.md`
- **部署指南**: 查看 `DEPLOYMENT.md`

---

## ✅ 验证安装

启动后，验证所有服务正常运行：

```bash
# 1. 检查后端健康状态
curl http://localhost:5000/health

# 2. 检查前端是否可访问
curl http://localhost:8000/  # 直接运行方式
# 或
curl http://localhost/       # Docker 方式

# 3. 检查 API 是否工作
curl http://localhost:5000/api/questions
```

---

## 🎉 完成！

现在你可以：
✅ 浏览题目列表
✅ 进行答题练习
✅ 查看成绩统计
✅ 体验完整系统

祝你使用愉快！🚀
