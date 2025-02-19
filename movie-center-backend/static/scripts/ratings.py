import pandas as pd
import mysql.connector
from mysql.connector import Error

# 读取 ratings.csv 文件
ratings_file = 'IMDBPoster/ml-latest-small/ratings.csv'
ratings_df = pd.read_csv(ratings_file)

# 计算每部电影的平均评分
movie_ratings = ratings_df.groupby('movieId')['rating'].mean().reset_index()
movie_ratings.columns = ['movie_id', 'avg_rating']

# 连接 MySQL 数据库
try:
    connection = mysql.connector.connect(
        host='localhost',       # 数据库主机地址
        user='root',    # 数据库用户名
        password='123456',# 数据库密码
        database='movie_com'     # 数据库名称
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # 遍历每部电影的平均评分，更新 movie 表
        for index, row in movie_ratings.iterrows():
            movie_id = row['movie_id']
            avg_rating = row['avg_rating']

            # 更新 movie 表的 rating 字段
            update_query = """
            UPDATE movie
            SET rating = %s
            WHERE movie_id = %s;
            """
            cursor.execute(update_query, (avg_rating, movie_id))

        # 提交事务
        connection.commit()
        print("电影评分更新成功！")

except Error as e:
    print(f"数据库连接或操作失败: {e}")

finally:
    # 关闭数据库连接
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("数据库连接已关闭。")