import pandas as pd
import requests
import tushare as  ts


def gen_secid(stock_code: str) -> str:
    """
    生成东方财富专用的secid

    Parameters
    ----------
    stock_code: 6 位股票代码

    Return
    ------
    str : 东方财富给股票设定的一些东西
    """
    if int(stock_code) < 301381:
        return f'0.{stock_code}'
    elif 688982 > int(stock_code) > 430685:
        return f'1.{stock_code}'
    else:
        return f'0.{stock_code}'
    return f'1.{stock_code}'


def get_history_bill(stock_code: str) -> pd.DataFrame:
    """
    获取多日单子数据
    -
    Parameters
    ----------
    stock_code: 6 位股票代码

    Return
    ------
    DataFrame : 包含指定股票的历史交易日单子数据（大单、超大单等）

    """
    EastmoneyHeaders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'http://quote.eastmoney.com/center/gridlist.html',
    }
    EastmoneyBills = {
        'f51': '日期',
        'f52': '主力净流入',
        'f53': '小单净流入',
        'f54': '中单净流入',
        'f55': '大单净流入',
        'f56': '超大单净流入',
        'f57': '主力净流入占比',
        'f58': '小单流入净占比',
        'f59': '中单流入净占比',
        'f60': '大单流入净占比',
        'f61': '超大单流入净占比',
        'f62': '收盘价',
        'f63': '涨跌幅'

    }
    fields = list(EastmoneyBills.keys())
    columns = list(EastmoneyBills.values())
    fields2 = ",".join(fields)
    secid = gen_secid(stock_code)
    params = (
        ('lmt', '100000'),
        ('klt', '101'),
        ('secid', secid),
        ('fields1', 'f1,f2,f3,f7'),
        ('fields2', fields2),

    )
    params = dict(params)
    url = 'http://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get'
    json_response = requests.get(url,
                                 headers=EastmoneyHeaders, params=params).json()
    data = json_response.get('data')
    if data is None:
        if secid[0] == '0':
            secid = f'1.{stock_code}'
        else:
            secid = f'0.{stock_code}'
        params['secid'] = secid

        json_response: dict = requests.get(
            url, headers=EastmoneyHeaders, params=params).json()
        data = json_response.get('data')
    if data is None:
        print('股票代码:', stock_code, '可能有误')
        return pd.DataFrame(columns=columns)
    if json_response is None:
        return
    data = json_response['data']
    klines = data['klines']
    rows = []
    for _kline in klines[len(klines) - 20:len(klines)]:
        kline = _kline.split(',')
        rows.append(kline)
    df = pd.DataFrame(rows, columns=columns)

    return df


def liuxiang(ts_code):
    # 股票代码
    stock_code = ts_code[0:6]
    # 调用函数获取股票历史单子数据（有天数限制）
    df1 = get_history_bill(stock_code)
    # 保存数据到 csv 文件中
    dfList = df1.values.tolist()
    fiveBig = 0.0
    fiveMain = 0.0
    twentyBig = 0.0
    twentyMain = 0.0
    for i in range(5):
        fiveBig += float(dfList[-i - 1][5])
        fiveMain += float(dfList[-i - 1][1])
    for i in range(20):
        twentyBig += float(dfList[-i - 1][5])
        twentyMain += float(dfList[-i - 1][1])
    if (fiveBig > 0 and fiveMain > 0) or (twentyBig > 0 and twentyMain > 0):
        return True
    return False
    # df.to_csv(f'{stock_code}.csv', index=None, encoding='utf-8-sig')
    # print(stock_code, f'的历史单子数据已保存到文件 {stock_code}.csv 中')

