import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import mysql.connector
from config import EPSILON
# 1. 数据加载
# 假设 rating.csv 包含 userId, movieId, rating 字段
ratings_file = 'static/scripts/IMDBPoster/ml-latest-small/ratings.csv'
ratings = pd.read_csv(ratings_file)

# 连接到MySQL数据库
connection = mysql.connector.connect(
    host='localhost',       # 数据库主机地址
    user='root',    # 数据库用户名
    password='123456',  # 数据库密码
    database='movie_com'     # 数据库名称
)

if connection.is_connected():
    print("成功连接到MySQL数据库")

    # 创建游标对象
    cursor = connection.cursor()
    # 查询每一行
    query = """
    SELECT movie_id, title, genres FROM movies
    """
    cursor.execute(query)

    # 获取查询结果
    rows = cursor.fetchall()

    # 将结果转换为DataFrame
    columns = [col[0] for col in cursor.description]  # 获取列名
    global movies
    movies = pd.DataFrame(rows, columns=columns)
    # 提交事务
    connection.commit()
    print("数据导出成功")

if connection.is_connected():
    # 关闭游标和连接
    cursor.close()
    connection.close()
    print("MySQL连接已关闭")

# 2. 差分隐私保护机制：添加拉普拉斯噪声
def add_laplace_noise(data, epsilon):
    """为数据添加拉普拉斯噪声"""
    scale = 1.0 / epsilon
    noise = np.random.laplace(0, scale, data.shape)
    return data + noise




# 5. 基于用户的协同过滤算法
def predict_ratings(user_id, user_similarity, user_movie_matrix):
    """基于用户相似度预测评分"""
    user_index = user_movie_matrix.index.get_loc(user_id)
    user_ratings = user_movie_matrix.iloc[user_index]
    unrated_movies = user_ratings[user_ratings == 0].index

    predicted_ratings = {}
    for movie_id in unrated_movies:
        movie_index = user_movie_matrix.columns.get_loc(movie_id)
        similar_users = user_similarity[user_index]
        rated_users = user_movie_matrix.iloc[:, movie_index] != 0

        # 将布尔数组转换为整数索引
        rated_users_indices = np.where(rated_users)[0]

        # 使用整数索引进行切片
        weighted_sum = np.dot(similar_users[rated_users], user_movie_matrix.iloc[rated_users_indices, movie_index])
        sum_of_weights = np.abs(similar_users[rated_users]).sum()
        predicted_ratings[movie_id] = weighted_sum / sum_of_weights if sum_of_weights != 0 else 0

    return predicted_ratings

# 6. 用户偏好类型匹配
def genre_match_score(genres, favorite_genres):
    """计算电影与用户偏好类型的匹配度"""
    genre_list = genres.split('|')
    match_count = sum(1 for genre in genre_list if genre in favorite_genres)
    return match_count / len(genre_list) if genre_list else 0

def normalize_ratings(ratings):
    """将评分归一化到0-100区间"""
    min_rating = min(ratings.values())
    max_rating = max(ratings.values())
    range_rating = max_rating - min_rating
    normalized_ratings = {k: (v - min_rating) / range_rating * 100 for k, v in ratings.items()}
    return normalized_ratings
def get_recommend_movies(user_id, user_favorite_genres, user_browse_history, user_rating_dict):
    epsilon = EPSILON # 隐私预算越小，隐私保护越强，但数据准确性越低
    print("ratings", ratings)
    # 向ratings新增用户自己的评分历史
    new_rows = []
    for movie_id, rating in user_rating_dict.items():
        new_rows.append({
            'userId': user_id,
            'movieId': movie_id,
            'rating': rating,
            'timestamp': pd.Timestamp.now().timestamp()
        })
    new_data = pd.DataFrame(new_rows)
    # print(new_data)
    new_ratings = pd.concat([ratings, new_data], ignore_index=True)
    # 混淆评分
    new_ratings['rating'] = add_laplace_noise(new_ratings['rating'].values, epsilon)
    print("混淆后的评分,new_ratings\n", new_ratings)
    user_movie_matrix = new_ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)

    user_similarity = cosine_similarity(user_movie_matrix)

    # 计算用户浏览历史的类型权重
    total_views = sum(user_browse_history.values())
    genre_weights = {genre: count / total_views for genre, count in user_browse_history.items()}



    # 计算电影与用户偏好类型的匹配度
    def enhanced_genre_match(genres):
        genre_list = genres.split('|')
        match_score = 0
        for genre in genre_list:
            if genre in user_favorite_genres:
                match_score += 1
            if genre in genre_weights:
                match_score += genre_weights[genre] * 2  #浏览权重加成
        return match_score / len(genre_list) if genre_list else 0

    movies['genre_match'] = movies['genres'].apply(enhanced_genre_match)

    # 7. 预测用户对未评分电影的评分
    predicted_ratings = predict_ratings(user_id, user_similarity, user_movie_matrix)

    # 8.1 结合用户偏好类型调整推荐分数
    for movie_id, rating in predicted_ratings.items():
        genre_match = movies.loc[movies['movie_id'] == movie_id, 'genre_match'].values[0]
        predicted_ratings[movie_id] = rating * (1 + genre_match)  # 调整评分

    # 8.2 结合用户年龄和性别调整推荐分数


    normalized_predicted_ratings = normalize_ratings(predicted_ratings)
    # 9. 按调整后的评分排序
    recommended_movies = sorted(normalized_predicted_ratings.items(), key=lambda x: x[1], reverse=True)

    # 10. 输出推荐结果
    for movie_id, score in recommended_movies[:10]:
        movie_title = movies.loc[movies['movie_id'] == movie_id, 'title'].values[0] if movie_id in movies[
            'movie_id'].values else "Unknown"
        # print(f"Movie ID: {movie_id}, 电影名称: {movie_title}, 推荐分数: {score:.2f}")
    return recommended_movies[:10]

# get_recommend_movies(1, ['Adventure', 'Comic'])