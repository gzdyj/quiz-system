# 系统架构设计文档

## 目录
1. [系统概览](#系统概览)
2. [技术栈](#技术栈)
3. [整体架构](#整体架构)
4. [各模块设计](#各模块设计)
5. [数据库设计](#数据库设计)
6. [安全设计](#安全设计)
7. [扩展指南](#扩展指南)

---

## 系统概览

### 项目目标
建立一个完整的在线答题系统，支持计算机科学教育，具有良好的可扩展性和用户体验。

### 核心特性
- **题目管理** - 创建、查看、筛选题目
- **智能答题** - 支持单选、多选、判断等多种题型
- **成绩统计** - 跟踪用户答题情况和成绩
- **用户隔离** - 多用户独立的答题记录

---

## 技术栈

### 后端技术
```
├── 框架: Flask 2.3.3
│   ├── Flask-CORS 4.0.0      # 跨域支持
│   ├── Flask-SQLAlchemy 3.0.5 # ORM框架
│   └── Gunicorn 21.2.0       # 应用服务器
│
├── 数据库: SQLite/PostgreSQL
│   └── SQLAlchemy ORM        # 数据库操作
│
└── 开发: Python 3.11
```

### 前端技术
```
├── HTML5
├── CSS3
│   ├── Flexbox/Grid
│   └── 响应式设计
│
└── JavaScript (ES6+)
    ├── Fetch API
    ├── localStorage
    └── DOM操作
```

### 部署技术
```
├── Docker
│   ├── 后端容器 (Python)
│   └── 前端容器 (Nginx)
│
├── Docker Compose
│   └── 服务编排
│
└── Nginx
    └── 反向代理 + 静态文件服务
```

---

## 整体架构

### C3架构图

```
┌─────────────────────────────────────────────────────┐
│                    用户浏览器                         │
│              (HTML + CSS + JavaScript)               │
└────────────────────┬────────────────────────────────┘
                     │ HTTP/HTTPS
                     ▼
┌─────────────────────────────────────────────────────┐
│                   Nginx (前端)                        │
│  ┌─────────────────────────────────────────────┐   │
│  │ 反向代理 / 静态文件服务 / 代理API请求       │   │
│  └──────────┬──────────────────────────────────┘   │
└─────────────┼──────────────────────────────────────┘
              │ proxy
              ▼
┌─────────────────────────────────────────────────────┐
│              Flask API (后端)                        │
│  ┌──────────────────────────────────────────────┐  │
│  │ • 题目管理接口                                │  │
│  │ • 答题接口                                    │  │
│  │ • 统计接口                                    │  │
│  │ • 用户管理接口                                │  │
│  └──────────┬──────────────────────────────────┘  │
└─────────────┼──────────────────────────────────────┘
              │ ORM
              ▼
┌─────────────────────────────────────────────────────┐
│                  SQLite/PostgreSQL                   │
│  ┌──────────────────────────────────────────────┐  │
│  │ • questions (题目表)                          │  │
│  │ • user_answers (用户答题表)                   │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## 各模块设计

### 后端模块架构

```
backend/
├── app.py                    # 主应用入口
│   ├── models/              # 数据模型层
│   │   ├── Question         # 题目模型
│   │   └── UserAnswer       # 用户答题模型
│   │
│   ├── routes/              # API路由层
│   │   ├── questions        # 题目相关API
│   │   ├── answers          # 答题相关API
│   │   ├── stats            # 统计API
│   │   └── admin            # 管理员API
│   │
│   ├── services/            # 业务逻辑层
│   │   ├── question_service # 题目服务
│   │   ├── answer_service   # 答题服务
│   │   └── stats_service    # 统计服务
│   │
│   └── utils/               # 工具函数
│       ├── validators       # 验证器
│       └── helpers          # 辅助函数
│
└── init_data.py            # 数据初始化脚本
```

### 前端模块架构

```
frontend/
├── index.html              # HTML结构
│   ├── navbar              # 导航栏
│   ├── views               # 多个视图
│   │   ├── questionsView   # 题目列表视图
│   │   ├── answerView      # 答题视图
│   │   └── statsView       # 统计视图
│   └── modal               # 模态框
│
├── styles.css              # 样式
│   ├── 组件样式
│   ├── 布局样式
│   ├── 响应式设计
│   └── CSS变量定义
│
└── app.js                  # 前端逻辑
    ├── 初始化函数
    ├── API调用函数
    ├── 视图切换函数
    ├── 事件处理函数
    └── 工具函数
```

### 数据流

#### 答题数据流
```
1. 用户选择题目
   ↓
2. 前端获取题目详情 (GET /api/questions/{id})
   ↓
3. 显示题目和选项
   ↓
4. 用户选择答案
   ↓
5. 提交答案 (POST /api/answers)
   ↓
6. 后端验证答案正确性
   ↓
7. 保存答题记录到数据库
   ↓
8. 返回答题结果
   ↓
9. 前端显示结果反馈
```

#### 统计查询数据流
```
1. 用户访问统计页面
   ↓
2. 前端获取用户ID
   ↓
3. 查询统计数据 (GET /api/stats/{userId})
   ↓
4. 后端汇总用户答题数据
   ↓
5. 计算统计指标
   ↓
6. 返回统计结果
   ↓
7. 前端显示统计信息
```

---

## 数据库设计

### Question表 (题目表)

```sql
CREATE TABLE question (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    question_type VARCHAR(20) NOT NULL,  -- 'single' 或 'multiple'
    options JSON NOT NULL,               -- 储存选项数组
    correct_answers JSON NOT NULL,       -- 储存正确答案数组
    difficulty VARCHAR(20),              -- 'easy', 'medium', 'hard'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 索引优化查询性能
CREATE INDEX idx_difficulty ON question(difficulty);
CREATE INDEX idx_question_type ON question(question_type);
CREATE INDEX idx_created_at ON question(created_at);
```

**字段说明**

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| id | INTEGER | 是 | 主键，自增 |
| title | VARCHAR(500) | 是 | 题目标题 |
| description | TEXT | 否 | 题目描述/背景 |
| question_type | VARCHAR(20) | 是 | single/multiple |
| options | JSON | 是 | 选项列表 |
| correct_answers | JSON | 是 | 正确答案 |
| difficulty | VARCHAR(20) | 是 | 难度等级 |
| created_at | DATETIME | 是 | 创建时间 |

**options字段示例**
```json
[
  {"id": "A", "text": "选项A内容"},
  {"id": "B", "text": "选项B内容"},
  {"id": "C", "text": "选项C内容"},
  {"id": "D", "text": "选项D内容"}
]
```

### UserAnswer表 (用户答题表)

```sql
CREATE TABLE user_answer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    selected_answers JSON NOT NULL,
    is_correct BOOLEAN,
    answered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY(question_id) REFERENCES question(id)
);

-- 索引优化查询
CREATE INDEX idx_user_id ON user_answer(user_id);
CREATE INDEX idx_question_id ON user_answer(question_id);
CREATE INDEX idx_user_question ON user_answer(user_id, question_id);
CREATE INDEX idx_answered_at ON user_answer(answered_at);
```

**字段说明**

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| id | INTEGER | 是 | 主键，自增 |
| question_id | INTEGER | 是 | 题目ID（外键） |
| user_id | VARCHAR(100) | 是 | 用户标识 |
| selected_answers | JSON | 是 | 用户的选择 |
| is_correct | BOOLEAN | 是 | 是否正确 |
| answered_at | DATETIME | 是 | 答题时间 |

---

## 安全设计

### 输入验证

```python
# 后端应验证：
- 题目ID有效性
- 用户ID格式
- 选择答案的格式
- JSON数据完整性
```

### CORS配置

```python
CORS(app)  # Flask-CORS处理跨域请求
# 生产环境应限制源地址：
CORS(app, origins=['https://yourdomain.com'])
```

### 错误处理

```python
try:
    # 数据库操作
except Exception as e:
    # 记录日志（不暴露详细错误）
    logger.error(str(e))
    # 返回通用错误消息
    return jsonify({'error': 'Internal Server Error'}), 500
```

### 生产环境建议

1. **认证授权**
   - 添加用户认证系统
   - 实现基于角色的权限控制

2. **速率限制**
   - 使用Flask-Limiter限制API请求
   - 防止滥用和DDoS攻击

3. **数据加密**
   - HTTPS通信
   - 敏感数据加密存储

4. **日志审计**
   - 记录所有API访问
   - 监控异常行为

---

## 扩展指南

### 添加新题型

**步骤1**: 修改前端选项组件
```javascript
// frontend/app.js
const inputType = q.questionType === 'judgment' ? 'radio' : 'checkbox';
```

**步骤2**: 修改后端验证逻辑
```python
# backend/app.py
VALID_TYPES = ['single', 'multiple', 'judgment', 'fill-blank']
```

**步骤3**: 更新初始化数据
```python
# backend/init_data.py
{
    'question_type': 'judgment',
    'options': [
        {'id': 'T', 'text': '正确'},
        {'id': 'F', 'text': '错误'}
    ]
}
```

### 添加用户认证

```python
# 安装flask-jwt-extended
pip install flask-jwt-extended

# 在app.py中集成
from flask_jwt_extended import JWTManager, create_access_token

jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    # 验证用户
    access_token = create_access_token(identity=user_id)
    return jsonify(access_token=access_token)

@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    # 只有认证用户可访问
    pass
```

### 集成数据库

#### 从SQLite迁移到PostgreSQL

```python
# 修改环境变量
DATABASE_URL=postgresql://user:password@localhost:5432/quiz_db

# 更新requirements.txt
pip install psycopg2-binary

# 重新初始化
python init_data.py
```

### 添加缓存

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/questions')
@cache.cached(timeout=300)  # 缓存5分钟
def get_questions():
    # ...
```

### 性能监控

```python
from flask import g
import time

@app.before_request
def start_timer():
    g.start = time.time()

@app.after_request
def log_request(response):
    elapsed = time.time() - g.start
    logger.info(f'{request.path} took {elapsed}s')
    return response
```

---

## API设计规范

### RESTful原则

| 操作 | HTTP方法 | 路径 | 示例 |
|------|---------|------|------|
| 查询列表 | GET | /api/questions | GET /api/questions?page=1 |
| 查询单项 | GET | /api/questions/:id | GET /api/questions/1 |
| 创建 | POST | /api/questions | POST /api/questions |
| 更新 | PUT | /api/questions/:id | PUT /api/questions/1 |
| 删除 | DELETE | /api/questions/:id | DELETE /api/questions/1 |

### 响应格式

**成功响应**
```json
{
  "success": true,
  "data": { ... },
  "message": "操作成功"
}
```

**错误响应**
```json
{
  "success": false,
  "error": "error_code",
  "message": "错误描述"
}
```

---

## 部署架构

### 开发环境
```
本地开发 → Flask开发服务器 → SQLite
```

### 生产环境
```
用户 → Nginx (反向代理) → Gunicorn → Flask → PostgreSQL
              ↓
        静态文件服务
```

### 云部署
```
CDN
 ↓
Nginx (负载均衡)
 ↓
Gunicorn Pool (多个实例)
 ↓
数据库集群
```

---

**最后更新**: 2024年1月
