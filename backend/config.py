"""
应用配置文件
"""
import os
from datetime import timedelta

class Config:
    """基础配置"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class DevelopmentConfig(Config):
    """开发配置"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///questions.db'
    )
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    """生产配置"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://user:password@localhost/quiz_db'
    )

class ReplitConfig(Config):
    """Replit 配置"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:////tmp/questions.db'
    )
    SESSION_COOKIE_SECURE = False

# 获取配置
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'replit': ReplitConfig,
    'default': DevelopmentConfig
}

def get_config():
    """获取当前配置"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
