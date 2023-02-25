from requests_html import HTMLSession
import re

session = HTMLSession()


def juLiang(ts_code):
    if int(ts_code[0:6]) < 301397:
        ts_code = 'sz{}'.format(ts_code)
    elif 689010 > int(ts_code[0:6]) > 430685:
        ts_code = 'sh{}'.format(ts_code)
    else:
        ts_code = 'bj{}'.format(ts_code)
    url = 'https://finance.sina.com.cn/realstock/company/{}/nc.shtml'.format(ts_code)
    print(url)
    r = session.get(url)
    r.html.render()
    # success = True
    html2 = r.html.html
    print(html2)
    pattern0 = re.compile(
        '<div class="other" id="hqDetails">.*?<tr>.*?<tr>.*?<td>(.*?)</td>.*?<tr>.*?<tr>.*?<td>.*?<td>(.*?)</td>'
        , re.S)
    jiaoYiELiutong = pattern0.findall(html2)
    print(jiaoYiELiutong)
    # 浜垮厓 亿元 浜� 亿
    jiaoYiE = jiaoYiELiutong[0][0]
    if jiaoYiE[-3:] == '浜垮厓':
        jiaoYiE = float(jiaoYiE[0:-3])
    elif jiaoYiE[-3:] == '涓囧厓':
        jiaoYiE = float(jiaoYiE[0:-3]) / 10000
    liutong = jiaoYiELiutong[0][1]
    liutong = float(liutong[0:-2])
    print(jiaoYiE)
    print(liutong)
    if jiaoYiE / liutong > 0.1:
        return True
    return False

