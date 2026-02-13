"""
数据库模型
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Admin(db.Model):
    """管理员用户"""
    __tablename__ = 'admin'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }

class Question(db.Model):
    """题目"""
    __tablename__ = 'question'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    description = db.Column(db.Text)
    question_type = db.Column(db.String(20), nullable=False)  # single, multiple
    options = db.Column(db.JSON, nullable=False)  # [{"id": "A", "text": "..."}, ...]
    correct_answers = db.Column(db.JSON, nullable=False)  # ["A"] 或 ["A", "B"]
    explanation = db.Column(db.Text)  # 解析说明
    difficulty = db.Column(db.String(20), default='medium', index=True)  # easy, medium, hard
    category = db.Column(db.String(100), index=True)  # 题目分类
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    is_published = db.Column(db.Boolean, default=True, index=True)
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    admin = db.relationship('Admin', backref='questions')
    
    def to_dict(self, include_answers=False):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'questionType': self.question_type,
            'options': self.options,
            'difficulty': self.difficulty,
            'category': self.category,
            'explanation': self.explanation,
            'isPublished': self.is_published,
            'viewCount': self.view_count,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat()
        }
        if include_answers:
            data['correctAnswers'] = self.correct_answers
        return data

class UserAnswer(db.Model):
    """用户答题记录"""
    __tablename__ = 'user_answer'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False, index=True)
    user_id = db.Column(db.String(100), nullable=False, index=True)
    selected_answers = db.Column(db.JSON, nullable=False)  # ["A"] 或 ["A", "B"]
    is_correct = db.Column(db.Boolean, nullable=False, index=True)
    time_spent = db.Column(db.Integer)  # 花费的时间（秒）
    answered_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    question = db.relationship('Question', backref='user_answers')
    
    def to_dict(self):
        return {
            'id': self.id,
            'questionId': self.question_id,
            'userId': self.user_id,
            'selectedAnswers': self.selected_answers,
            'isCorrect': self.is_correct,
            'timeSpent': self.time_spent,
            'answeredAt': self.answered_at.isoformat()
        }

class Category(db.Model):
    """题目分类"""
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'order': self.order
        }

class UserStatistics(db.Model):
    """用户统计（缓存）"""
    __tablename__ = 'user_statistics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    total_answers = db.Column(db.Integer, default=0)
    correct_answers = db.Column(db.Integer, default=0)
    incorrect_answers = db.Column(db.Integer, default=0)
    accuracy = db.Column(db.Float, default=0.0)
    last_answer_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'userId': self.user_id,
            'total': self.total_answers,
            'correct': self.correct_answers,
            'incorrect': self.incorrect_answers,
            'accuracy': round(self.accuracy, 2)
        }
