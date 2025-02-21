from flask import Flask, jsonify, request, send_from_directory
from models import db, User, Movie, Rating
from config import Config
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# 初始化数据库
db.init_app(app)
with app.app_context():
    db.create_all()



@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter(User.username == username).first()
    if user and user.password == password:
        return jsonify({
            "success": True,
            "user": {
                "userid": user.user_id,
                "username": user.username,
                "role": user.role,
                "avatar_url": user.avatarUrl,
                "email": user.email,
                "phone": user.phone,
                "gender": user.gender,
                "age": user.age,
                "password": user.password
            },
        })
    else:
        return jsonify({
            "success": False,
            "message": "用户名或密码错误",
        }), 401


# 用户注册
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({
            'success': False,
            'message': 'Missing required fields'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'success': False,'message': 'Username already exists'}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'User registered successfully'
    }), 201


# 获取电影列表
@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return jsonify([{
        'movie_id': movie.movie_id,
        'title': movie.title,
        'poster_url': movie.poster_url,
        'description': movie.description,
        'genres': movie.genres,
        'rating': movie.rating
    } for movie in movies])

# 搜索电影
@app.route('/movies/search', methods=['GET'])
def search():
    print('search()')
    search_name = request.args.get('name', '').lower()
    search_genre = request.args.get('genre', '').lower()
    search_rating = request.args.get('rating', type=float)

    # 过滤电影
    filtered_movies = Movie.query.all()
    # for movie in filtered_movies:
    #     print(movie.title)
    if search_name:
        filtered_movies = [m for m in filtered_movies if search_name in m.title.lower()]
    if search_genre:
        filtered_movies = [m for m in filtered_movies if search_genre in m.genres.lower()]
    if search_rating:
        filtered_movies = [m for m in filtered_movies if m.rating >= search_rating]
    # for movie in filtered_movies:
    #     print(movie.title)
    return jsonify([{
        'movie_id': movie.movie_id,
        'title': movie.title,
        'poster_url': movie.poster_url,
        'description': movie.description,
        'genres': movie.genres,
        'rating': movie.rating
    } for movie in filtered_movies])

# 添加电影（管理员功能）
@app.route('/movies', methods=['POST'])
def add_movie():
    data = request.get_json()
    title = data.get('title')
    poster_url = data.get('poster_url')
    description = data.get('description')
    genres = data.get('genres')

    if not title:
        return jsonify({'message': 'Title is required'}), 400

    new_movie = Movie(title=title, poster_url=poster_url, description=description, genres=genres)
    db.session.add(new_movie)
    db.session.commit()

    return jsonify({'message': 'Movie added successfully'}), 201

# 用户评分
@app.route('/ratings', methods=['POST'])
def add_rating():
    data = request.get_json()
    user_id = data.get('user_id')
    movie_id = data.get('movie_id')
    rating = data.get('rating')

    if not user_id or not movie_id or not rating:
        return jsonify({'message': 'Missing required fields'}), 400

    new_rating = Rating(user_id=user_id, movie_id=movie_id, rating=rating)
    db.session.add(new_rating)
    db.session.commit()

    return jsonify({'message': 'Rating added successfully'}), 201

#修改用户信息
@app.route('/infoChange', methods=['POST'])
def infoChange():
    data = request.get_json()
    print("data" + str(data))
    id = data.get('userid')
    user = User.query.get(id)
    print(user)
    user.username = data.get('username')
    user.avatarUrl = data.get('avatar')
    user.phone = data.get('phone')
    user.email = data.get('email')
    user.gender = data.get('gender')
    user.age = data.get('age')
    user.password = data.get('password')
    db.session.commit()
    return jsonify({
        'success': True,
        'message': 'User info changed successfully'
    }), 201

import uuid
# 配置文件上传
AVATARS_FOLDER = os.path.join(app.static_folder, 'avatars')  # 保存到 static/avatars 目录
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # 允许的文件类型
MAX_FILE_SIZE = 2 * 1024 * 1024  # 最大文件大小（2MB）

# 确保 avatars 目录存在
if not os.path.exists(AVATARS_FOLDER):
    os.makedirs(AVATARS_FOLDER)

# 检查文件类型是否允许
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 上传文件接口
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': '未上传文件'}), 400

    file = request.files['file']

    # 检查文件是否存在
    if file.filename == '':
        return jsonify({'success': False, 'message': '未选择文件'}), 400

    # 检查文件类型和大小
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': '文件类型不支持'}), 400

    file.seek(0, os.SEEK_END)  # 移动到文件末尾
    file_size = file.tell()  # 获取文件大小
    file.seek(0)  # 重置文件指针

    if file_size > MAX_FILE_SIZE:
        return jsonify({'success': False, 'message': '文件大小不能超过 2MB'}), 400

    # 生成唯一文件名
    file_ext = file.filename.rsplit('.', 1)[1].lower()
    unique_filename = f'{uuid.uuid4().hex}.{file_ext}'
    file_path = os.path.join(AVATARS_FOLDER, unique_filename)
    file.save(file_path)

    # userid = request.form.get('userId')
    # 返回文件访问 URL
    file_url = f'http://localhost:5000/static/avatars/{unique_filename}'
    return jsonify({'success': True, 'url': file_url})

if __name__ == '__main__':
    app.run(debug=True, static_url_path='/')
