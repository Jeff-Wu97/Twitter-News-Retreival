import sqlite3


def conn_db():
    # 连接到数据库，如果数据库不存在的话，将会自动创建一个 数据库
    conn = sqlite3.connect('twiNewsSearchDB.db')
    # 创建一个游标 curson
    cursor = conn.cursor()
    return conn, cursor


def create_table():  # 创建数据表
    conn, cursor = conn_db()
    sql1 = '''CREATE TABLE DOC_INFO
           (ID INTEGER PRIMARY KEY AUTOINCREMENT,
           POST_TIME      CHAR(20)      NOT NULL,
           TEXT           TEXT          NOT NULL,
           ACCOUNT_NAME   VARCHAR(100)  NOT NULL,
           TWEET_ID       TEXT          NOT NULL);'''
    sql2 = '''CREATE TABLE INVERT_INDEX
               (ID INTEGER PRIMARY KEY AUTOINCREMENT,
               TERM       VARCHAR(100)  NOT NULL,
               V_VALUE    TEXT          NOT NULL);'''
    cursor.execute(sql2)


def insert(sql, para):  # 插入语句
    conn, cursor = conn_db()
    sta = cursor.execute(sql, para)
    conn.commit()
    return sta


def select(sql):  # 查询语句
    conn, cursor = conn_db()
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def update(sql):  # 插入语句
    conn, cursor = conn_db()
    sta = cursor.execute(sql)
    conn.commit()
    return sta

# create_table()
