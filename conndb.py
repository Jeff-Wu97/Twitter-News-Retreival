import pymysql
import sqlite3


def conn_db():  # 连接数据库函数
    conn = pymysql.connect(user='root', password='123456', database='twiNewsSearchDB')
    cur = conn.cursor()
    return conn, cur


def exe_insert(sql):  # 更新语句，可执行insert语句
    conn, cur = conn_db()
    sta = cur.execute(sql)
    cur.commit()  # 执行commit操作，插入语句才能生效
    return sta


def exe_delete(ids):  # 删除语句，可批量删除
    conn, cur = conn_db()
    for eachID in ids.split(' '):
        sta = cur.execute('delete from cms where id =%d' % int(eachID))
    cur.commit()  # 执行commit操作，插入语句才能生效
    return sta


def exe_query(sql):  # 查询语句
    conn, cur = conn_db()
    cur.execute(sql)
    results = cur.fetchall()
    return results


def conn_close(conn, cur):  # 关闭所有连接
    cur.close()
    conn.close()


# if __name__ == '__main__':
#     #创建数据库
#     conn = pymysql.connect(host='localhost', user='root', passwd='root')
#     cur = conn.cursor()
#     cur.execute("CREATE DATABASE TTDSDB")
#
#     conn = pymysql.connect(host='localhost', user='root', passwd='root', db='TTDSDB', charset='utf8')
#     cur = conn.cursor()
#     cur.execute("SHOW DATABASES")
