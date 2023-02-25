import pymysql


def getdb():
    host = 'localhost'
    user = 'root'
    password = '245664'
    database = 'transaction'
    db = pymysql.connect(host=host, user=user, password=password, database=database)
    return db
