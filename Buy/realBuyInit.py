import re
from time import sleep
import threading
import datetime as dt
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import pymysql
from io import BytesIO
import gzip
import sys

sys.path.append("..")
from sql.configSql import getdb
from Sell.nowData import getNow


def realtimeInit1(ts_code):
    for j in range(6 - len(ts_code)):
        ts_code = "0" + ts_code
    db = getdb()
    cursor = db.cursor()
    _, _, _, _, _, chengjiaoliang, _, _, _, _ = getNow(ts_code)
    put = '''
            REPLACE INTO realtime(`code`, `gujia`, `kaipan`, `super`, `zhuli`, `fenshiliang`) 
                                                            VALUES (%s, %f, %f, %f, %f, %f)
          ''' % (ts_code, 0, 0, 0, 0, chengjiaoliang)
    cursor.execute(put)
    db.commit()
    db.close()


def realtimeInit2(ts_code):
    for j in range(6 - len(ts_code)):
        ts_code = "0" + ts_code
    db = getdb()
    cursor = db.cursor()
    get = ''' 
                       SELECT `fenshiliang`
                       FROM `realtime`
                       WHERE `code` = %s
                       ''' % ts_code
    cursor.execute(get)
    chengjiaoliang = cursor.fetchall()
    print(chengjiaoliang)
    gujia, kaipan, zuigao, zuidi, zhangfu, chengjiaoliang2, jiaoYiE, liutong, super, zhuli = getNow(ts_code)
    fenshiliang = chengjiaoliang2 - chengjiaoliang[0][0]
    put = '''
            REPLACE INTO realtime(`code`, `gujia`, `kaipan`, `super`, `zhuli`, `fenshiliang`)
                                                            VALUES (%s, %f, %f, %f, %f, %f)
          ''' % (ts_code, gujia, kaipan, super, zhuli, fenshiliang)
    cursor.execute(put)
    db.commit()
    db.close()

#
# realtimeInit1('000002')
# sleep(6)
# realtimeInit2('000002')