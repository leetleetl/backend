import asyncio

import pymysql
import tushare as ts
from Buy.buy import buyDay
import threading
from time import sleep
from Buy.buyrealtime import real
import datetime as dt
from Buy.realTime import realtime1, realtime2
from Buy.realBuyInit import realtimeInit1, realtimeInit2
import sys

sys.path.append("..")
from sql.configSql import getdb

sem = threading.Semaphore(24)
sem2 = threading.Semaphore(1)


def picOperation():
    db = getdb()
    cursor = db.cursor()
    del1 = "DELETE FROM codelist1"
    cursor.execute(del1)
    token = 'f558cbc6b24ed78c2104e209a8a8986b33ec66b7c55bcfa2f46bc108'
    pro = ts.pro_api(token)
    datas = pro.stock_basic(fields=[
        "ts_code"
    ])
    for i in datas.values.tolist():
        put = '''
                    REPLACE INTO codelist1(code) VALUES (%s)
                  ''' % i[0][0:6]
        cursor.execute(put)
    db.commit()
    cursor.close()
    db.close()


def oneOperation():
    db = getdb()
    cursor = db.cursor()
    del1 = "DELETE FROM codelist2"
    cursor.execute(del1)
    db.commit()
    select1 = "SELECT * FROM codelist1"
    cursor.execute(select1)
    cursor.close()
    db.close()
    fetch = cursor.fetchall()
    # thread = []
    count = 0
    for i in fetch:
        count += 1
        if count == 198:
            sleep(60)
            count = 0
        sem.acquire()
        thr = threading.Thread(target=operation2, args=(i[0],))
        thr.start()


def operation2(code):
    db = getdb()
    cursor = db.cursor()
    for j in range(6 - len(code)):
        code = "0" + code
    try:
        if buyDay(code):
            ins = "REPLACE INTO codelist2(code) VALUES (%s)" % code
            cursor.execute(ins)
            db.commit()
        sem.release()
    except:
        sem.release()
    cursor.close()
    db.close()


def twoOperation():
    db = getdb()
    cursor = db.cursor()
    del1 = "DELETE FROM codelist3"
    cursor.execute(del1)
    db.commit()
    select1 = "SELECT * FROM codelist2"
    cursor.execute(select1)
    fetch = cursor.fetchall()
    print(fetch)
    db.close()
    for i in fetch:
        # sem3.acquire()
        print(i[0])
        attempts = 0
        success = False
        # while attempts < 3 and not success:
        # try:
        if real(i[0]):
            db = getdb()
            cursor = db.cursor()
            ins = "REPLACE INTO codelist3(code) VALUES (%s)" % i[0]
            cursor.execute(ins)
            db.commit()
            db.close()
            #     success = True
            # except:
            #     attempts += 1
            #     sleep(3)
            #     if attempts == 3:
            #         break


