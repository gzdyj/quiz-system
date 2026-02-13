# 快速开始指南

本指南帮助你快速启动和使用刷题系统。

## ⚡ 5分钟快速启动

### 前置条件
- 已安装Docker和Docker Compose
- 可用的互联网连接

### 启动步骤

**1. 进入项目目录**
```bash
cd /root/CodeBuddy/20260213173159
```

**2. 启动服务**
```bash
docker-compose up -d
```

**3. 初始化数据库**
```bash
docker-compose exec backend python init_data.py
```

**4. 打开浏览器**
访问: `http://localhost`

✅ **完成！** 系统已启动

---

## 📖 首次使用

### 主要页面

#### 1️⃣ 题目列表页面
- **位置**: 应用首页
- **功能**:
  - 浏览所有可用题目
  - 按难度筛选 (简单/中等/困难)
  - 按题型筛选 (单选/多选)
  - 分页浏览

#### 2️⃣ 答题页面
- **触发**: 点击题目卡片的"查看详情"按钮
- **功能**:
  - 显示完整题目信息
  - 单选或多选选项
  - 提交答题
  - 即时反馈

#### 3️⃣ 成绩统计页面
- **位置**: 导航栏 > 成绩统计
- **功能**:
  - 查看总答题数
  - 查看正确/错误数
  - 查看正确率百分比

---

## 🎯 常见操作

### 答题流程

```
1. 进入系统
   ↓
2. 在题目列表中找到想要的题目
   ↓
3. 点击"查看详情"按钮
   ↓
4. 阅读题目和选项
   ↓
5. 选择答案 (单选用圆圈，多选用方框)
   ↓
6. 点击"提交答案"按钮
   ↓
7. 查看答题结果
   ↓
8. 点击"继续答题"返回列表
```

### 筛选题目

**按难度筛选:**
```
点击"题目筛选" → 选择难度 → 自动刷新
```

**按题型筛选:**
```
点击"题目筛选" → 选择题型 → 自动刷新
```

**分页浏览:**
```
使用底部"上一页"和"下一页"按钮
```

### 查看成绩

```
1. 在导航栏输入用户ID (可选，系统自动生成)
2. 点击"成绩统计"标签
3. 查看统计数据卡片
4. 可以输入其他用户ID查看其成绩
```

---

## 🔧 常用命令

### Docker命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose stop

# 查看日志
docker-compose logs -f

# 查看容器状态
docker-compose ps

# 重启服务
docker-compose restart

# 完全清除（包括数据）
docker-compose down -v
```

### 进入容器

```bash
# 进入后端容器
docker-compose exec backend bash

# 进入前端容器
docker-compose exec frontend bash

# 退出容器
exit
```

### 数据库操作

```bash
# 初始化数据库
docker-compose exec backend python init_data.py

# 备份数据库
docker-compose exec backend cp /data/questions.db /data/backup.db

# 连接数据库（如需直接操作）
sqlite3 /data/questions.db
```

---

## 📝 自定义配置

### 修改端口

编辑 `docker-compose.yml`:
```yaml
frontend:
  ports:
    - "8080:80"  # 改成8080
```

然后重启:
```bash
docker-compose up -d
```

新地址: `http://localhost:8080`

### 修改题目数据

编辑 `backend/init_data.py` 中的 `SAMPLE_QUESTIONS`，然后运行:
```bash
docker-compose exec backend python init_data.py
```

### 修改样式

编辑 `frontend/styles.css` 中的 CSS 变量:
```css
:root {
    --primary-color: #3498db;    /* 改变主色 */
    --success-color: #2ecc71;    /* 改变成功色 */
    --bg-color: #ecf0f1;         /* 改变背景 */
}
```

实时生效（F5刷新即可）。

---

## ❓ 常见问题

### Q: 如何添加更多题目?

**方法1: 编辑init_data.py**
```python
SAMPLE_QUESTIONS = [
    # ... 现有题目 ...
    {
        'title': '新题目标题',
        'description': '题目描述',
        'question_type': 'single',
        'options': [
            {'id': 'A', 'text': '选项A'},
            {'id': 'B', 'text': '选项B'},
        ],
        'correct_answers': ['A'],
        'difficulty': 'easy'
    }
]
```

然后运行: `docker-compose exec backend python init_data.py`

**方法2: 使用API**
```bash
curl -X POST http://localhost:5000/api/admin/questions \
  -H "Content-Type: application/json" \
  -d '{
    "title": "新题目",
    "description": "描述",
    "questionType": "single",
    "options": [{"id": "A", "text": "选项A"}],
    "correctAnswers": ["A"],
    "difficulty": "easy"
  }'
```

### Q: 如何导出用户成绩?

访问: `http://localhost:5000/api/stats/用户ID`

获取JSON格式的统计数据。

### Q: 数据保存在哪里?

所有数据保存在: `/data/questions.db`

该目录被Docker volume挂载，服务停止后数据仍保留。

### Q: 如何重置所有数据?

```bash
# 删除数据卷
docker-compose down -v

# 重新启动并初始化
docker-compose up -d
docker-compose exec backend python init_data.py
```

### Q: 前端无法访问后端?

**检查清单:**
1. 后端容器是否运行: `docker-compose ps`
2. 查看后端日志: `docker-compose logs backend`
3. 测试后端: `curl http://localhost:5000/health`

### Q: 如何修改默认用户ID?

在前端 `app.js` 中修改:
```javascript
let userId = 'my_custom_id';  // 改成你的ID
```

---

## 📚 了解更多

- **完整文档**: 查看 `README.md`
- **API文档**: 查看 `API_EXAMPLES.md`
- **部署指南**: 查看 `DEPLOYMENT.md`
- **架构设计**: 查看 `ARCHITECTURE.md`

---

## 🆘 需要帮助?

### 查看日志获取错误信息
```bash
docker-compose logs -f --tail=50
```

### 测试后端API
```bash
curl http://localhost:5000/health
```

### 检查所有服务状态
```bash
docker-compose ps
```

### 检查网络连接
```bash
docker-compose exec backend ping frontend
```

---

## 📞 快速参考

| 需求 | 命令 |
|------|------|
| 启动系统 | `docker-compose up -d` |
| 停止系统 | `docker-compose stop` |
| 查看日志 | `docker-compose logs -f` |
| 初始化数据 | `docker-compose exec backend python init_data.py` |
| 访问前端 | http://localhost |
| 访问后端API | http://localhost:5000/api |
| 进入后端容器 | `docker-compose exec backend bash` |
| 查看容器状态 | `docker-compose ps` |
| 完全清除 | `docker-compose down -v` |

---

**祝你使用愉快！** 🎉

如有问题，请查阅完整文档或联系技术支持。
