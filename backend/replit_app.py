"""
Replit 统一启动文件 - 同时启动前端和后端
"""
import os
import sys
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# 后端 API 应用
app = Flask(__name__)
CORS(app)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/questions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 数据库模型
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    question_type = db.Column(db.String(20), nullable=False)
    options = db.Column(db.JSON, nullable=False)
    correct_answers = db.Column(db.JSON, nullable=False)
    difficulty = db.Column(db.String(20), default='medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    user_id = db.Column(db.String(100), nullable=False)
    selected_answers = db.Column(db.JSON, nullable=False)
    is_correct = db.Column(db.Boolean)
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)

# 创建表
with app.app_context():
    db.create_all()

# 初始化数据
def init_questions():
    if Question.query.first() is None:
        questions = [
            {
                "title": "以下哪个不是计算机的硬件设备？",
                "description": "计算机硬件是指组成计算机的各种物理设备。",
                "question_type": "single",
                "options": [
                    {"id": "A", "text": "CPU"},
                    {"id": "B", "text": "内存"},
                    {"id": "C", "text": "Windows系统"},
                    {"id": "D", "text": "硬盘"}
                ],
                "correct_answers": ["C"],
                "difficulty": "easy"
            },
            {
                "title": "下列哪些是常见的编程语言？（多选）",
                "description": "编程语言是用于编写计算机程序的形式化语言。",
                "question_type": "multiple",
                "options": [
                    {"id": "A", "text": "Python"},
                    {"id": "B", "text": "JavaScript"},
                    {"id": "C", "text": "中文"},
                    {"id": "D", "text": "Java"}
                ],
                "correct_answers": ["A", "B", "D"],
                "difficulty": "easy"
            },
            {
                "title": "数据库中的主键具有以下哪些特性？（多选）",
                "description": "主键是数据库表中用于唯一标识每条记录的字段。",
                "question_type": "multiple",
                "options": [
                    {"id": "A", "text": "唯一性"},
                    {"id": "B", "text": "非空性"},
                    {"id": "C", "text": "可重复性"},
                    {"id": "D", "text": "自动递增"}
                ],
                "correct_answers": ["A", "B"],
                "difficulty": "medium"
            },
            {
                "title": "下列关于操作系统的说法中，正确的是？",
                "description": "操作系统是管理计算机硬件和软件资源的程序。",
                "question_type": "single",
                "options": [
                    {"id": "A", "text": "操作系统是连接用户和计算机的界面"},
                    {"id": "B", "text": "操作系统只能处理一个任务"},
                    {"id": "C", "text": "操作系统不需要管理内存"},
                    {"id": "D", "text": "所有操作系统都相同"}
                ],
                "correct_answers": ["A"],
                "difficulty": "medium"
            },
            {
                "title": "面向对象编程中的三大特性是？（多选）",
                "description": "这是OOP的核心概念。",
                "question_type": "multiple",
                "options": [
                    {"id": "A", "text": "封装"},
                    {"id": "B", "text": "继承"},
                    {"id": "C", "text": "多态"},
                    {"id": "D", "text": "递归"}
                ],
                "correct_answers": ["A", "B", "C"],
                "difficulty": "medium"
            },
            {
                "title": "以下关于网络协议的描述中，哪个是错误的？",
                "description": "网络协议是一组规则和标准。",
                "question_type": "single",
                "options": [
                    {"id": "A", "text": "TCP协议是面向连接的"},
                    {"id": "B", "text": "UDP协议比TCP协议可靠"},
                    {"id": "C", "text": "HTTP协议运行在TCP之上"},
                    {"id": "D", "text": "IP协议负责路由"}
                ],
                "correct_answers": ["B"],
                "difficulty": "hard"
            },
            {
                "title": "算法的时间复杂度为O(n²)，这意味着什么？",
                "description": "时间复杂度用来估算算法的运行时间。",
                "question_type": "single",
                "options": [
                    {"id": "A", "text": "算法需要n的平方步操作"},
                    {"id": "B", "text": "算法运行时间固定"},
                    {"id": "C", "text": "算法永远不会终止"},
                    {"id": "D", "text": "算法使用n的平方内存"}
                ],
                "correct_answers": ["A"],
                "difficulty": "hard"
            },
            {
                "title": "以下哪些是数据结构？（多选）",
                "description": "数据结构是组织和存储数据的方式。",
                "question_type": "multiple",
                "options": [
                    {"id": "A", "text": "数组"},
                    {"id": "B", "text": "链表"},
                    {"id": "C", "text": "树"},
                    {"id": "D", "text": "字母表"}
                ],
                "correct_answers": ["A", "B", "C"],
                "difficulty": "easy"
            },
            {
                "title": "什么是内存泄漏？",
                "description": "内存管理是程序设计中的重要概念。",
                "question_type": "single",
                "options": [
                    {"id": "A", "text": "程序分配的内存没有被正确释放"},
                    {"id": "B", "text": "内存条损坏"},
                    {"id": "C", "text": "程序运行速度变慢"},
                    {"id": "D", "text": "硬盘空间不足"}
                ],
                "correct_answers": ["A"],
                "difficulty": "medium"
            },
            {
                "title": "以下关于多线程编程的说法中，正确的有？（多选）",
                "description": "多线程是并发编程的重要方式。",
                "question_type": "multiple",
                "options": [
                    {"id": "A", "text": "多线程可以充分利用多核处理器"},
                    {"id": "B", "text": "多线程编程比单线程更简单"},
                    {"id": "C", "text": "多线程需要考虑线程同步问题"},
                    {"id": "D", "text": "线程之间可以共享内存"}
                ],
                "correct_answers": ["A", "C", "D"],
                "difficulty": "hard"
            }
        ]
        
        for q_data in questions:
            q = Question(**q_data)
            db.session.add(q)
        
        db.session.commit()
        print("✅ 初始化 10 道题目完成")

# API 路由

@app.route('/api/questions', methods=['GET'])
def get_questions():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    difficulty = request.args.get('difficulty', None)
    question_type = request.args.get('type', None)
    
    query = Question.query
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if question_type:
        query = query.filter_by(question_type=question_type)
    
    total = query.count()
    pages = (total + per_page - 1) // per_page
    
    questions = query.limit(per_page).offset((page - 1) * per_page).all()
    
    return jsonify({
        'current': page,
        'pages': pages,
        'total': total,
        'data': [{
            'id': q.id,
            'title': q.title,
            'description': q.description,
            'questionType': q.question_type,
            'options': q.options,
            'difficulty': q.difficulty,
            'createdAt': q.created_at.isoformat()
        } for q in questions]
    })

@app.route('/api/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    q = Question.query.get_or_404(question_id)
    return jsonify({
        'id': q.id,
        'title': q.title,
        'description': q.description,
        'questionType': q.question_type,
        'options': q.options,
        'correctAnswers': q.correct_answers,
        'difficulty': q.difficulty,
        'createdAt': q.created_at.isoformat()
    })

@app.route('/api/answers', methods=['POST'])
def submit_answer():
    data = request.get_json()
    
    question = Question.query.get(data['questionId'])
    is_correct = set(data['selectedAnswers']) == set(question.correct_answers)
    
    answer = UserAnswer(
        question_id=data['questionId'],
        user_id=data['userId'],
        selected_answers=data['selectedAnswers'],
        is_correct=is_correct
    )
    db.session.add(answer)
    db.session.commit()
    
    return jsonify({
        'isCorrect': is_correct,
        'correctAnswers': question.correct_answers,
        'selectedAnswers': data['selectedAnswers']
    })

@app.route('/api/stats/<user_id>', methods=['GET'])
def get_stats(user_id):
    answers = UserAnswer.query.filter_by(user_id=user_id).all()
    total = len(answers)
    correct = sum(1 for a in answers if a.is_correct)
    incorrect = total - correct
    accuracy = round(correct * 100 / total, 2) if total > 0 else 0
    
    return jsonify({
        'userId': user_id,
        'total': total,
        'correct': correct,
        'incorrect': incorrect,
        'accuracy': accuracy
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

# 前端路由 - 提供 HTML 文件
FRONTEND_PATH = os.path.join(os.path.dirname(__file__), '..', 'frontend')

@app.route('/')
def index():
    return send_from_directory(FRONTEND_PATH, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    # 避免路由冲突：如果路径以 /api 开头，不处理
    if path.startswith('api'):
        return {'error': 'Not found'}, 404
    return send_from_directory(FRONTEND_PATH, path)

if __name__ == '__main__':
    # 初始化数据
    with app.app_context():
        init_questions()
    
    # 启动服务 - Replit 需要使用 3000 或从环境变量读取
    port = int(os.getenv('PORT', 3000))
    host = os.getenv('HOST', '0.0.0.0')
    print(f"🚀 服务启动在 http://{host}:{port}")
    print(f"📱 访问地址: http://localhost:{port}")
    app.run(host=host, port=port, debug=False)
