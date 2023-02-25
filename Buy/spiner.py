import re
from requests_html import HTMLSession
import tushare as ts

session = HTMLSession()


def get_chiGu(ts_code):
    url = 'https://data.eastmoney.com/stockcomment/stock/{}.html'.format(ts_code[0:6])
    r = session.get(url)
    r.html.render()
    html = r.html.html
    img_list = re.findall('<span id="dv_empty0">.*</span>', html)
    return img_list[0][-11:-7]


def chiGu(ts_code):
    chigu = False
    chigu1 = get_chiGu(ts_code)
    print(chigu1)
    if chigu1 == '完全控盘' or chigu1 == '中度控盘':
        chigu = True
    return chigu


