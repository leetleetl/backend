import os
import shutil
import threading

import pyecharts.options as opts
from pyecharts.charts import Kline
import tushare as ts
import imgkit
from PIL import Image
import cv2
import pandas as pd
import datetime as dt
from time import sleep
import sys

sys.path.append("..")
from sql.configSql import getdb

sem = threading.Semaphore(15)


def daily_kline(token, ts_code, start_date, end_date):
    # 调用获取股票交易日数据（x轴数据）
    date = get_tushare_kline_date(token, ts_code, start_date, end_date)
    # 调用获取股票open,close,low,high数据（y轴数据）
    data = get_tushare_kline_data(token, ts_code, start_date, end_date)
    # #调用画图函数
    plot_kline(date, data, ts_code, end_date)


def get_tushare_kline_date(token, ts_code, start_date, end_date):
    pro = ts.pro_api(token)
    # 拉取日期数据
    date = pro.daily(**{
        "ts_code": ts_code,
        "trade_date": "",
        "start_date": start_date,
        "end_date": end_date,
        "offset": "",
        "limit": ""
    }, ascending=True, fields=[
        "trade_date"
    ])
    date.values.tolist()
    return date


def get_tushare_kline_data(token, ts_code, start_date, end_date):
    pro = ts.pro_api(token)
    # 拉取k线数据
    data = pro.daily(**{
        "ts_code": ts_code,
        "trade_date": "",
        "start_date": start_date,
        "end_date": end_date,
        "offset": "",
        "limit": ""
    }, fields=[
        "open",
        "high",
        "low",
        "close"
    ])
    data.values.tolist()
    return data


def plot_kline(date, data, ts_code, end_date):
    c = (
        Kline()
        .add_xaxis(date.values.tolist())
        .add_yaxis(
            "kline",
            data[['open', 'close', 'low', 'high']].values.tolist(),
            itemstyle_opts=opts.ItemStyleOpts(  # 系列配置项-图元样式
                color="#ec0000",  # 涨
                color0="#00da3c",  # 跌
                border_color="#8A0000",  # 涨外框
                border_color0="#008F28",  # 跌外框
            ),
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True),  # 全局-x坐标刻度不会强制包含零刻度
            yaxis_opts=opts.AxisOpts(  # 全局-y轴
                is_scale=True,  # y坐标刻度不会强制包含零刻度
                splitarea_opts=opts.SplitAreaOpts(  # 系列配置项-分割线
                    is_show=False  # 分割线 线风格-系列配置项-线样式-分割线透明度
                ),
            ),
            title_opts=opts.TitleOpts(title="Kline-ItemStyle"),  # 全局-标题-标题
        )
        .render("./html/{}.html".format(ts_code))  # 保存本地
    )
    # https: // wkhtmltopdf.org / downloads.html
    # r'/usr/local/bin/wkhtmltoimage'
    path_wkimg = r'./wkhtmltoimage.exe'  # 工具路径
    cfg = imgkit.config(wkhtmltoimage=path_wkimg)
    # 1、将html文件转为图片
    imgkit.from_file("./html/{}.html".format(ts_code), "./toPic/{}.jpg".format(ts_code), config=cfg)
    img = Image.open("./toPic/{}.jpg".format(ts_code))
    region = img.crop((100, 68, 816, 449))
    region.save("./tran/{}.png".format(ts_code))
    src = cv2.imread("./tran/{}.png".format(ts_code))
    result = cv2.resize(src, (300, 150))
    result = cv2.flip(result, 1)
    cv2.imwrite(r"./predict/picture/{}_{}.png".format(ts_code, end_date),
                result)
    os.remove("./html/{}.html".format(ts_code))
    os.remove("./toPic/{}.jpg".format(ts_code))
    os.remove("./tran/{}.png".format(ts_code))


def removeDir(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)


def drawPic(tscode, token, days):
    attempts = 0
    success = False
    while attempts < 5 and not success:
        try:
            # 股票代码（tushare格式的）
            end_date = dt.date.today() - dt.timedelta(days=1)
            a = dt.datetime.strptime(str(end_date), '%Y-%m-%d')
            if days == 60:
                start_date = a - dt.timedelta(days=61)
            elif days == 90:
                start_date = a - dt.timedelta(days=92)
            else:
                start_date = a - dt.timedelta(days=183)
            # 开始日期（tushare格式的）例：20220101
            start_date = dt.date.strftime(start_date, '%Y%m%d')
            end_date = dt.date.strftime(end_date, '%Y%m%d')
            end_date = int(end_date)
            start_date = int(start_date)

            # 画日k线
            daily_kline(token, tscode, start_date, end_date)
            success = True
            sem.release()
        except:
            attempts += 1
            sleep(5)
            if attempts == 5:
                print("{} false".format(tscode))
                db = getdb()
                cursor = db.cursor()
                ins = "REPLACE INTO falsecode(code) VALUES (%s)" % tscode[2:6]
                cursor.execute(ins)
                db.commit()
                cursor.close()
                db.close()
                sem.release()
                break


def draw(begin, days):
    # tushare的token
    token = 'f558cbc6b24ed78c2104e209a8a8986b33ec66b7c55bcfa2f46bc108'
    pro = ts.pro_api(token)
    datas = pro.stock_basic(fields=[
        "ts_code"
    ])
    print(len(datas))
    filepath1 = "./html"
    filepath3 = "./tran"
    filepath2 = "./predict/picture"
    filepath4 = "./toPic"
    if begin == 0:
        removeDir(filepath1)
        removeDir(filepath3)
        removeDir(filepath2)
        removeDir(filepath4)
        db = getdb()
        cursor = db.cursor()
        del1 = "DELETE FROM falsecode"
        cursor.execute(del1)
        db.commit()
        cursor.close()
        db.close()
        n = len(os.listdir(filepath2))
        if n < len(datas):
            for i in datas.values.tolist()[n:]:
                sem.acquire()
                thr = threading.Thread(target=drawPic, args=(i[0], token, days))
                thr.start()
    elif begin == 2:
        removeDir(filepath1)
        removeDir(filepath3)
        removeDir(filepath2)
        removeDir(filepath4)
        db = getdb()
        cursor = db.cursor()
        del1 = "DELETE FROM falsecode"
        cursor.execute(del1)
        db.commit()
        select = "SELECT * FROM codelist1"
        cursor.execute(select)
        fetch = cursor.fetchall()
        db.commit()
        cursor.close()
        db.close()
        for i in fetch:
            ts_code = i[0]
            for j in range(6 - len(ts_code)):
                ts_code = "0" + ts_code
            if int(ts_code) < 301397:
                ts_code = '{}.SZ'.format(ts_code)
            elif 689010 > int(ts_code) > 430685:
                ts_code = '{}.SH'.format(ts_code)
            else:
                ts_code = '{}.BJ'.format(ts_code)
            sem.acquire()
            thr = threading.Thread(target=drawPic, args=(ts_code, token, days))
            thr.start()
    else:
        db = getdb()
        cursor = db.cursor()
        select = "SELECT * FROM falsecode"
        cursor.execute(select)
        fetch = cursor.fetchall()
        del1 = "DELETE FROM falsecode"
        cursor.execute(del1)
        db.commit()
        cursor.close()
        db.close()
        for i in fetch:
            sem.acquire()
            ts_code = i[0]
            for j in range(6 - len(ts_code)):
                ts_code = "0" + ts_code
            if int(ts_code) < 301397:
                ts_code = '{}.SZ'.format(ts_code)
            elif 689010 > int(ts_code) > 430685:
                ts_code = '{}.SH'.format(ts_code)
            else:
                ts_code = '{}.BJ'.format(ts_code)
            thr = threading.Thread(target=drawPic, args=(ts_code, token, days))
            thr.start()
        n = len(os.listdir(filepath2))
        if n < len(datas):
            for i in datas.values.tolist()[n:]:
                sem.acquire()
                thr = threading.Thread(target=drawPic, args=(i[0], token, days))
                thr.start()

# draw(0)
