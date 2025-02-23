from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """用户表"""
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), default='user')  # 用户角色：user/admin
    avatarUrl = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    tags = db.Column(db.String(225))
    def __repr__(self):
        return f'<User {self.username}>'

class Movie(db.Model):
    """电影表"""
    __tablename__ = 'movies'
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    poster_url = db.Column(db.String(200))
    description = db.Column(db.Text)
    genres = db.Column(db.String(100))
    rating = db.Column(db.Float)
    def __repr__(self):
        return f'<Movie {self.title}>'

class Rating(db.Model):
    """评分表"""
    __tablename__ = 'ratings'
    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Rating {self.rating}>'