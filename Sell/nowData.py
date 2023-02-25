import re
from requests_html import HTMLSession

from time import sleep

asession = HTMLSession()

def get_webdriver(ts_code):
    if int(ts_code[0:6]) < 301397:
        ts_code = 'sz{}'.format(ts_code)
    elif 689010 > int(ts_code[0:6]) > 430685:
        ts_code = 'sh{}'.format(ts_code)
    else:
        ts_code = 'bj{}'.format(ts_code)
    url = 'https://finance.sina.com.cn/realstock/company/{}/nc.shtml'.format(ts_code)
    r = asession.get(url)
    r.html.render()
    return r.html.html


def getNow(ts_code):
    # html2 = asession.run(get_webdriver, urls=ts_code)
    # html2 = str(html2)
    html2 = ""
    attempts = 0
    success = False
    while attempts < 3 and not success:
        try:
            html2 = get_webdriver(ts_code)
            success = True
        except:
            attempts += 1
            sleep(3)
            if attempts == 3:
                print(ts_code + " failed")
                break
    pattern0 = re.compile(
        '<div id="price" class=".*?">(.*?)</div>',
        re.S)
    gujia = pattern0.findall(html2)
    gujia = float(gujia[0])
    pattern1 = re.compile(
        'div id="changeP" class=".*?">(.*?)</div>',
        re.S)
    zhangfu = pattern1.findall(html2)
    zhangfu = float(zhangfu[0][:-1])
    pattern0 = re.compile(
        '<div class="other" id="hqDetails">.*?<tr>.*?<td class=".*?">(.*?)</td>.*?<td>('
        '.*?)</td>.*?<tr>.*?<td class=".*?">('
        '.*?)</td>.*?<td>(.*?)</td>.*?<tr>.*?<td class=".*?">(.*?)</td>.*?<tr>.*?<td>.*?<td>(.*?)</td>'
        , re.S)
    data1 = pattern0.findall(html2)
    data1 = data1[0]
    kaipan = float(data1[0])
    # 涓囨墜 万 浜垮厓 亿
    # 鎵�   手     涓囧厓 万
    chengjiaoliang = data1[1]
    if chengjiaoliang[-2:] == '鎵�':
        chengjiaoliang = float(chengjiaoliang[0:-2]) / 10000
    else:
        chengjiaoliang = chengjiaoliang[:-3]
        chengjiaoliang = float(chengjiaoliang)
    zuigao = float(data1[2])
    zuidi = float(data1[4])
    # 浜垮厓 亿元 浜� 亿
    jiaoYiE = data1[3]
    if jiaoYiE[-3:] == '浜垮厓':
        jiaoYiE = float(jiaoYiE[0:-3])
    elif jiaoYiE[-3:] == '涓囧厓':
        jiaoYiE = float(jiaoYiE[0:-3]) / 10000
    liutong = data1[4]
    liutong = float(liutong[0:-2])
    pattern3 = re.compile('<div class="flow_table" id="FLFlow">.*?<tbody>.*?<tr>.*?</tr>.*?<tr>.*?<td>.*?<td>.*?<td'
                          '>.*?<td>(.*?)</td>', re.S)
    super = pattern3.findall(html2)
    super = float(super[0])

    pattern4 = re.compile('<div class="flow_table" id="MRFlow">.*?<tbody>.*?<tr>.*?</tr>.*?<tr>.*?<td>('
                          '.*?)</td>.*?<td>(.*?)</td>', re.S)
    zhuli = pattern4.findall(html2)
    zhuli = float(zhuli[0][0]) - float(zhuli[0][1])
    result = (gujia, kaipan, zuigao, zuidi, zhangfu, chengjiaoliang, jiaoYiE, liutong, super, zhuli)
    return result
