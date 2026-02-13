# 🚀 Replit 部署指南

本指南帮助你在 Replit 上免费部署刷题系统。

## 📋 前置条件

- GitHub 账号（已有）
- Replit 账号（免费注册：https://replit.com）

## 🎯 部署步骤

### 步骤 1: 打开 Replit

访问 https://replit.com 并登录

### 步骤 2: 从 GitHub 导入项目

1. 点击右上角 **"+"** 按钮或 **"Create"**
2. 选择 **"Import from GitHub"**
3. 粘贴仓库地址：
   ```
   https://github.com/gzdyj/quiz-system
   ```
4. 点击 **"Import"** 并等待导入完成

### 步骤 3: 自动启动

项目会自动识别 `.replit` 配置文件并启动：

- Replit 会检测项目结构
- 自动运行 `cd backend && python3 replit_app.py`
- 依赖会自动安装

### 步骤 4: 获取访问地址

项目启动后，Replit 会显示：

```
🚀 Your app is live at: https://YOUR_REPLIT_USERNAME-quiz-system.replit.dev
```

复制这个地址就可以访问了！

---

## ✅ 部署完成

访问生成的链接即可查看系统：

```
https://YOUR_REPLIT_USERNAME-quiz-system.replit.dev
```

---

## 🎨 系统功能

部署后，你可以：

✅ 浏览 10 道初始题目  
✅ 按难度和题型筛选题目  
✅ 完成单选和多选题  
✅ 查看答题反馈和解析  
✅ 查看成绩统计  
✅ 多用户独立统计  

---

## 🔧 访问后端 API

部署后可以直接访问 API：

```bash
# 获取题目列表
curl https://YOUR_REPLIT_USERNAME-quiz-system.replit.dev/api/questions

# 获取单个题目
curl https://YOUR_REPLIT_USERNAME-quiz-system.replit.dev/api/questions/1

# 获取用户统计
curl https://YOUR_REPLIT_USERNAME-quiz-system.replit.dev/api/stats/user123

# 健康检查
curl https://YOUR_REPLIT_USERNAME-quiz-system.replit.dev/health
```

---

## 💡 常见问题

### Q1: 项目启动失败？
**解决**: 
- 检查 `.replit` 文件是否正确
- 查看 Replit 的控制台输出
- 确保 `backend/replit_app.py` 文件存在

### Q2: 前端无法连接后端？
**解决**:
- 系统已自动配置，前端会自动连接到正确的后端地址
- 检查浏览器控制台是否有错误信息

### Q3: 数据会保存吗？
**解决**:
- Replit 免费版本的数据存储在内存中
- 项目重启时数据会重置
- 如需持久化存储，可升级为付费版本

### Q4: 可以自定义题目吗？
**解决**:
- 编辑 `backend/replit_app.py` 中的 `questions` 变量
- 保存后项目会自动重启并加载新题目

---

## 📚 项目结构

```
quiz-system/
├── .replit                 # Replit 配置
├── backend/
│   ├── replit_app.py       # 统一应用（同时托管前后端）
│   ├── requirements.txt     # Python 依赖
│   ├── app.py              # 原始后端应用
│   └── init_data.py        # 数据初始化
├── frontend/
│   ├── index.html          # 前端页面
│   ├── app.js              # 前端逻辑
│   └── styles.css          # 样式表
└── 其他文件...
```

---

## 🌐 部署架构

```
用户 (浏览器)
    ↓
Replit 域名
    ↓
Flask 应用 (replit_app.py)
    ├─ 前端路由: /
    ├─ API 路由: /api/...
    └─ 静态文件: /*.css, /*.js
    ↓
SQLite 数据库 (/tmp/questions.db)
```

---

## 🔗 相关链接

- **GitHub 仓库**: https://github.com/gzdyj/quiz-system
- **Replit**: https://replit.com
- **部署后地址**: https://YOUR_REPLIT_USERNAME-quiz-system.replit.dev

---

## 🎉 完成！

你的刷题系统现在已在 Replit 上免费运行！

分享这个链接给朋友体验：
```
https://YOUR_REPLIT_USERNAME-quiz-system.replit.dev
```

---

## 💡 升级选项（可选）

如果需要更多功能：

1. **Replit Hacker 套餐** - $7/月
   - 无限 CPU 和内存
   - 优先级队列
   - 无编辑器限制

2. **添加数据库** - 使用 PostgreSQL（可选）
   - 修改 `replit_app.py` 中的数据库连接
   - 数据持久化存储

3. **自定义域名** - 指向 Replit 应用

---

祝你使用愉快！🚀
