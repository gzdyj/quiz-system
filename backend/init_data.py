"""
初始化示例数据脚本
运行方式: python init_data.py
"""

from app import app, db, Question

# 示例题目数据
SAMPLE_QUESTIONS = [
    {
        'title': '以下哪个不是计算机的硬件设备？',
        'description': '计算机硬件是指组成计算机的各种物理设备。',
        'question_type': 'single',
        'options': [
            {'id': 'A', 'text': 'CPU'},
            {'id': 'B', 'text': '内存'},
            {'id': 'C', 'text': 'Windows系统'},
            {'id': 'D', 'text': '硬盘'}
        ],
        'correct_answers': ['C'],
        'difficulty': 'easy'
    },
    {
        'title': '下列哪些是常见的编程语言？（多选）',
        'description': '编程语言是用于编写计算机程序的形式化语言。',
        'question_type': 'multiple',
        'options': [
            {'id': 'A', 'text': 'Python'},
            {'id': 'B', 'text': 'JavaScript'},
            {'id': 'C', 'text': '中文'},
            {'id': 'D', 'text': 'Java'}
        ],
        'correct_answers': ['A', 'B', 'D'],
        'difficulty': 'easy'
    },
    {
        'title': '数据库中的主键具有以下哪些特性？（多选）',
        'description': '主键是数据库表中用于唯一标识每条记录的字段。',
        'question_type': 'multiple',
        'options': [
            {'id': 'A', 'text': '唯一性'},
            {'id': 'B', 'text': '非空性'},
            {'id': 'C', 'text': '可重复性'},
            {'id': 'D', 'text': '自动递增'}
        ],
        'correct_answers': ['A', 'B'],
        'difficulty': 'medium'
    },
    {
        'title': '下列关于操作系统的说法中，正确的是？',
        'description': '操作系统是管理计算机硬件和软件资源的程序。',
        'question_type': 'single',
        'options': [
            {'id': 'A', 'text': '操作系统是连接用户和计算机的界面'},
            {'id': 'B', 'text': '操作系统只能处理一个任务'},
            {'id': 'C', 'text': '操作系统不需要管理内存'},
            {'id': 'D', 'text': '所有操作系统都相同'}
        ],
        'correct_answers': ['A'],
        'difficulty': 'medium'
    },
    {
        'title': '面向对象编程中的三大特性是？（多选）',
        'description': '这是OOP的核心概念。',
        'question_type': 'multiple',
        'options': [
            {'id': 'A', 'text': '封装'},
            {'id': 'B', 'text': '继承'},
            {'id': 'C', 'text': '多态'},
            {'id': 'D', 'text': '递归'}
        ],
        'correct_answers': ['A', 'B', 'C'],
        'difficulty': 'medium'
    },
    {
        'title': '以下关于网络协议的描述，哪个是错误的？',
        'description': '网络协议是一组规则和标准。',
        'question_type': 'single',
        'options': [
            {'id': 'A', 'text': 'TCP协议是面向连接的'},
            {'id': 'B', 'text': 'UDP协议比TCP协议可靠'},
            {'id': 'C', 'text': 'HTTP协议运行在TCP之上'},
            {'id': 'D', 'text': 'IP协议负责路由'}
        ],
        'correct_answers': ['B'],
        'difficulty': 'hard'
    },
    {
        'title': '算法的时间复杂度为O(n²)，这意味着？',
        'description': '时间复杂度用来估算算法的运行时间。',
        'question_type': 'single',
        'options': [
            {'id': 'A', 'text': '算法需要n的平方步操作'},
            {'id': 'B', 'text': '算法运行时间固定'},
            {'id': 'C', 'text': '算法永远不会终止'},
            {'id': 'D', 'text': '算法使用n的平方内存'}
        ],
        'correct_answers': ['A'],
        'difficulty': 'hard'
    },
    {
        'title': '以下哪些是数据结构？（多选）',
        'description': '数据结构是组织和存储数据的方式。',
        'question_type': 'multiple',
        'options': [
            {'id': 'A', 'text': '数组'},
            {'id': 'B', 'text': '链表'},
            {'id': 'C', 'text': '树'},
            {'id': 'D', 'text': '字母表'}
        ],
        'correct_answers': ['A', 'B', 'C'],
        'difficulty': 'easy'
    },
    {
        'title': '什么是内存泄漏？',
        'description': '内存管理是程序设计中的重要概念。',
        'question_type': 'single',
        'options': [
            {'id': 'A', 'text': '程序分配的内存没有被正确释放'},
            {'id': 'B', 'text': '内存条损坏'},
            {'id': 'C', 'text': '程序运行速度变慢'},
            {'id': 'D', 'text': '硬盘空间不足'}
        ],
        'correct_answers': ['A'],
        'difficulty': 'medium'
    },
    {
        'title': '以下关于多线程编程的说法中，正确的有？（多选）',
        'description': '多线程是并发编程的重要方式。',
        'question_type': 'multiple',
        'options': [
            {'id': 'A', 'text': '多线程可以充分利用多核处理器'},
            {'id': 'B', 'text': '多线程编程比单线程更简单'},
            {'id': 'C', 'text': '多线程需要考虑线程同步问题'},
            {'id': 'D', 'text': '线程之间可以共享内存'}
        ],
        'correct_answers': ['A', 'C', 'D'],
        'difficulty': 'hard'
    }
]

def init_database():
    with app.app_context():
        # 清空现有数据（可选）
        db.drop_all()
        db.create_all()
        
        # 插入示例数据
        for q_data in SAMPLE_QUESTIONS:
            question = Question(
                title=q_data['title'],
                description=q_data['description'],
                question_type=q_data['question_type'],
                options=q_data['options'],
                correct_answers=q_data['correct_answers'],
                difficulty=q_data['difficulty']
            )
            db.session.add(question)
        
        db.session.commit()
        print(f"成功初始化 {len(SAMPLE_QUESTIONS)} 道题目")

if __name__ == '__main__':
    init_database()
