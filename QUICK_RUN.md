# ⚡ 一键快速启动（仅需 3 步）

## 🎯 场景 1: 有 Docker（推荐）

如果你的电脑已安装 Docker 和 Docker Compose：

```bash
# 1. 克隆项目
git clone https://github.com/gzdyj/quiz-system.git
cd quiz-system

# 2. 启动服务
docker-compose up -d

# 3. 初始化数据
docker-compose exec backend python init_data.py

# ✅ 打开浏览器访问 http://localhost
```

**停止服务**:
```bash
docker-compose down
```

---

## 🎯 场景 2: 仅有 Python（直接运行）

### 终端 1 - 启动后端

```bash
git clone https://github.com/gzdyj/quiz-system.git
cd quiz-system/backend

pip install -r requirements.txt
python init_data.py
python app.py
```

后端运行在 `http://localhost:5000`

### 终端 2 - 启动前端

```bash
cd quiz-system/frontend
python -m http.server 8000
```

前端运行在 `http://localhost:8000`

### 打开浏览器访问

```
http://localhost:8000
```

---

## 🎯 场景 3: 完全从零开始（包含所有依赖）

### Windows 用户

```batch
REM 1. 安装 Python 3.9+（从 https://www.python.org/downloads/ 下载）

REM 2. 克隆项目
git clone https://github.com/gzdyj/quiz-system.git
cd quiz-system

REM 3. 创建虚拟环境
python -m venv venv
venv\Scripts\activate

REM 4. 启动后端（在命令行窗口 1）
cd backend
pip install -r requirements.txt
python init_data.py
python app.py

REM 5. 启动前端（在命令行窗口 2）
cd frontend
python -m http.server 8000

REM 6. 打开浏览器访问 http://localhost:8000
```

### Mac/Linux 用户

```bash
# 1. 确保已安装 Python 3.8+
python3 --version

# 2. 克隆项目
git clone https://github.com/gzdyj/quiz-system.git
cd quiz-system

# 3. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 4. 启动后端（在终端 1）
cd backend
pip install -r requirements.txt
python init_data.py
python app.py

# 5. 启动前端（在终端 2）
cd frontend
python3 -m http.server 8000

# 6. 打开浏览器访问 http://localhost:8000
```

---

## 📱 系统功能演示

### 首页 - 题目列表
- ✅ 显示 10 道初始题目
- ✅ 支持按难度筛选（简单/中等/困难）
- ✅ 支持按题型筛选（单选/多选）
- ✅ 分页浏览

### 答题页面
- ✅ 阅读题目内容
- ✅ 选择答案
- ✅ 提交答案
- ✅ 查看是否正确
- ✅ 显示解析

### 成绩统计
- ✅ 总答题数
- ✅ 正确数/错误数
- ✅ 正确率百分比
- ✅ 多用户独立统计

---

## 🐛 遇到问题？

### Python 版本错误
```bash
# 确保使用 Python 3.8+
python3 --version
# 或
python --version
```

### 端口被占用
```bash
# 改用其他端口
python -m http.server 9000  # 用 9000 而不是 8000
```

### 模块未找到
```bash
# 重新安装依赖
pip install -r requirements.txt
# 或使用 pip3
pip3 install -r requirements.txt
```

### 前端无法连接后端
1. 确保后端已启动（`python app.py` 已运行）
2. 检查后端运行地址（应显示 `Running on http://127.0.0.1:5000`）
3. 检查前端 `app.js` 中的 API 地址配置

---

## 📖 完整文档

需要更多详情？查看完整的本地设置指南：

**查看**: `LOCAL_SETUP.md`

---

## 🎉 完成！

现在你可以：
- 🎯 浏览和筛选题目
- 📝 完成答题练习
- 📊 查看成绩统计
- 🎨 体验完整的 UI/UX

祝你使用愉快！🚀
