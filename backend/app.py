from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///questions.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 数据库模型
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    question_type = db.Column(db.String(20), nullable=False)  # single, multiple
    options = db.Column(db.JSON, nullable=False)  # [{"id": "A", "text": "..."}, ...]
    correct_answers = db.Column(db.JSON, nullable=False)  # ["A"] 或 ["A", "B"]
    difficulty = db.Column(db.String(20), default='medium')  # easy, medium, hard
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    user_id = db.Column(db.String(100), nullable=False)
    selected_answers = db.Column(db.JSON, nullable=False)  # ["A"] 或 ["A", "B"]
    is_correct = db.Column(db.Boolean)
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)

# 创建表
with app.app_context():
    db.create_all()

# API 路由

# 1. 获取所有题目
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
    
    pagination = query.paginate(page=page, per_page=per_page)
    
    questions = []
    for q in pagination.items:
        questions.append({
            'id': q.id,
            'title': q.title,
            'description': q.description,
            'questionType': q.question_type,
            'options': q.options,
            'difficulty': q.difficulty,
            'createdAt': q.created_at.isoformat()
        })
    
    return jsonify({
        'data': questions,
        'total': pagination.total,
        'pages': pagination.pages,
        'current': page
    })

# 2. 获取单个题目
@app.route('/api/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    question = Question.query.get_or_404(question_id)
    return jsonify({
        'id': question.id,
        'title': question.title,
        'description': question.description,
        'questionType': question.question_type,
        'options': question.options,
        'difficulty': question.difficulty
    })

# 3. 提交答案
@app.route('/api/answers', methods=['POST'])
def submit_answer():
    data = request.json
    question_id = data.get('questionId')
    user_id = data.get('userId', 'anonymous')
    selected_answers = data.get('selectedAnswers', [])
    
    question = Question.query.get_or_404(question_id)
    
    # 检查答案是否正确
    correct_answers = set(question.correct_answers)
    selected_set = set(selected_answers)
    is_correct = correct_answers == selected_set
    
    # 保存用户答案
    user_answer = UserAnswer(
        question_id=question_id,
        user_id=user_id,
        selected_answers=selected_answers,
        is_correct=is_correct
    )
    db.session.add(user_answer)
    db.session.commit()
    
    return jsonify({
        'answerId': user_answer.id,
        'isCorrect': is_correct,
        'correctAnswers': question.correct_answers,
        'message': '回答正确！' if is_correct else '回答错误，请查看正确答案。'
    }), 201

# 4. 获取用户答题统计
@app.route('/api/stats/<user_id>', methods=['GET'])
def get_stats(user_id):
    user_answers = UserAnswer.query.filter_by(user_id=user_id).all()
    
    total = len(user_answers)
    correct = sum(1 for a in user_answers if a.is_correct)
    accuracy = (correct / total * 100) if total > 0 else 0
    
    return jsonify({
        'userId': user_id,
        'total': total,
        'correct': correct,
        'incorrect': total - correct,
        'accuracy': round(accuracy, 2)
    })

# 5. 创建题目（管理员接口）
@app.route('/api/admin/questions', methods=['POST'])
def create_question():
    data = request.json
    
    question = Question(
        title=data.get('title'),
        description=data.get('description'),
        question_type=data.get('questionType'),
        options=data.get('options'),
        correct_answers=data.get('correctAnswers'),
        difficulty=data.get('difficulty', 'medium')
    )
    
    db.session.add(question)
    db.session.commit()
    
    return jsonify({
        'id': question.id,
        'message': '题目创建成功'
    }), 201

# 6. 删除题目（管理员接口）
@app.route('/api/admin/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    
    return jsonify({'message': '题目已删除'}), 200

# 健康检查
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
