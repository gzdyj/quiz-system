# 🔐 后台管理系统完整指南

## 📱 系统功能概览

刷题系统现在包含完整的**后台管理系统**，支持：

✅ **题库管理** - 添加、编辑、删除题目  
✅ **分类管理** - 管理题目分类  
✅ **用户统计** - 查看用户答题数据  
✅ **数据分析** - 实时统计仪表板  
✅ **账户管理** - 管理员认证和权限  

---

## 🔑 默认登录信息

```
用户名: admin
密码: admin123
```

⚠️ **首次使用后请修改密码！**

---

## 🌐 访问地址

### 前端应用（学生用）
```
http://your-domain.com
```

### 管理后台（管理员用）
```
http://your-domain.com/admin
```

---

## 📊 数据库支持

### 支持的数据库

| 数据库 | 环境 | 连接字符串 |
|--------|------|----------|
| SQLite | 开发/Replit | `sqlite:///questions.db` |
| PostgreSQL | 生产 | `postgresql://user:password@host/db` |

### 环境变量配置

创建 `.env` 文件：

```
FLASK_ENV=production
DATABASE_URL=postgresql://user:password@localhost:5432/quiz_db
SECRET_KEY=your-secret-key-here
```

---

## 📋 管理后台功能详解

### 1️⃣ 仪表板

显示实时统计信息：

- **题目总数** - 系统中所有题目的数量
- **已发布** - 已发布的题目数量
- **总答题数** - 用户答题总数
- **用户数** - 不同用户数量
- **平均正确率** - 所有用户的平均正确率

```
示例:
题目总数: 50
已发布: 48
总答题数: 1,234
用户数: 156
平均正确率: 73.4%
```

### 2️⃣ 题目管理

#### 查看题目列表

- 支持按难度筛选（简单/中等/困难）
- 支持按分类筛选
- 支持搜索题目标题
- 显示题目浏览次数

#### 添加题目

点击 **"+ 添加题目"** 按钮：

```
题目标题: (必填) 题目的完整文字描述
题目描述: (可选) 题目的背景信息
题型: 单选 / 多选
难度: 简单 / 中等 / 困难
分类: 选择或输入分类名称
选项: A、B、C、D 等（自动生成）
正确答案: A 或 A,B,C（多选用逗号分隔）
解析说明: 答题后显示给用户的解析
```

#### 编辑题目

点击题目行的 **"编辑"** 按钮修改任何题目信息。

#### 删除题目

点击 **"删除"** 按钮删除题目（确认后不可恢复）。

### 3️⃣ 分类管理

#### 查看分类

显示所有题目分类卡片。

#### 添加分类

点击 **"+ 添加分类"** 按钮创建新分类。

#### 编辑/删除分类

在分类卡片上直接编辑或删除。

### 4️⃣ 用户统计

显示用户答题统计表格：

| 用户ID | 总答题数 | 正确数 | 错误数 | 正确率 |
|--------|---------|--------|--------|--------|
| user_1234567890 | 25 | 18 | 7 | 72% |
| user_9876543210 | 42 | 31 | 11 | 73.8% |

### 5️⃣ 账户设置

- **查看账户信息** - 用户名、邮箱
- **修改密码** - 输入旧密码和新密码

---

## 🔌 API 接口文档

### 认证相关

#### 登录
```http
POST /admin/api/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}

Response:
{
  "token": "eyJhbGc...",
  "admin": { "id": 1, "username": "admin", ... },
  "expires_in": 86400
}
```

所有其他请求需要在 Header 中添加：
```
Authorization: Bearer <token>
```

### 题目管理

#### 获取题目列表
```http
GET /admin/api/questions?page=1&per_page=20&difficulty=easy&search=题目
```

#### 创建题目
```http
POST /admin/api/questions
Content-Type: application/json
Authorization: Bearer <token>

{
  "title": "题目标题",
  "description": "题目描述",
  "question_type": "single",
  "options": [{"id": "A", "text": "选项A"}, ...],
  "correct_answers": ["A"],
  "difficulty": "easy",
  "category": "分类",
  "explanation": "解析说明",
  "is_published": true
}
```

#### 获取题目详情
```http
GET /admin/api/questions/<id>
Authorization: Bearer <token>
```

#### 更新题目
```http
PUT /admin/api/questions/<id>
Content-Type: application/json
Authorization: Bearer <token>

{ ... 同创建题目 ... }
```

#### 删除题目
```http
DELETE /admin/api/questions/<id>
Authorization: Bearer <token>
```

### 分类管理

#### 获取所有分类
```http
GET /admin/api/categories
```

#### 创建分类
```http
POST /admin/api/categories
Authorization: Bearer <token>

{
  "name": "分类名称",
  "description": "分类描述"
}
```

### 统计相关

#### 获取统计概览
```http
GET /admin/api/statistics/overview
Authorization: Bearer <token>

Response:
{
  "totalQuestions": 50,
  "publishedQuestions": 48,
  "totalAnswers": 1234,
  "totalUsers": 156,
  "accuracy": 73.4,
  "difficultyStats": [
    {"difficulty": "easy", "count": 20},
    ...
  ]
}
```

#### 获取用户统计
```http
GET /admin/api/statistics/users?page=1&per_page=20
Authorization: Bearer <token>
```

---

## 🗄️ 数据库模型

### Question（题目表）

```python
{
    id: Integer,                    # 题目ID
    title: String(500),             # 题目标题
    description: Text,              # 题目描述
    question_type: String,          # single/multiple
    options: JSON,                  # 选项列表
    correct_answers: JSON,          # 正确答案
    explanation: Text,              # 解析说明
    difficulty: String,             # easy/medium/hard
    category: String,               # 分类
    admin_id: Integer,              # 创建者
    is_published: Boolean,          # 是否发布
    view_count: Integer,            # 浏览次数
    created_at: DateTime,           # 创建时间
    updated_at: DateTime            # 更新时间
}
```

### UserAnswer（答题记录表）

```python
{
    id: Integer,
    question_id: Integer,
    user_id: String,
    selected_answers: JSON,
    is_correct: Boolean,
    time_spent: Integer,            # 花费的秒数
    answered_at: DateTime
}
```

### Admin（管理员表）

```python
{
    id: Integer,
    username: String(50),
    password_hash: String,
    email: String,
    is_active: Boolean,
    created_at: DateTime,
    updated_at: DateTime
}
```

### Category（分类表）

```python
{
    id: Integer,
    name: String(100),
    description: Text,
    order: Integer,
    created_at: DateTime
}
```

### UserStatistics（用户统计表）

```python
{
    id: Integer,
    user_id: String,
    total_answers: Integer,
    correct_answers: Integer,
    incorrect_answers: Integer,
    accuracy: Float,
    last_answer_at: DateTime,
    created_at: DateTime,
    updated_at: DateTime
}
```

---

## 🚀 部署到 Replit

### 步骤 1: 更新代码

在 Replit Shell 中运行：

```bash
git pull origin main
```

### 步骤 2: 重启应用

点击 Replit 的 **"Stop"** 然后 **"Run"**

### 步骤 3: 访问管理后台

```
https://your-replit-name.replit.dev/admin
```

默认用户名: `admin`  
默认密码: `admin123`

---

## 🔒 安全建议

### 部署前

1. **修改默认密码**
   ```bash
   # 在 Replit Shell 中
   python3 -c "
   from admin_app import app, db, Admin
   with app.app_context():
       admin = Admin.query.filter_by(username='admin').first()
       admin.set_password('your-strong-password')
       db.session.commit()
   "
   ```

2. **更新 SECRET_KEY**
   - 编辑 `.env` 文件
   - 设置一个随机的 SECRET_KEY

3. **启用 HTTPS**
   - Replit 自动支持 HTTPS
   - 生产环境使用安全的数据库连接

### 日常维护

- 定期备份数据库
- 监控管理员账户
- 审计用户活动
- 及时更新密码

---

## 🐛 常见问题

### Q1: 忘记管理员密码怎么办？

进入 Replit Shell：

```bash
python3 -c "
from admin_app import app, db, Admin
with app.app_context():
    admin = Admin.query.filter_by(username='admin').first()
    admin.set_password('newpassword123')
    db.session.commit()
    print('密码已重置为: newpassword123')
"
```

### Q2: 如何创建新的管理员账户？

在 Replit Shell 中：

```bash
python3 -c "
from admin_app import app, db, Admin
with app.app_context():
    new_admin = Admin(username='newadmin', email='admin@example.com')
    new_admin.set_password('password123')
    db.session.add(new_admin)
    db.session.commit()
    print('创建成功')
"
```

### Q3: 如何导出用户数据？

访问 API 端点：

```
/admin/api/statistics/users?page=1&per_page=1000
```

然后保存 JSON 数据。

### Q4: 如何迁移到 PostgreSQL？

1. 创建 PostgreSQL 数据库
2. 设置 `DATABASE_URL` 环境变量
3. 重启应用（数据库表会自动创建）

---

## 📈 使用场景

### 场景 1: 学校教师

- 创建考试题目库
- 查看学生答题统计
- 分析每道题的难度和正确率
- 调整题目内容

### 场景 2: 在线教育平台

- 管理大量题库
- 按科目/章节分类
- 支持多位教师同时编辑
- 追踪学生学习进度

### 场景 3: 考试培训机构

- 维护培训题库
- 统计学生成绩
- 生成学习报告
- 调整教学内容

---

## 🎉 完成！

现在你拥有一个完整的：

✅ **学生端** - 答题和查看成绩  
✅ **管理员端** - 题库和用户管理  
✅ **数据库** - 持久化存储  
✅ **API** - 可扩展的后端  

开始使用吧！🚀
