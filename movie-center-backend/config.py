import os
import json
from pathlib import Path
HOST = '127.0.0.1'
PORT = 3306
DATABASE = 'movie_com'
USERNAME = 'root'
PASSWORD = '123456'

EPSILON = 1.0  #系统隐私保护值
class Config:
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 密钥配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'



CONFIG_FILE = Path("runtime_config.json")

# 默认值
_DEFAULT_EPSILON = 1.0

def get_epsilon():
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text()).get("epsilon", _DEFAULT_EPSILON)
    return _DEFAULT_EPSILON

def set_epsilon(value):
    CONFIG_FILE.write_text(json.dumps({"epsilon": float(value)}))

# 初始化全局变量
EPSILON = get_epsilon()