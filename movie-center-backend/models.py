from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric

db = SQLAlchemy()

class User(db.Model):
    """用户表"""
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='user')  # 用户角色：user/admin
    avatarUrl = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    tags = db.Column(db.String(225))
    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'role': self.role,
            'avatarUrl': self.avatarUrl,
            'phone': self.phone,
            'age': self.age,
            'gender': self.gender,
            'tags': self.tags
        }


class Movie(db.Model):
    """电影表"""
    __tablename__ = 'movies'
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    poster_url = db.Column(db.String(200))
    description = db.Column(db.Text)
    genres = db.Column(db.String(100))
    rating = db.Column(Numeric(2, 1))  # DECIMAL(2,1)

    @property
    def safe_rating(self):
        return float(self.rating) if self.rating is not None else 0.0
    def __repr__(self):
        return f'<Movie {self.title}>'

    def to_dict(self):
        return {
            'movie_id': self.movie_id,
            'title': self.title,
            'poster_url': self.poster_url,
            'description': self.description,
            'genres': self.genres,
            'rating': float(self.rating) if self.rating is not None else None,  # 转成 float
        }

# 定义电影详情表模型
class MovieDetail(db.Model):
    __tablename__ = 'movie_detail'  # 表名

    # 表字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 电影ID，主键
    name = db.Column(db.String(255), nullable=False)                 # 电影名称
    url = db.Column(db.String(255))                                  # 电影URL
    time = db.Column(db.String(50))                                  # 电影时长
    genre = db.Column(db.String(255))                                # 电影类型
    release_time = db.Column(db.String(255))                                # 上映时间
    intro = db.Column(db.Text)                                       # 电影简介
    directors = db.Column(db.String(255))                            # 导演
    writers = db.Column(db.String(255))                              # 编剧
    stars = db.Column(db.Text)                                       # 主演

    def __repr__(self):
        return f"<MovieDetail(id={self.id}, name={self.name}, genre={self.genre})>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'time': self.time,
            'genre': self.genre,
            'release_time': self.release_time,
            'intro': self.intro,
            'directors': self.directors,
            'writers': self.writers,
            'stars': self.stars,
        }
class Rating(db.Model):
    """评分表"""
    __tablename__ = 'ratings'
    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    comment = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Rating {self.rating}>'


class Browse(db.Model):
    __tablename__ = 'browse_history'
    browse_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    movie_id = db.Column(db.Integer)
    time = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'browse_id': self.browse_id,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'time': self.time,
        }