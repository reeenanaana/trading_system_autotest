#! /usr/bin/python3
# coding = utf-8
# @Time: 2026/5/15 11:32
# @Author: Rena

import pymysql

from common.yaml_config import GetConf


class MysqlOperate:
    def __init__(self):
        """
        定义变量
        """
        mysql_conf = GetConf().get_mysql_config()
        self.host = mysql_conf['host']
        self.db = mysql_conf['db']
        self.port = mysql_conf['port']
        self.user = mysql_conf['user']
        self.password = mysql_conf['password']
        self.conn = None
        self.cur = None

    def __conn_db(self):
        """
        连接数据库
        :return:
        """
        try:
            # pymysql.connect()连接数据库
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.db,
                port=int(self.port),
                charset='utf8'
            )
        except Exception as e:
            print(e)
            return False
        # 获取cursor游标对象（cursor是一个记录标识，用于一行一行迭代的访问查询返回的结果）
        self.cur = self.conn.cursor()
        return True

    def __close_conn(self):
        """
        关闭与数据库的连接
        :return:
        """
        self.cur.close()
        self.conn.close()
        return True

    def __commit(self):
        """
        执行update/insert语句时，需要commit
        :return:
        """
        self.conn.commit()
        return True

    def query(self, sql):
        """
        查询
        :param sql:
        :return:
        """
        # 连接数据库
        self.__conn_db()
        # 实例self.cur，执行sql语句
        self.cur.execute(sql)
        # 获取通过sql语句查询到的结果
        query_data = self.cur.fetchall()
        if query_data == ():
            query_data = None
            print("没有获取到数据，表为空")
        else:
            pass
        # 断开连接
        self.__close_conn()
        return query_data

    def insert_update_table(self, sql):
        """
        执行增、删、改
        :param sql:
        :return:
        """
        # 连接数据库
        self.__conn_db()
        # 通过cursor执行sql语句
        self.cur.execute(sql)
        # 增删改需要commit
        self.__commit()
        # 关闭连接
        self.__close_conn()


if __name__ == '__main__':
    result = MysqlOperate().query('select * from user')
    # # 取第一个元组数据
    print(result)
    print(result[0])
    print(result[0][1])
    # 写入新数据
    sql = ("INSERT INTO `product` VALUES"
           " (67, '全心宿舍床垫2，1.2*2，舍友不用了，便宜出', 1, 50.00, '全心宿舍床垫，1.2*2，舍友不用了，便宜出', 'http://47.101.216.239:9090/product/product_img/16574178408375f8f7935-67cb-4749-b320-e6e4c285b607', '', 1, '2022-07-10 09:50:48', '2022-07-10 09:50:48', 13);")
    MysqlOperate().insert_update_table(sql)