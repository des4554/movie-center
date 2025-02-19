import os
HOST = '127.0.0.1'
PORT = 3306
DATABASE = 'movie_com'
USERNAME = 'root'
PASSWORD = '123456'
class Config:
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 密钥配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'