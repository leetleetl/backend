import tushare as ts
import datetime as dt

from Sell.Liuxiang import liuxiang
from Sell.Kongpan import chiGu
from Sell.nowData import getNow


def huitiao(ts_code, buydate):
    for j in range(6 - len(ts_code)):
        ts_code = "0" + ts_code
    if int(ts_code) < 301397:
        ts_code = '{}.SZ'.format(ts_code)
    elif 689010 > int(ts_code) > 430685:
        ts_code = '{}.SH'.format(ts_code)
    else:
        ts_code = '{}.BJ'.format(ts_code)
    token = 'f558cbc6b24ed78c2104e209a8a8986b33ec66b7c55bcfa2f46bc108'
    pro = ts.pro_api(token)
    start_date = buydate
    end_date0 = dt.date.today() - dt.timedelta(days=1)
    end_date = dt.date.strftime(end_date0, '%Y%m%d')
    a = dt.datetime.strptime(str(end_date0), '%Y-%m-%d')
    # start_date = a - dt.timedelta(days=61)
    # start_date = dt.datetime.strftime(start_date, '%Y%m%d')

    df = ts.pro_bar(ts_code=ts_code, start_date=start_date, end_date=end_date, ma=[5, 10, 30])
    shizhi = pro.bak_daily(ts_code=ts_code)
    shizhi = shizhi.values.tolist()[0][22]
    df = df.values.tolist()
    nowD = getNow(ts_code[0:6])
    # 出现5% 以上大阳线后，后几日又回调，回调幅度已超过大阳线的1/3
    # 以上（回调收盘价低于大阳线收盘价，且下降幅度达大阳线K线实体长度的1/3
    # 以上），减仓一半。如回调幅度达到大阳线K线实体长度100 % 以上（即回调收盘价低于大阳线开盘价），全部清仓。
    # 跌破最近一根大阳线
    ysdayPrice = nowD[0]
    if len(df) > 1:
        for i in df:
            if i[8] > 5:
                # if 1 - ysdayPrice / i[5] > i[8]:
                #     return 1
                # elif 1 - ysdayPrice / i[5] > i[8] * 0.3:
                #     return 0.5...
                if ysdayPrice / i[2] < 0.97:
                    return 1
                break
        dfmax = max(df, key=lambda x: x[5])[5]
        # 亏损百分之10
        if ysdayPrice / dfmax < 0.9:
            return 1

        # 跌破5,10,30日均线，最近一日最低点
        if ysdayPrice / df[0][-2] < 0.97:
            return 1
        if ysdayPrice / df[0][4] < 0.97:
            return 1
        if ysdayPrice / df[0][-6] < 0.97:
            return 1
        if ysdayPrice / df[0][-4] < 0.97:
            return 1

        yearago_date = a - dt.timedelta(days=365)
        yearago_date = dt.datetime.strftime(yearago_date, '%Y%m%d')
        dfyear = ts.pro_bar(ts_code=ts_code, start_date=yearago_date, end_date=end_date)
        dfyear = dfyear.values.tolist()
        dfmin = min(dfyear, key=lambda x: x[5])[5]

        # 目前股价相比一年来的最低点已涨幅达300 % 以上，前一日出现涨停板后当日收盘没有封死涨停板
        if ysdayPrice / dfmin > 4:
            if df[0][8] == 10.0 and nowD[2] != 10.0:
                return 2

        # 巨量(当日的成交量占其流通盘10 % 以上) + 股价已高于5日均线价格达15 % 以上
        juliang = False
        if nowD[6] / shizhi > 0.1:
            juliang = True
        if ysdayPrice / df[0][-6] > 1.15 and juliang:
            return 3

        # 巨量(当日的成交量占其流通盘10 % 以上) + 高开大阴线 / 十字线 / 长上影线（上影线占K线实体长度50 % 以上）
        if (nowD[2] - max(nowD[0], nowD[1])) / abs(nowD[0] - nowD[1]) > 0.5 and juliang:
            return 4

        # 高位出货形态
        gaowei = False
        if ysdayPrice / dfmin > 2:
            gaowei = True
        if gaowei:
            # 长上下影线
            if (nowD[2] - max(nowD[0], nowD[1])) / abs(nowD[0] - nowD[1]) > 0.5:
                return 5

            # 连续出现巨阳线（百亿市值以上的6 % 以上涨幅的阳线，百亿市值以下的8 % 以上的阳线），且最后一根阳线有上影线（上影线长度达K线实体20 % 以上）
            shizhi = pro.daily_basic(ts_code=ts_code, start_date=start_date, end_date=end_date, fields='total_mv')
            if len(df) > 2:
                if (nowD[2] - max(nowD[0], nowD[1])) / abs(nowD[0] - nowD[1]) > 0.2:
                    if shizhi > 100000.0:
                        if df[1][8] > 6 and df[0][8] > 6:
                            return 6
                    else:
                        if df[1][8] > 8 and df[0][8] > 8:
                            return 6

            # 大阳线之后第二天走弱
            if shizhi > 100000.0:
                if df[0][8] > 6 and nowD[4] < 0 and nowD[1] < df[0][5]:
                    return 7
            else:
                if df[0][8] > 8 and nowD[4] < 0 and nowD[1] < df[0][5]:
                    return 7

            # 平顶线
            if nowD[2] - df[0][4] < nowD[0] * 0.2:
                return 8

        # 跌破趋势线
        dfminqushi = min(df, key=lambda x: x[5])
        dfqushi = ts.pro_bar(ts_code=ts_code, start_date=dfminqushi[1], end_date=end_date)
        dfqushi = dfqushi.values.tolist()
        i = 2
        while i < len(dfqushi) - 2:
            if dfqushi[i][8] < 0:
                j = i
                while j < len(dfqushi) - 2 and dfqushi[j][8] < 0:
                    j += 1
                if (dfqushi[j - 1][5] - dfminqushi[5]) / j > (ysdayPrice - dfminqushi[5]) / len(dfqushi):
                    return 9
                break
            i += 1

    # 股票已变为轻度控盘，且近5日内大资金持续净流出
    if len(df) > 4:
        if chiGu(ts_code) and liuxiang(ts_code):
            return 10

    return 0


