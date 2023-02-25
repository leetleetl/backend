import tushare as ts
import datetime as dt
from Sell.nowData import getNow


def continuebuy(ts_code, buydate):
    for j in range(6 - len(ts_code)):
        ts_code = "0" + ts_code
    if int(ts_code) < 301397:
        ts_code = '{}.SZ'.format(ts_code)
    elif 689010 > int(ts_code) > 430685:
        ts_code = '{}.SH'.format(ts_code)
    else:
        ts_code = '{}.BJ'.format(ts_code)
    token = 'f558cbc6b24ed78c2104e209a8a8986b33ec66b7c55bcfa2f46bc108'
    ts.set_token(token)
    start_date = buydate
    end_date0 = dt.date.today() - dt.timedelta(days=1)
    end_date = dt.datetime.strftime(end_date0, '%Y%m%d')
    # a = dt.datetime.strptime(str(end_date0), '%Y-%m-%d')
    # start_date = a - dt.timedelta(days=61)
    # start_date = dt.datetime.strftime(start_date, '%Y%m%d')
    if int(end_date) - int(start_date) < 3:
        return False
    df = ts.pro_bar(ts_code=ts_code, start_date=start_date, end_date=end_date, ma=[5, 10, 30])

    df = df.values.tolist()


    nowD = getNow(ts_code[0:6])
    if df[0][8] < 0.0 and 0 < nowD[4] and nowD[8] > 0 and nowD[9] > 0:
        if nowD[3] < df[0][-2] < nowD[2] or nowD[3] < df[0][-4] < nowD[2] or nowD[3] < df[0][-6] < nowD[2]:
            return True
        if df[0][5] / df[1][4] > 0.97:
            return True
        for i in df[1:]:
            if i[8] > 5:
                # if 1 - ysdayPrice / i[5] > i[8]:
                #     return 1
                # elif 1 - ysdayPrice / i[5] > i[8] * 0.3:
                #     return 0.5
                if i[0][5] / i[2] > 0.97:
                    return True
    return False

