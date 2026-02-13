"""
后台管理系统应用
"""
import os
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from sqlalchemy import func

from config import get_config
from models import db, Admin, Question, UserAnswer, Category, UserStatistics

# 创建应用
app = Flask(__name__)
config = get_config()
app.config.from_object(config)
app.config['JSON_SORT_KEYS'] = False

# 初始化扩展
db.init_app(app)
CORS(app)

# ==================== 认证相关 ====================

def generate_token(admin_id, expires_in=86400):
    """生成 JWT token"""
    payload = {
        'admin_id': admin_id,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    """验证 JWT token"""
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload.get('admin_id')
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def require_admin(f):
    """要求管理员认证的装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({'error': '缺少认证令牌'}), 401
        
        admin_id = verify_token(token)
        if not admin_id:
            return jsonify({'error': '无效或过期的令牌'}), 401
        
        request.admin_id = admin_id
        return f(*args, **kwargs)
    
    return decorated_function

# ==================== 管理员相关 API ====================

@app.route('/admin/api/login', methods=['POST'])
def admin_login():
    """管理员登录"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400
    
    admin = Admin.query.filter_by(username=username).first()
    if not admin or not admin.check_password(password):
        return jsonify({'error': '用户名或密码错误'}), 401
    
    if not admin.is_active:
        return jsonify({'error': '账户已禁用'}), 403
    
    token = generate_token(admin.id)
    return jsonify({
        'token': token,
        'admin': admin.to_dict(),
        'expires_in': 86400
    })

@app.route('/admin/api/admin/profile', methods=['GET'])
@require_admin
def get_admin_profile():
    """获取管理员信息"""
    admin = Admin.query.get(request.admin_id)
    if not admin:
        return jsonify({'error': '管理员不存在'}), 404
    return jsonify(admin.to_dict())

@app.route('/admin/api/admin/password', methods=['POST'])
@require_admin
def change_password():
    """修改密码"""
    admin = Admin.query.get(request.admin_id)
    data = request.get_json()
    
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    if not admin.check_password(old_password):
        return jsonify({'error': '旧密码错误'}), 401
    
    admin.set_password(new_password)
    db.session.commit()
    
    return jsonify({'message': '密码已修改'})

# ==================== 题目管理 API ====================

@app.route('/admin/api/questions', methods=['GET'])
@require_admin
def get_questions_admin():
    """获取题目列表（管理员）"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    difficulty = request.args.get('difficulty')
    category = request.args.get('category')
    search = request.args.get('search')
    
    query = Question.query
    
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(Question.title.ilike(f'%{search}%'))
    
    total = query.count()
    pages = (total + per_page - 1) // per_page
    
    questions = query.order_by(Question.created_at.desc())\
        .limit(per_page)\
        .offset((page - 1) * per_page)\
        .all()
    
    return jsonify({
        'current': page,
        'pages': pages,
        'total': total,
        'data': [q.to_dict(include_answers=True) for q in questions]
    })

@app.route('/admin/api/questions', methods=['POST'])
@require_admin
def create_question():
    """创建题目"""
    data = request.get_json()
    
    question = Question(
        title=data.get('title'),
        description=data.get('description'),
        question_type=data.get('question_type'),
        options=data.get('options'),
        correct_answers=data.get('correct_answers'),
        explanation=data.get('explanation'),
        difficulty=data.get('difficulty', 'medium'),
        category=data.get('category'),
        admin_id=request.admin_id,
        is_published=data.get('is_published', True)
    )
    
    db.session.add(question)
    db.session.commit()
    
    return jsonify({
        'message': '题目已创建',
        'question': question.to_dict(include_answers=True)
    }), 201

@app.route('/admin/api/questions/<int:question_id>', methods=['GET'])
@require_admin
def get_question_admin(question_id):
    """获取题目详情（管理员）"""
    question = Question.query.get_or_404(question_id)
    return jsonify(question.to_dict(include_answers=True))

@app.route('/admin/api/questions/<int:question_id>', methods=['PUT'])
@require_admin
def update_question(question_id):
    """更新题目"""
    question = Question.query.get_or_404(question_id)
    data = request.get_json()
    
    question.title = data.get('title', question.title)
    question.description = data.get('description', question.description)
    question.question_type = data.get('question_type', question.question_type)
    question.options = data.get('options', question.options)
    question.correct_answers = data.get('correct_answers', question.correct_answers)
    question.explanation = data.get('explanation', question.explanation)
    question.difficulty = data.get('difficulty', question.difficulty)
    question.category = data.get('category', question.category)
    question.is_published = data.get('is_published', question.is_published)
    question.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'message': '题目已更新',
        'question': question.to_dict(include_answers=True)
    })

@app.route('/admin/api/questions/<int:question_id>', methods=['DELETE'])
@require_admin
def delete_question(question_id):
    """删除题目"""
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    
    return jsonify({'message': '题目已删除'})

# ==================== 分类管理 API ====================

@app.route('/admin/api/categories', methods=['GET'])
def get_categories():
    """获取所有分类"""
    categories = Category.query.order_by(Category.order).all()
    return jsonify([c.to_dict() for c in categories])

@app.route('/admin/api/categories', methods=['POST'])
@require_admin
def create_category():
    """创建分类"""
    data = request.get_json()
    
    category = Category(
        name=data.get('name'),
        description=data.get('description'),
        order=data.get('order', 0)
    )
    
    db.session.add(category)
    db.session.commit()
    
    return jsonify({
        'message': '分类已创建',
        'category': category.to_dict()
    }), 201

@app.route('/admin/api/categories/<int:category_id>', methods=['PUT'])
@require_admin
def update_category(category_id):
    """更新分类"""
    category = Category.query.get_or_404(category_id)
    data = request.get_json()
    
    category.name = data.get('name', category.name)
    category.description = data.get('description', category.description)
    category.order = data.get('order', category.order)
    
    db.session.commit()
    return jsonify({'message': '分类已更新', 'category': category.to_dict()})

@app.route('/admin/api/categories/<int:category_id>', methods=['DELETE'])
@require_admin
def delete_category(category_id):
    """删除分类"""
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': '分类已删除'})

# ==================== 统计分析 API ====================

@app.route('/admin/api/statistics/overview', methods=['GET'])
@require_admin
def get_statistics_overview():
    """获取统计概览"""
    total_questions = Question.query.count()
    published_questions = Question.query.filter_by(is_published=True).count()
    total_answers = UserAnswer.query.count()
    total_users = db.session.query(func.count(func.distinct(UserAnswer.user_id))).scalar() or 0
    
    # 难度分布
    difficulty_stats = db.session.query(
        Question.difficulty,
        func.count(Question.id)
    ).group_by(Question.difficulty).all()
    
    # 正确率
    if total_answers > 0:
        correct_answers = UserAnswer.query.filter_by(is_correct=True).count()
        accuracy = round(correct_answers * 100 / total_answers, 2)
    else:
        accuracy = 0
    
    return jsonify({
        'totalQuestions': total_questions,
        'publishedQuestions': published_questions,
        'totalAnswers': total_answers,
        'totalUsers': total_users,
        'accuracy': accuracy,
        'difficultyStats': [
            {'difficulty': d, 'count': c} for d, c in difficulty_stats
        ]
    })

@app.route('/admin/api/statistics/users', methods=['GET'])
@require_admin
def get_user_statistics():
    """获取用户统计"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    stats = UserStatistics.query\
        .order_by(UserStatistics.updated_at.desc())\
        .limit(per_page)\
        .offset((page - 1) * per_page)\
        .all()
    
    total = UserStatistics.query.count()
    pages = (total + per_page - 1) // per_page
    
    return jsonify({
        'current': page,
        'pages': pages,
        'total': total,
        'data': [s.to_dict() for s in stats]
    })

# ==================== 前端服务 ====================

FRONTEND_PATH = os.path.join(os.path.dirname(__file__), '..', 'frontend')
ADMIN_PATH = os.path.join(os.path.dirname(__file__), '..', 'admin')

@app.route('/admin/')
@app.route('/admin/index.html')
def admin_index():
    """管理后台首页"""
    return send_from_directory(ADMIN_PATH, 'index.html')

@app.route('/admin/<path:path>')
def admin_static(path):
    """管理后台静态文件"""
    return send_from_directory(ADMIN_PATH, path)

@app.route('/')
def index():
    """前端首页"""
    return send_from_directory(FRONTEND_PATH, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    """前端静态文件"""
    if path.startswith('admin/'):
        return admin_static(path[6:])
    if path.startswith('api'):
        return jsonify({'error': 'Not found'}), 404
    return send_from_directory(FRONTEND_PATH, path)

# ==================== 初始化 ====================

def init_db():
    """初始化数据库"""
    with app.app_context():
        db.create_all()
        
        # 创建默认管理员
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            admin = Admin(username='admin', email='admin@quiz.local')
            admin.set_password('admin123')
            db.session.add(admin)
            
            # 初始化题目分类
            categories = ['计算机基础', '操作系统', '数据库', '网络协议', '算法与数据结构']
            for cat in categories:
                category = Category(name=cat)
                db.session.add(category)
            
            db.session.commit()
            print("✅ 数据库已初始化，默认管理员: admin / admin123")
        
        # 初始化示例题目
        if Question.query.count() == 0:
            from init_data import create_sample_questions
            create_sample_questions(db, admin)
            print("✅ 示例题目已创建")

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Admin': Admin, 'Question': Question, 'UserAnswer': UserAnswer}

if __name__ == '__main__':
    init_db()
    
    port = int(os.getenv('PORT', 3000))
    host = os.getenv('HOST', '0.0.0.0')
    print(f"🚀 应用启动在 http://{host}:{port}")
    print(f"📱 前端地址: http://localhost:{port}")
    print(f"🔐 管理后台: http://localhost:{port}/admin")
    
    app.run(host=host, port=port, debug=False)
