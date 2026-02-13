# 计算机考试刷题系统

一个功能完整的在线刷题平台，支持计算机科学课程的单选和多选题练习。

## 📋 功能特性

### 核心功能
- ✅ **题目浏览** - 分页展示题目列表
- ✅ **智能筛选** - 按难度和题型筛选
- ✅ **在线答题** - 支持单选和多选题
- ✅ **即时反馈** - 答题后立即显示对错和正确答案
- ✅ **成绩统计** - 显示答题数、正确率等统计数据
- ✅ **用户系统** - 支持多用户使用记录

### 技术特性
- 🚀 **现代前端** - 原生HTML/CSS/JavaScript（无框架依赖，快速加载）
- 🔧 **RESTful API** - 标准化的后端接口
- 🐳 **Docker支持** - 一键部署
- 📱 **响应式设计** - 完美支持桌面和移动端

## 🏗️ 项目结构

```
quiz-system/
├── backend/                 # 后端服务
│   ├── app.py              # Flask主应用
│   ├── requirements.txt     # Python依赖
│   ├── Dockerfile          # 后端Docker配置
│   └── init_data.py        # 初始化示例数据
├── frontend/               # 前端服务
│   ├── index.html          # 主页面
│   ├── styles.css          # 样式表
│   ├── app.js              # 前端逻辑
│   ├── Dockerfile          # 前端Docker配置
│   └── nginx.conf          # Nginx配置
├── docker-compose.yml      # Docker编排配置
└── README.md              # 本文件
```

## 🚀 快速开始

### 方式一：使用Docker（推荐）

#### 前置条件
- 已安装 Docker 和 Docker Compose

#### 部署步骤

1. **构建并启动服务**
```bash
docker-compose up -d
```

2. **初始化示例数据**
```bash
# 进入后端容器
docker-compose exec backend bash

# 运行初始化脚本
python init_data.py

# 退出容器
exit
```

3. **访问应用**
- 打开浏览器访问：`http://localhost`
- 后端API：`http://localhost:5000`

#### 查看日志
```bash
docker-compose logs -f
```

#### 停止服务
```bash
docker-compose down
```

### 方式二：本地运行

#### 前置条件
- Python 3.8+
- Node.js（可选，用于开发）

#### 后端启动

1. **安装依赖**
```bash
cd backend
pip install -r requirements.txt
```

2. **初始化数据库**
```bash
python init_data.py
```

3. **启动服务**
```bash
# 开发模式
python app.py

# 生产模式
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

#### 前端启动

1. **使用简单HTTP服务器**
```bash
cd frontend
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000
```

2. **或使用Nginx/Apache等Web服务器**
- 将frontend文件夹中的文件部署到Web服务器的根目录
- 配置代理转发API请求到后端

3. **访问应用**
- 打开浏览器访问：`http://localhost:8000`

## 📚 API文档

### 基础URL
- 本地: `http://localhost:5000/api`
- Docker: `http://backend:5000/api`

### 1. 获取题目列表

**请求**
```
GET /api/questions?page=1&per_page=5&difficulty=medium&type=single
```

**参数**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码（默认1） |
| per_page | int | 否 | 每页条数（默认10） |
| difficulty | string | 否 | 难度：easy/medium/hard |
| type | string | 否 | 题型：single/multiple |

**响应示例**
```json
{
  "data": [
    {
      "id": 1,
      "title": "以下哪个不是计算机的硬件设备？",
      "description": "计算机硬件是指...",
      "questionType": "single",
      "options": [
        {"id": "A", "text": "CPU"},
        {"id": "B", "text": "内存"},
        {"id": "C", "text": "Windows系统"},
        {"id": "D", "text": "硬盘"}
      ],
      "difficulty": "easy",
      "createdAt": "2024-01-01T12:00:00"
    }
  ],
  "total": 100,
  "pages": 10,
  "current": 1
}
```

### 2. 获取单个题目

**请求**
```
GET /api/questions/{questionId}
```

**响应示例**
```json
{
  "id": 1,
  "title": "以下哪个不是计算机的硬件设备？",
  "description": "计算机硬件是指...",
  "questionType": "single",
  "options": [
    {"id": "A", "text": "CPU"},
    {"id": "B", "text": "内存"},
    {"id": "C", "text": "Windows系统"},
    {"id": "D", "text": "硬盘"}
  ],
  "difficulty": "easy"
}
```

### 3. 提交答案

**请求**
```
POST /api/answers
Content-Type: application/json

{
  "questionId": 1,
  "userId": "user_123",
  "selectedAnswers": ["C"]
}
```

**参数说明**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| questionId | int | 是 | 题目ID |
| userId | string | 否 | 用户ID（不提供则为anonymous） |
| selectedAnswers | array | 是 | 选中的答案ID列表 |

**响应示例**
```json
{
  "answerId": 1,
  "isCorrect": true,
  "correctAnswers": ["C"],
  "message": "回答正确！"
}
```

### 4. 获取用户统计

**请求**
```
GET /api/stats/{userId}
```

**响应示例**
```json
{
  "userId": "user_123",
  "total": 25,
  "correct": 20,
  "incorrect": 5,
  "accuracy": 80.0
}
```

### 5. 创建题目（管理员）

**请求**
```
POST /api/admin/questions
Content-Type: application/json

{
  "title": "题目标题",
  "description": "题目描述",
  "questionType": "single",
  "options": [
    {"id": "A", "text": "选项A"},
    {"id": "B", "text": "选项B"},
    {"id": "C", "text": "选项C"},
    {"id": "D", "text": "选项D"}
  ],
  "correctAnswers": ["A"],
  "difficulty": "easy"
}
```

**响应示例**
```json
{
  "id": 1,
  "message": "题目创建成功"
}
```

### 6. 删除题目（管理员）

**请求**
```
DELETE /api/admin/questions/{questionId}
```

**响应示例**
```json
{
  "message": "题目已删除"
}
```

## 🎨 前端功能说明

### 页面导航
- **题目列表** - 浏览所有题目
- **成绩统计** - 查看个人成绩
- **用户ID** - 输入或生成用户ID

### 题目列表视图
- 题目分页展示
- 按难度筛选（简单/中等/困难）
- 按题型筛选（单选/多选）
- 快速查看题目详情

### 答题界面
- 显示题目详情
- 单选或多选选项
- 即时答题反馈
- 显示正确答案

### 统计信息
- 总答题数
- 正确题数
- 错误题数
- 正确率百分比

## 💾 数据库说明

### 表结构

#### Question表
```sql
CREATE TABLE question (
  id INTEGER PRIMARY KEY,
  title VARCHAR(500) NOT NULL,
  description TEXT,
  question_type VARCHAR(20) NOT NULL,  -- 'single' 或 'multiple'
  options JSON NOT NULL,               -- [{"id": "A", "text": "..."}, ...]
  correct_answers JSON NOT NULL,       -- ["A"] 或 ["A", "B"]
  difficulty VARCHAR(20) DEFAULT 'medium', -- 'easy', 'medium', 'hard'
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### UserAnswer表
```sql
CREATE TABLE user_answer (
  id INTEGER PRIMARY KEY,
  question_id INTEGER FOREIGN KEY,
  user_id VARCHAR(100) NOT NULL,
  selected_answers JSON NOT NULL,     -- 用户选择的答案
  is_correct BOOLEAN,                 -- 答案是否正确
  answered_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 环境配置

### 后端环境变量
```env
DATABASE_URL=sqlite:////data/questions.db    # 数据库URL
FLASK_ENV=production                         # Flask环境
```

### Docker环境配置
```yaml
# docker-compose.yml 中配置

backend:
  environment:
    - FLASK_ENV=production
    - DATABASE_URL=sqlite:////data/questions.db
```

## 📝 开发指南

### 添加新题目

**方法1：使用API**
```bash
curl -X POST http://localhost:5000/api/admin/questions \
  -H "Content-Type: application/json" \
  -d '{
    "title": "什么是算法？",
    "description": "算法是解决问题的步骤序列",
    "questionType": "single",
    "options": [
      {"id": "A", "text": "解决问题的步骤"},
      {"id": "B", "text": "编程语言"},
      {"id": "C", "text": "计算机硬件"},
      {"id": "D", "text": "操作系统"}
    ],
    "correctAnswers": ["A"],
    "difficulty": "easy"
  }'
```

**方法2：修改init_data.py**
在 `SAMPLE_QUESTIONS` 列表中添加新题目数据，然后运行：
```bash
python backend/init_data.py
```

### 自定义样式
编辑 `frontend/styles.css` 中的CSS变量：
```css
:root {
    --primary-color: #3498db;        /* 主色 */
    --success-color: #2ecc71;        /* 成功色 */
    --danger-color: #e74c3c;         /* 危险色 */
    --bg-color: #ecf0f1;             /* 背景色 */
}
```

### 修改后端API
在 `backend/app.py` 中修改路由和业务逻辑

### 修改前端UI
编辑以下文件：
- `frontend/index.html` - HTML结构
- `frontend/styles.css` - 样式
- `frontend/app.js` - 交互逻辑

## 🐛 常见问题

### Q1: 数据库错误
**症状**: `DatabaseError: no such table`

**解决方案**:
```bash
# 使用Docker时
docker-compose exec backend python init_data.py

# 本地运行时
cd backend
python init_data.py
```

### Q2: API请求失败 (CORS错误)
**症状**: `Access to XMLHttpRequest blocked by CORS policy`

**解决方案**: 
- 已在后端启用CORS，如问题依旧，检查代理配置
- 在Docker中确保nginx.conf正确配置了代理

### Q3: 端口已被占用
**症状**: `Address already in use`

**解决方案**:
```bash
# 修改docker-compose.yml的端口映射
# 或 kill现有进程
lsof -i :5000  # 查看占用端口的进程
kill -9 <PID>  # 杀死进程
```

### Q4: 前端无法访问后端API
**症状**: 请求超时或404错误

**解决方案**:
- 确保后端容器运行正常
- 检查nginx.conf中的proxy_pass配置
- 查看浏览器开发者工具中的网络标签

## 📊 性能优化建议

### 前端优化
- 实现虚拟列表处理大量题目
- 添加缓存减少API调用
- 使用WebWorker处理复杂计算

### 后端优化
- 添加数据库查询索引
- 实现Redis缓存
- 使用连接池管理数据库

### 部署优化
- 使用CDN加速静态文件
- 配置gzip压缩
- 使用负载均衡器

## 🔐 安全建议

### 生产环境检查清单
- [ ] 启用HTTPS
- [ ] 添加用户认证
- [ ] 实现API速率限制
- [ ] 验证所有用户输入
- [ ] 定期备份数据库
- [ ] 隐藏错误详情信息
- [ ] 更新依赖包版本

## 📦 依赖版本

### 后端依赖
- Flask 2.3.3
- Flask-CORS 4.0.0
- Flask-SQLAlchemy 3.0.5
- Python 3.11

### 前端
- 原生JavaScript（无框架依赖）
- CSS3
- HTML5

## 📜 许可证

MIT License

## 👥 贡献指南

欢迎提交Issue和Pull Request！

## 📞 技术支持

如有问题，请查看：
1. 本README中的"常见问题"部分
2. 查看应用日志 (`docker-compose logs`)
3. 检查浏览器开发者工具

---

**最后更新**: 2024年1月
**版本**: 1.0.0
