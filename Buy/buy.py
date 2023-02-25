import tushare as ts
import datetime as dt
from Buy.spiner import chiGu
from time import sleep
from Buy.LiuXiang import liuxiang


def buyDay(ts_code):
    if int(ts_code) < 301397:
        ts_code = '{}.SZ'.format(ts_code)
    elif 689010 > int(ts_code) > 430685:
        ts_code = '{}.SH'.format(ts_code)
    else:
        ts_code = '{}.BJ'.format(ts_code)

    token = 'f558cbc6b24ed78c2104e209a8a8986b33ec66b7c55bcfa2f46bc108'
    pro = ts.pro_api(token)
    basic = pro.stock_basic(**{
        "ts_code": ts_code,
        "name": "",
        "exchange": "",
        "market": "",
        "is_hs": "",
        "list_status": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "name",
        "list_date"
    ])
    ts.set_token(token)

    end_date0 = dt.date.today() - dt.timedelta(days=1)
    a = dt.datetime.strptime(str(end_date0), '%Y-%m-%d')
    start_date = a - dt.timedelta(days=61)
    # 开始日期（tushare格式的）例：20220101
    start_date = dt.date.strftime(start_date, '%Y%m%d')
    end_date = dt.date.strftime(end_date0, '%Y%m%d')
    df = ts.pro_bar(ts_code=ts_code, start_date=start_date, end_date=end_date, ma=[5, 10, 30])
    dfList = df.values.tolist()
    print(ts_code)

    # 四连阳判定:七天内有一次四连阳判定为真
    fourRed = False
    for i in range(15):
        if dfList[i][8] > 0 and dfList[i + 1][8] > 0 and dfList[i + 2][8] > 0 and dfList[i + 3][8] > 0:
            fourRed = True
            break
    if not fourRed:
        return False

    # 成交量温和放大判定:找一个四天有三天在跌的时间，然后找这四天的最后一天作为拐点，拐点往前一周求均值，拐点往后到今天求一个均值，拐点往后的均值大于拐点往前的均值百分之50就判定通过
    vol = False
    for i in range(40):
        countchange = 0
        for j in range(4):
            if dfList[i + j][8] < 0:
                countchange += 1
        if countchange > 2:
            frontvol = 0
            behindvol = 0
            for j in range(7):
                frontvol += dfList[i + j][9]
            for j in range(i + 1):
                behindvol += dfList[j][9]
            if frontvol != 0:
                frontvol = frontvol / 7
            if behindvol != 0:
                behindvol = behindvol / i + 1
            if behindvol / frontvol > 1.5:
                vol = True
            break
    # 阳线成交量总和大于阴线成交量总和20 % 以上。并且阳线数量大于阴线数量20 % 以上。
    if vol:
        redvol = 0
        greenvol = 0
        redcount = 0
        greencount = 0
        for i in range(30):
            if dfList[i][8] > 0:
                redcount += 1
                redvol += dfList[i][9]
            else:
                greencount += 1
                greenvol += dfList[i][9]
        if redvol / greenvol < 1.2 or redcount / greencount < 1.2:
            return False
    else:
        return False
    # 近15日，一半以上时间的阳线成交量比昨日成交量大；如果是阴线，一半以上时间的阴线成交量比昨日成交量少。
    if vol:
        redcount1 = 0
        redcount2 = 0
        greencount1 = 0
        greencount2 = 0
        for i in range(15):
            if dfList[i][8] > 0 and dfList[i + 1][9] < dfList[i][9]:
                redcount1 += 1
            elif dfList[i][8] > 0 and dfList[i + 1][9] > dfList[i][9]:
                redcount2 += 1
            elif dfList[i][8] < 0 and dfList[i + 1][9] < dfList[i][9]:
                greencount1 += 1
            else:
                greencount2 += 1
        if redcount1 / redcount2 < 1 or greencount1 / greencount2 > 1:
            return False


    # 均线多头排列判定：当下7日均线>14日均线>月均线，判定为真
    ma = False
    maList = dfList[0]
    if maList[-6] > maList[-4] > maList[-2]:
        ma = True
    if not ma:
        return False

    # 控盘判定：完全控盘与中度控盘，判定为真
    attempts = 0
    success = False
    chigu = False
    while attempts < 10 and not success:
        try:
            chigu = chiGu(ts_code)
            success = True
        except:
            attempts += 1
            sleep(3)
            if attempts == 10:
                break

    # 资金流判定：5日超大单和主力为净流入，或20日超大单和主力为净流入，判定为真
    attempts = 0
    success = False
    lx = False
    while attempts < 10 and not success:
        try:
            lx = liuxiang(ts_code)
            success = True
        except:
            attempts += 1
            sleep(3)
            if attempts == 10:
                break

    # 高位判定：一年内涨幅超100%判定为高位
    highState = True
    yearago_date = a - dt.timedelta(days=365)
    yearago_date = dt.datetime.strftime(yearago_date, '%Y%m%d')
    # 防止找不到昨天的数据
    threedays_dates = a - dt.timedelta(days=3)
    threedays_dates = dt.datetime.strftime(threedays_dates, '%Y%m%d')
    dfyearago = ts.pro_bar(ts_code=ts_code, start_date=yearago_date, end_date=end_date)
    dfyearago = dfyearago.values.tolist()
    dfmin = min(dfyearago, key=lambda x: x[5])[5]
    dftoday = ts.pro_bar(ts_code=ts_code, start_date=threedays_dates, end_date=end_date)
    if dftoday.values.tolist()[0][5] / dfmin > 2.0:
        highState = False

    # 低位判定： 半年内跌幅超50%判定为低位
    lowState = True
    halfyearago_date = a - dt.timedelta(days=182)
    halfyearago_date = dt.datetime.strftime(halfyearago_date, '%Y%m%d')
    dfhalfyearago = ts.pro_bar(ts_code=ts_code, start_date=halfyearago_date, end_date=end_date)
    dfhalfyearago = dfhalfyearago.values.tolist()
    dfmax = max(dfhalfyearago, key=lambda x: x[5])[5]
    if dftoday.values.tolist()[0][5] / dfmax < 0.5:
        lowState = False

    # ST判定
    st = True
    name = basic.values.tolist()[0][0]
    if name[0:2] == 'ST':
        st = False

    # 次新判定:一年内上市判定为次新
    cixin = True
    shangshi = basic.values.tolist()[0][1]
    dShangshi = dt.date(int(shangshi[0:4]), int(shangshi[4:6]), int(shangshi[6:8]))
    interval = end_date0 - dShangshi
    if interval.days < 365:
        cixin = False

    # print(fourRed, vol, ma, chigu, highState, lowState, cixin, lx, st)
    if fourRed and vol and ma and (chigu or lx) and st and highState:
        return True
    return False

