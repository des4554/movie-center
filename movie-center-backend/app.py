from flask import Flask, jsonify, request
from models import db, User, Movie, Rating, MovieDetail
from config import Config
from flask_cors import CORS
import os

from algorithms import get_recommend_movies

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
                "password": user.password,
                "tags": user.tags,
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
    # 获取查询参数中的 id 列表
    ids_str = request.args.get('ids')  # 获取字符串形式的 ids
    if ids_str:
        ids = [int(id) for id in ids_str.split(',')]  # 将字符串转换为整数列表
    else:
        ids = []  # 如果没有传递 ids，返回空列表

    # 根据 id 列表查询电影信息
    if ids:
        movies = Movie.query.filter(Movie.movie_id.in_(ids)).all()
    else:
        movies = Movie.query.all()  # 如果没有传递 ids，返回所有电影

    # 返回电影信息的 JSON 数据
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

#搜索电影详情信息
@app.route('/movies/<int:movieId>', methods=['GET'])
def get_movie_detail(movieId):
    movie = MovieDetail.query.get(movieId)
    return jsonify({
        'movie_id': movie.id,
        'name': movie.name,
        'url': movie.url,
        'time': movie.time,
        'genre': movie.genre,
        'release_time': movie.release_time,
        'intro': movie.intro,
        'directors': movie.directors,
        'writers': movie.writers,
        'stars': movie.stars
    }), 201

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

#获取用户评分
@app.route('/ratings/<int:userId>', methods=['GET'])
def get_movie_rating(userId):
    ratings = Rating.query.filter_by(user_id=userId).all()
    return jsonify([{
        'message': 'get ratings successfully',
        'rating_id': rating.rating_id,
        'user_id': rating.user_id,
        'movie_id': rating.movie_id,
        'rating': rating.rating,
        'comment': rating.comment,
        'timestamp': rating.timestamp
    } for rating in ratings])

@app.route('/ratings/<int:userId>/<int:movieId>', methods=['GET'])
def get_movie_rating_comment(userId, movieId):
    http_version = request.environ.get('HTTP_VERSION')
    print('http_version:', http_version)
    rating = Rating.query.filter_by(user_id=userId, movie_id=movieId).first()
    if rating:
        return jsonify({
            'message': 'get ratings successfully',
            'rating_id': rating.rating_id,
            'user_id': rating.user_id,
            'movie_id': rating.movie_id,
            'rating': rating.rating,
            'comment': rating.comment,
            'timestamp': rating.timestamp
        })
    else:
        return jsonify({
            'message': 'Rating not found',
        })
#修改和新增用户评分
@app.route('/ratings/<int:userId>/<int:movieId>', methods=['POST'])
def updateMovieRating(userId, movieId):
    rating = Rating.query.filter_by(user_id=userId, movie_id=movieId).first()
    data = request.get_json()
    rat = data.get('rating')
    comment = data.get('comment')
    if rating:
        rating.rating = rat
        rating.comment = comment
        db.session.commit()
        return jsonify({'message': 'Rating updated successfully'}), 201
    else:
        new_rating = Rating(user_id=userId, movie_id=movieId, rating=rat, comment=comment)
        db.session.add(new_rating)
        db.session.commit()

        return jsonify({'message': 'Rating added successfully'}), 201

#删除用户评分
@app.route('/ratings/<int:userId>/<int:movieId>', methods=['DELETE'])
def deleteMovieRating(userId, movieId):
    # 查询评分记录
    rating = Rating.query.filter_by(user_id=userId, movie_id=movieId).first()

    # 如果评分记录不存在，返回错误信息
    if rating is None:
        return jsonify({'error': 'Rating not found'}), 404

    try:
        # 删除评分记录
        db.session.delete(rating)
        db.session.commit()
        return jsonify({'message': 'Rating deleted successfully'}), 200
    except Exception as e:
        # 如果删除失败，回滚并返回错误信息
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
#修改用户信息
@app.route('/infoChange', methods=['POST'])
def infoChange():
    data = request.get_json()
    print("data" + str(data))
    id = data.get('userid')
    user = User.query.get(id)
    print("user", user)
    user.username = data.get('username')
    # avatar_url  = user.avatarUrl
    # 删除对应的头像，删不了一点
    # static_index = avatar_url.find('/static/')
    # relative_path = avatar_url[static_index:]
    # print("delete", relative_path)
    # if avatar_url and os.path.exists(relative_path):
    #     print("delete!!!")
    #     os.remove(avatar_url)
    user.avatarUrl = data.get('avatar_url')
    user.phone = data.get('phone')
    user.email = data.get('email')
    user.gender = data.get('gender')
    user.age = data.get('age')
    user.password = data.get('password')
    user.tags = data.get('tags')
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


@app.route('/recommend/<int:userId>', methods=['GET'])
def recommend(userId):
    user = User.query.get(userId)
    like_tags = user.tags.split(',')
    movies = get_recommend_movies(userId, like_tags)
    print(movies)
    return jsonify(movies)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    print(data)
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'success': False,'message': 'Username already exists'}), 400
    user = User()
    user.username = data.get('username')
    user.password = data.get('password')
    user.email = data.get('email')
    user.gender = data.get('gender')
    user.age = data.get('age')
    user.phone = data.get('phone')
    user.avatarUrl = data.get('avatar_url')
    user.tags = data.get('tags')
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@app.route('/user/<int:userId>', methods=['DELETE'])
def delete_user(userId):
    user = User.query.get(userId)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'success': True, 'message': 'User deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
