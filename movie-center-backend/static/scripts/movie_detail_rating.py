import mysql.connector
from mysql.connector import Error
import random


def generate_age_ratings():
    """生成年龄段评分数量的逗号分隔字符串"""
    age_groups = ['Under18', '18-24', '25-34', '35-44', '45-54', '55+']
    ratings = [str(random.randint(50, 1000)) for _ in age_groups]
    return ','.join(ratings)


try:
    # 连接到MySQL数据库
    connection = mysql.connector.connect(
        host='localhost',  # 数据库主机地址
        user='root',  # 数据库用户名
        password='123456',  # 数据库密码
        database='movie_com'  # 数据库名称
    )

    if connection.is_connected():
        print("成功连接到MySQL数据库")

        # 创建游标对象
        cursor = connection.cursor()

        # 首先获取所有电影的ID
        cursor.execute("SELECT id FROM movie_detail")
        movie_ids = [row[0] for row in cursor.fetchall()]

        # 为每部电影更新三个字段
        for movie_id in movie_ids:
            male_rating = random.randint(100, 5000)  # 男性评分数量
            female_rating = random.randint(100, 5000)  # 女性评分数量
            age_rating = generate_age_ratings()  # 年龄段评分数量

            update_query = """
            UPDATE movie_detail 
            SET male_rating = %s, 
                female_rating = %s, 
                age_rating = %s
            WHERE id = %s
            """
            cursor.execute(update_query, (male_rating, female_rating, age_rating, movie_id))

        # 提交事务
        connection.commit()
        print(f"成功更新{len(movie_ids)}部电影的评分统计数据")

except Error as e:
    print(f"错误: {e}")
    connection.rollback()

finally:
    if connection.is_connected():
        # 关闭游标和连接
        cursor.close()
        connection.close()
        print("MySQL连接已关闭")