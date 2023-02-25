import sys
from time import sleep


sys.path.append("..")
from Sell.nowData import getNow


def real(ts_code):
    for j in range(6 - len(ts_code)):
        ts_code = "0" + ts_code
    gujia, kaipan, zuigao, zuidi, zhangfu, chengjiaoliang, jiaoYiE, liutong, super, zhuli = getNow(ts_code)
    if 3.0 < zhangfu < 5.0:
        if zhuli > 0 and super > 0:
            return True
    return False
