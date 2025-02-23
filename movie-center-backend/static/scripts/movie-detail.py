import mysql.connector
from mysql.connector import Error
import csv

try:
    # 连接到MySQL数据库
    connection = mysql.connector.connect(
        host='localhost',       # 数据库主机地址
        user='root',    # 数据库用户名
        password='123456',# 数据库密码
        database='movie_com'     # 数据库名称
    )

    if connection.is_connected():
        print("成功连接到MySQL数据库")

        # 创建游标对象
        cursor = connection.cursor()
        delete_query = "DELETE FROM movie_detail"
        cursor.execute(delete_query)
        # 读取CSV文件并插入数据
        with open('IMDBPoster/info/info.csv', mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # 插入每一行
                insert_query = """
                INSERT INTO movie_detail (id, name, url, time, genre, release_time, intro, directors, writers, stars)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                data = (
                    row['id'],  # id
                    row['name'],  # name
                    row['url'],  # url
                    row['time'],  # time
                    row['genre'],  # genre
                    row['release_time'],  # release_time
                    row['intro'],  # intro
                    row['directors'],  # directors
                    row['writers'],  # writers
                    row['stars']  # stars
                )
                cursor.execute(insert_query, data)
        # 提交事务
        connection.commit()
        print("数据导入成功")

except Error as e:
    print(f"错误: {e}")

finally:
    if connection.is_connected():
        # 关闭游标和连接
        cursor.close()
        connection.close()
        print("MySQL连接已关闭")