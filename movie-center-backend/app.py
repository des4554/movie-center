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
                "id": user.user_id,
                "username": user.username,
                "role": user.role,
                "avatar_url": user.avatarUrl,
                "email": user.email,
                "phone": user.phone,
                "gender": user.gender,
                "age": user.age
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
    id = data.get('userId')
    user = User.query.get(id)
    print(user)
    user.username = data.get('username')
    user.avatarUrl = data.get('avatar')
    user.phone = data.get('phone')
    user.email = data.get('email')
    user.gender = data.get('gender')
    user.age = data.get('age')
    db.session.commit()
    return jsonify({
        'success': True,
        'message': 'User info changed successfully'
    }), 201

# 头像上传
# 文件上传配置
UPLOAD_FOLDER = 'uploads'  # 文件保存目录
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # 允许的文件类型
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传目录存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 检查文件类型是否允许
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 文件上传接口
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        # 生成安全的文件名
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # 返回文件的访问 URL
        file_url = f"/uploads/{filename}"
        return jsonify({'url': file_url}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400

# 提供上传文件的访问
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True, static_url_path='/', static_folder='uploads')
