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



def realtime1(ts_code):
    for j in range(6 - len(ts_code)):
        ts_code = "0" + ts_code
    db = getdb()
    cursor = db.cursor()
    _, _, _, _, _, chengjiaoliang, _, _, _, _ = getNow(ts_code)
    get = ''' 
                   SELECT `gujia`, `kaipan`, `super`, `zhuli`, `fenshiliang`
                   FROM `realtime`
                   WHERE `code` = %s
                   ''' % ts_code
    cursor.execute(get)
    fetch = cursor.fetchall()[0]
    print(fetch)
    gujia1, kaipan, super1, zhuli1, fenshiliang1 = fetch
    put = '''
            REPLACE INTO realtime(`code`, `gujia`, `kaipan`, `zhuli`, `super`, `fenshiliang`, `fenshiliang2`) 
                                                            VALUES (%s, %f, %f, %f, %f, %f, %f)
          ''' % (ts_code,  gujia1, kaipan, super1, zhuli1, fenshiliang1, chengjiaoliang)
    cursor.execute(put)
    db.commit()
    db.close()


def realtime2(ts_code):

    for j in range(6 - len(ts_code)):
        ts_code = "0" + ts_code
    db = getdb()
    cursor = db.cursor()
    get = ''' 
                   SELECT `gujia`, `super`, `zhuli`, `fenshiliang`, `fenshiliang2`
                   FROM `realtime`
                   WHERE `code` = %s
                   ''' % ts_code
    cursor.execute(get)
    fetch = cursor.fetchall()[0]
    print(fetch)
    db.commit()
    db.close()
    gujia1, super1, zhuli1, fenshiliang1, fenshiliang2 = fetch
    gujia, kaipan, zuigao, zuidi, zhangfu, chengjiaoliang, jiaoYiE, liutong, super, zhuli = getNow(ts_code)
    fenshiliang2 = chengjiaoliang - fenshiliang2

    # db.close()

    if 3.0 < zhangfu < 5.0:
        if fenshiliang2 != 0:
            junzhi = jiaoYiE * 100 / fenshiliang2
            print(junzhi)
            if zhuli > 0 and super > 0 and abs(junzhi - gujia) / gujia < 0.03:
                return True
        if zhuli > zhuli1 and super > super1 and gujia < kaipan:
            return True
        if fenshiliang2 > fenshiliang1 and gujia < gujia1:
            if zhuli > 0 or super > 0:
                return True
    return False
#
#
# realtime1('000002')
# sleep(6)
# realtime2('000002')
