import os
import sys
import datetime as dt
import importlib
import threading
import Cla2
from pythonProject2 import testSet
import torch.nn as nn
import torch.nn.functional as F
from sql.configSql import getdb
from Buy.buy_main import oneOperation, twoOperation
from Sell.back import huitiao
from Sell.continueBuy import continuebuy
from time import sleep

from drawkline import letdraw

import socketserver


# 定义一个类，继承socketserver.BaseRequestHandler
class Server(socketserver.BaseRequestHandler):
    def handle(self):
        # 打印客户端地址和端口
        print('New connection:', self.client_address)
        # 循环
        while True:
            # 接收客户发送的数据
            data = self.request.recv(1024)
            if not data:
                break  # 如果接收数据为空就跳出，否则打印
            print('Client data:', data.decode())
            if data.decode() == "getpic":
                fenlei = Cla2.Fenlei()
                list1 = fenlei.classify()
            self.request.send(list1)  # 将收到的信息再发送给客户端


if __name__ == '__main__':
    host, port = '172.29.7.161', 8080
    # 定义服务器地址和端口
    server = socketserver.ThreadingTCPServer((host, port), Server)  # 实现了多线程的socket通话
    server.serve_forever()

