import pyecharts.options as opts
from pyecharts.charts import Kline
import tushare as ts
import imgkit
from PIL import Image
import cv2
import pandas as pd
import datetime as dt


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
        .render("kline.html")  # 保存本地
    )
    path_wkimg = r'D:\wkhtmltopdf\bin\wkhtmltoimage.exe'  # 工具路径
    cfg = imgkit.config(wkhtmltoimage=path_wkimg)
    # 1、将html文件转为图片
    imgkit.from_file("C:\\Users\\24566\\PycharmProjects\\pythonProject2\\kline.html", 'cal.jpg', config=cfg)
    img = Image.open("C:\\Users\\24566\\PycharmProjects\\pythonProject2\\cal.jpg")
    region = img.crop((100, 68, 816, 449))
    region.save('jl.jpg')
    src = cv2.imread("C:\\Users\\24566\\PycharmProjects\\pythonProject2\\jl.jpg")
    result = cv2.resize(src, (300, 150))
    result = cv2.flip(result, 1)
    cv2.imwrite("C:\\Users\\24566\\PycharmProjects\\pythonProject2\\train\\w\\{}_{}.jpg".format(ts_code,
                                                                                                        end_date),
                result)


if __name__ == "__main__":
    # tushare的token
    token = 'f558cbc6b24ed78c2104e209a8a8986b33ec66b7c55bcfa2f46bc108'
    datas = pd.read_csv("./train/csv/w.csv")
    print(len(datas))
    # 股票代码（tushare格式的）
    for i in range(99, len(datas)):
        data = datas.iloc[i, :]
        tscode = "%06d" % data[0]
        if data[0] < 301397:
            ts_code = '{}.SZ'.format(tscode)
        elif 689010 > data[0] > 430685:
            ts_code = '{}.SH'.format(tscode)
        else:
            ts_code = '{}.BJ'.format(tscode)
        end_date = data[1]
        a = dt.datetime.strptime(str(end_date), '%Y%m%d')
        start_date = a - dt.timedelta(days=61)
        # 开始日期（tushare格式的）例：20220101
        start_date = dt.datetime.strftime(start_date, '%Y%m%d')
        end_date = int(end_date)
        start_date = int(start_date)

        # 画日k线
        daily_kline(token, ts_code, start_date, end_date)
        print("{}_{}_{}".format(i, ts_code, end_date))
