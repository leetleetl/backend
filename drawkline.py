import tushare as ts
# import talib as ta
import numpy as np
import pandas as pd
from pyecharts.charts import Kline, Line
from pyecharts import options as opts
import datetime as dt
from sql.configSql import getdb


def plot_kline(data, name, buy_sell):
    # buy_sell 是一个包含四个列表的列表
    # [['2022-07-07', '2022-07-13', '2022-08-04', '2022-08-15', '2022-08-26', '2022-11-01', '2022-12-07', '2022-12-19'],
    # [8.31, 8.74, 9.77, 9.01, 8.51, 8.02, 8.16, 7.95],
    # ['2022-07-12', '2022-07-14', '2022-08-05', '2022-08-19', '2022-10-20', '2022-12-06', '2022-12-08', '2023-01-06'],
    # [8.56, 9.1, 9.28, 9.6, 2, 8.37, 8.1, 8.14, 8.66]]
    # 分别是买入日期，买入时高价，卖出日期，卖出时高价，其中高价用来做买卖标记的纵坐标

    # name就是股票名

    # data是取tushare中的数据，并计算添加了画图需要的MA30，UP布林线，LOW布林线，MIDDLE布林线数据
    # 修改了data中global_data各式
    # global_data['trade_date'] = pd.to_datetime(global_data['trade_date'], format='%Y%m%d').apply(lambda x: x.strftime('%Y-%m-%d'))
    # global_data = global_data.set_index('trade_date')
    buy_date = buy_sell[0]
    buy_high = buy_sell[1]
    sell_date = buy_sell[2]
    sell_high = buy_sell[3]
    kline = (
        Kline(init_opts=opts.InitOpts(width="1350px", height="500px"))  # 设置画布大小
        .add_xaxis(xaxis_data=list(data.index))  # 将原始数据的index转化为list作为横坐标
        .add_yaxis(series_name="k线", y_axis=data[["open", "close", "low", "high"]].values.tolist(),
                   # 纵坐标采用OPEN、CLOSE、LOW、HIGH，注意顺序
                   itemstyle_opts=opts.ItemStyleOpts(color="#c61328", color0="#223b24"), )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=True, pos_bottom=0, pos_left="center", orient='horizontal'),
            datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=False,
                    type_="inside",
                    xaxis_index=[0],
                    range_start=50,
                    range_end=100,
                ),
                opts.DataZoomOpts(
                    is_show=False,
                    xaxis_index=[0],
                    type_="slider",
                    pos_top="10%",
                    range_start=50,
                    range_end=100,
                ),
            ],
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                axis_pointer_type="cross",
                background_color="rgba(245, 245, 245, 0.8)",
                border_width=1,
                border_color="#ccc",
                textstyle_opts=opts.TextStyleOpts(color="#000"),
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_show=False,
                dimension=2,
                series_index=5,
                is_piecewise=True,
                pieces=[
                    {"value": 1, "color": "#00da3c"},
                    {"value": -1, "color": "#ec0000"},
                ],
            ),
            axispointer_opts=opts.AxisPointerOpts(
                is_show=True,
                link=[{"xAxisIndex": "all"}],
                label=opts.LabelOpts(background_color="#777"),
            ),
            brush_opts=opts.BrushOpts(
                x_axis_index="all",
                brush_link="all",
                out_of_brush={"colorAlpha": 0.1},
                brush_type="lineX",
            ),
            title_opts=opts.TitleOpts(
                title=name,
                pos_left='center',
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=30
                )),
        )
    )

    line = (Line()
    .add_xaxis(xaxis_data=list(data.index))
    # .add_yaxis(
    #     series_name="UP",
    #     y_axis=data["upper"].tolist(),
    #     # xaxis_index=1,
    #     # yaxis_index=1,
    #     label_opts=opts.LabelOpts(is_show=False),
    # ).add_yaxis(
    #     series_name="MID",
    #     y_axis=data["middle"].tolist(),
    #     # xaxis_index=1,
    #     # yaxis_index=1,
    #     label_opts=opts.LabelOpts(is_show=False),
    # ).add_yaxis(
    #     series_name="LOW",
    #     y_axis=data["lower"].tolist(),
    #     # xaxis_index=1,
    #     # yaxis_index=1,
    #     label_opts=opts.LabelOpts(is_show=False),
    .add_yaxis(
        series_name="MA30",
        y_axis=data["ma30"].tolist(),
        # xaxis_index=1,
        # yaxis_index=1,
        label_opts=opts.LabelOpts(is_show=False),
    ))

    for i in range(0, len(buy_date)):
        kline.add_yaxis(
            series_name="买卖",
            y_axis="",
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(coord=[buy_date[i], buy_high[i]], name='test', value='买',
                                       itemstyle_opts={'color': '#08a2f9'}),
                ]
            ), )
    for i in range(0, len(sell_date)):
        kline.add_yaxis(
            series_name="买卖",
            y_axis="",
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(coord=[sell_date[i], sell_high[i]], name='test', value='卖',
                                       itemstyle_opts={'color': '#f75d06'}),
                ]
            ), )

    kline.overlap(line)
    kline.render("kline.html")
    return kline
    #     #导出成html文件


def letdraw(ts_code):
    if int(ts_code) < 301397:
        ts_code = '{}.SZ'.format(ts_code)
    elif 689010 > int(ts_code) > 430685:
        ts_code = '{}.SH'.format(ts_code)
    else:
        ts_code = '{}.BJ'.format(ts_code)
    pro = ts.pro_api('f558cbc6b24ed78c2104e209a8a8986b33ec66b7c55bcfa2f46bc108')
    end_date0 = dt.date.today()
    a = dt.datetime.strptime(str(end_date0), '%Y-%m-%d')
    start_date = a - dt.timedelta(days=365)
    # 开始日期（tushare格式的）例：20220101
    start_date = dt.date.strftime(start_date, '%Y%m%d')
    end_date = dt.date.strftime(end_date0, '%Y%m%d')
    global_data = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
    global_data = global_data.iloc[::-1]
    # global_data['upper'], global_data['middle'], global_data['lower'] = ta.BBANDS(
    #     global_data.close.values,
    #     timeperiod=20,
    #     nbdevup=2,
    #     nbdevdn=2,
    #     matype=0)
    # global_data['upper'] = round(global_data['upper'], 2)
    # global_data['middle'] = round(global_data['middle'], 2)
    # global_data['lower'] = round(global_data['lower'], 2)
    # global_data['rsi'] = ta.RSI(global_data.close.values, timeperiod=6)
    # global_data['rsi'] = round(global_data['rsi'], 4)
    # global_data['rsi_var'] = global_data['rsi'].diff() / np.roll(global_data['rsi'], shift=1)
    # global_data['rsi_var'] = round(global_data['rsi_var'], 4)
    # global_data['low-lowboll'] = global_data['low'] - global_data['lower']
    # global_data['high-highboll'] = global_data['high'] - global_data['upper']
    # global_data['high-mid'] = global_data['high'] - global_data['middle']
    # global_data['mid-low'] = global_data['middle'] - global_data['low']
    global_data['close-open'] = global_data['close'] - global_data['open']
    # global_data['yes_close-mid'] = global_data['pre_close'] - global_data['middle']
    # global_data['mid-close'] = global_data['middle'] - global_data['close']
    global_data['ma5'] = round(global_data['close'].rolling(5).mean(), 2)
    global_data['ma10'] = round(global_data['close'].rolling(10).mean(), 2)
    global_data['ma20'] = round(global_data['close'].rolling(20).mean(), 2)
    global_data['ma30'] = round(global_data['close'].rolling(30).mean(), 2)

    ts_code1 = ts_code[0:6]
    while ts_code1[0] == '0':
        ts_code1 = ts_code1[1:len(ts_code)]
    db = getdb()
    cursor = db.cursor()
    cursor.execute(
        'SELECT  `buyDate` from buy where code = (%s) ',
        (ts_code1,)
    )
    fetch1 = cursor.fetchall()
    cursor.execute(
        'SELECT  `buyDate` from sell where code = (%s) ',
        (ts_code1,)
    )
    fetch2 = cursor.fetchall()
    cursor.close()
    db.close()
    pro = ts.pro_api('f558cbc6b24ed78c2104e209a8a8986b33ec66b7c55bcfa2f46bc108')
    buylist = []
    buyprice = []
    selllist = []
    sellprice = []
    for i in fetch1:
        global_data1 = pro.daily(ts_code=ts_code, trade_date=i[0])
        global_data1 = global_data1.values.tolist()
        if len(global_data1) != 0:
            buylist.append(i[0])
            buyprice.append(global_data1[0][3])
    for i in fetch2:
        global_data2 = pro.daily(ts_code=ts_code, trade_date=i[0])
        global_data2 = global_data2.values.tolist()
        if len(global_data2) != 0:
            selllist.append(i[0])
            sellprice.append(global_data2[0][3])
    buysell = [buylist, buyprice, selllist, sellprice]
    print(buysell)
    # global_data['trade_date'] = pd.to_datetime(global_data['trade_date'], format='%Y%m%d').apply(
    #     lambda x: x.strftime('%Y-%m-%d'))
    global_data = global_data.set_index('trade_date')
    plot_kline(global_data, ts_code, buysell)
