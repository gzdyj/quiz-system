# API使用示例

本文档提供完整的API调用示例。

## 前提条件

- 后端服务已启动 (`http://localhost:5000`)
- 已初始化数据库

## cURL示例

### 1. 获取题目列表

**基础请求**
```bash
curl -X GET "http://localhost:5000/api/questions"
```

**带筛选条件**
```bash
# 获取简单难度的单选题
curl -X GET "http://localhost:5000/api/questions?difficulty=easy&type=single"

# 分页查询（第2页，每页5条）
curl -X GET "http://localhost:5000/api/questions?page=2&per_page=5"
```

**完整示例**
```bash
curl -X GET "http://localhost:5000/api/questions?page=1&per_page=10&difficulty=medium&type=multiple" \
  -H "Content-Type: application/json"
```

### 2. 获取单个题目

```bash
curl -X GET "http://localhost:5000/api/questions/1"
```

### 3. 提交答案

**单选题答案**
```bash
curl -X POST "http://localhost:5000/api/answers" \
  -H "Content-Type: application/json" \
  -d '{
    "questionId": 1,
    "userId": "student_001",
    "selectedAnswers": ["C"]
  }'
```

**多选题答案**
```bash
curl -X POST "http://localhost:5000/api/answers" \
  -H "Content-Type: application/json" \
  -d '{
    "questionId": 2,
    "userId": "student_001",
    "selectedAnswers": ["A", "B", "D"]
  }'
```

### 4. 获取用户统计

```bash
curl -X GET "http://localhost:5000/api/stats/student_001"
```

### 5. 创建题目（管理员）

```bash
curl -X POST "http://localhost:5000/api/admin/questions" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "什么是面向对象编程？",
    "description": "OOP是一种编程范式，强调对象的概念",
    "questionType": "single",
    "options": [
      {"id": "A", "text": "一种编程范式"},
      {"id": "B", "text": "一种编程语言"},
      {"id": "C", "text": "一种数据库"},
      {"id": "D", "text": "一种操作系统"}
    ],
    "correctAnswers": ["A"],
    "difficulty": "easy"
  }'
```

### 6. 删除题目

```bash
curl -X DELETE "http://localhost:5000/api/admin/questions/1"
```

### 7. 健康检查

```bash
curl -X GET "http://localhost:5000/health"
```

---

## Python requests示例

### 安装requests库
```bash
pip install requests
```

### 示例脚本

```python
import requests
import json

BASE_URL = "http://localhost:5000/api"

# 1. 获取题目列表
def get_questions(page=1, per_page=10):
    response = requests.get(
        f"{BASE_URL}/questions",
        params={
            "page": page,
            "per_page": per_page
        }
    )
    return response.json()

# 2. 获取单个题目
def get_question(question_id):
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    return response.json()

# 3. 提交答案
def submit_answer(question_id, user_id, selected_answers):
    response = requests.post(
        f"{BASE_URL}/answers",
        json={
            "questionId": question_id,
            "userId": user_id,
            "selectedAnswers": selected_answers
        }
    )
    return response.json()

# 4. 获取用户统计
def get_stats(user_id):
    response = requests.get(f"{BASE_URL}/stats/{user_id}")
    return response.json()

# 5. 创建题目
def create_question(data):
    response = requests.post(
        f"{BASE_URL}/admin/questions",
        json=data
    )
    return response.json()

# 使用示例
if __name__ == "__main__":
    # 获取题目
    questions = get_questions()
    print("题目列表:")
    print(json.dumps(questions, indent=2, ensure_ascii=False))
    
    # 答题
    if questions["data"]:
        q = questions["data"][0]
        result = submit_answer(q["id"], "user_123", ["A"])
        print("\n答题结果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 查看统计
    stats = get_stats("user_123")
    print("\n用户统计:")
    print(json.dumps(stats, indent=2, ensure_ascii=False))
```

---

## JavaScript/Fetch示例

### 获取题目列表
```javascript
async function getQuestions() {
    try {
        const response = await fetch('http://localhost:5000/api/questions');
        const data = await response.json();
        console.log(data);
        return data;
    } catch (error) {
        console.error('Error:', error);
    }
}

getQuestions();
```

### 提交答案
```javascript
async function submitAnswer(questionId, userId, selectedAnswers) {
    try {
        const response = await fetch('http://localhost:5000/api/answers', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                questionId: questionId,
                userId: userId,
                selectedAnswers: selectedAnswers
            })
        });
        const data = await response.json();
        console.log(data);
        return data;
    } catch (error) {
        console.error('Error:', error);
    }
}

submitAnswer(1, 'student_001', ['C']);
```

### 获取用户统计
```javascript
async function getUserStats(userId) {
    try {
        const response = await fetch(`http://localhost:5000/api/stats/${userId}`);
        const data = await response.json();
        console.log(data);
        return data;
    } catch (error) {
        console.error('Error:', error);
    }
}

getUserStats('student_001');
```

---

## Postman示例

### 导入集合

创建 `postman_collection.json`:

```json
{
  "info": {
    "name": "刷题系统API",
    "description": "计算机刷题系统API集合",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "获取题目列表",
      "request": {
        "method": "GET",
        "url": {
          "raw": "http://localhost:5000/api/questions?page=1&per_page=10",
          "protocol": "http",
          "host": ["localhost"],
          "port": "5000",
          "path": ["api", "questions"],
          "query": [
            {"key": "page", "value": "1"},
            {"key": "per_page", "value": "10"},
            {"key": "difficulty", "value": "easy", "disabled": true},
            {"key": "type", "value": "single", "disabled": true}
          ]
        }
      }
    },
    {
      "name": "提交答案",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "url": {
          "raw": "http://localhost:5000/api/answers",
          "protocol": "http",
          "host": ["localhost"],
          "port": "5000",
          "path": ["api", "answers"]
        },
        "body": {
          "mode": "raw",
          "raw": "{\n  \"questionId\": 1,\n  \"userId\": \"student_001\",\n  \"selectedAnswers\": [\"C\"]\n}"
        }
      }
    },
    {
      "name": "获取用户统计",
      "request": {
        "method": "GET",
        "url": {
          "raw": "http://localhost:5000/api/stats/student_001",
          "protocol": "http",
          "host": ["localhost"],
          "port": "5000",
          "path": ["api", "stats", "student_001"]
        }
      }
    }
  ]
}
```

### 导入步骤
1. 打开Postman
2. 点击 "Import"
3. 选择JSON文件或直接粘贴内容
4. 开始测试

---

## 响应示例

### 获取题目列表响应
```json
{
  "data": [
    {
      "id": 1,
      "title": "以下哪个不是计算机的硬件设备？",
      "description": "计算机硬件是指组成计算机的各种物理设备。",
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

### 答题结果响应
```json
{
  "answerId": 1,
  "isCorrect": true,
  "correctAnswers": ["C"],
  "message": "回答正确！"
}
```

### 用户统计响应
```json
{
  "userId": "student_001",
  "total": 25,
  "correct": 20,
  "incorrect": 5,
  "accuracy": 80.0
}
```

---

## 测试脚本

### 批量测试脚本 (Python)

```python
import requests
import time

BASE_URL = "http://localhost:5000/api"

def test_api():
    print("开始测试API...")
    
    # 测试1: 获取题目
    print("\n[测试1] 获取题目列表")
    try:
        response = requests.get(f"{BASE_URL}/questions?per_page=3")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        print(f"✓ 成功获取 {len(data['data'])} 道题目")
    except Exception as e:
        print(f"✗ 失败: {e}")
        return False
    
    # 测试2: 获取单个题目
    print("\n[测试2] 获取单个题目")
    try:
        question_id = data["data"][0]["id"]
        response = requests.get(f"{BASE_URL}/questions/{question_id}")
        assert response.status_code == 200
        question = response.json()
        print(f"✓ 成功获取题目: {question['title']}")
    except Exception as e:
        print(f"✗ 失败: {e}")
        return False
    
    # 测试3: 提交答案
    print("\n[测试3] 提交答案")
    try:
        payload = {
            "questionId": question_id,
            "userId": "test_user",
            "selectedAnswers": question["options"][:1]
        }
        response = requests.post(f"{BASE_URL}/answers", json=payload)
        assert response.status_code == 201
        result = response.json()
        print(f"✓ 答案已提交: {result['message']}")
    except Exception as e:
        print(f"✗ 失败: {e}")
        return False
    
    # 测试4: 获取统计
    print("\n[测试4] 获取用户统计")
    try:
        response = requests.get(f"{BASE_URL}/stats/test_user")
        assert response.status_code == 200
        stats = response.json()
        print(f"✓ 用户统计: 总数{stats['total']}, 正确{stats['correct']}, 正确率{stats['accuracy']}%")
    except Exception as e:
        print(f"✗ 失败: {e}")
        return False
    
    print("\n✓ 所有测试通过！")
    return True

if __name__ == "__main__":
    test_api()
```

运行测试:
```bash
python test_api.py
```

---

## 常见错误处理

### 错误: 404 Not Found
```
问题: 题目不存在
解决: 检查题目ID是否正确，运行初始化脚本
```

### 错误: 422 Unprocessable Entity
```
问题: 请求数据格式错误
解决: 检查JSON格式，确保所有必需字段都已提供
```

### 错误: CORS 错误
```
问题: 跨域请求被阻止
解决: 后端已配置CORS，如问题依旧，检查浏览器控制台
```

### 错误: 数据库错误
```
问题: "no such table" 或类似错误
解决: 运行初始化脚本: docker-compose exec backend python init_data.py
```

---

**最后更新**: 2024年1月
