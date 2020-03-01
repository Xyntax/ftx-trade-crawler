# !/usr/bin/env python
#  -*- coding: utf-8 -*-
import pymysql
from pymysql import escape_string
import time
import json
import urllib.request
import datetime
from ftx.ftx_client import FtxClient
from conf import *


db = pymysql.connect(MYSQL.HOST, MYSQL.USER, MYSQL.PASS, MYSQL.DB)
print('connect mysql success.')


def insert(id, liquidation, price, side, size, time, ticker, database=db):
    sql = "insert ignore into ftx_btc_move " \
          "(id,liquidation,price,side,size,time,ticker) " \
          "values " \
          "('{id}','{liquidation}','{price}','{side}','{size}','{time}','{ticker}');".format(
        id=escape_string(str(id)),
        liquidation=escape_string(str(liquidation)),
        price=escape_string(str(price)),
        side=escape_string(str(side)),
        size=escape_string(str(size)),
        time=escape_string(str(time)),
        ticker=escape_string(str(ticker))
    )
    cursor = database.cursor()
    cursor.execute(sql)
    database.commit()


def send_msg(msg):
    keyword = DINGTALK.KEYWORD
    webhook = DINGTALK.API
    post_data = {
        'msgtype': 'text',
        'text': {"content": '[{}]: '.format(keyword) + msg}
    }
    req = urllib.request.Request(webhook, json.dumps(post_data).encode('utf8'),
                                 headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req).read()
    except Exception as err:
        print(err)


def get_ticker_trades(ticker):
    try:
        ftx = FtxClient(FTX.AK, FTX.SK)
        trades = ftx.get_trades(ticker)
        for each in trades:
            insert(
                each['id'],
                each['liquidation'],
                each['price'],
                each['side'],
                each['size'],
                each['time'],
                ticker
            )
    except Exception as err:
        print(err)
        send_msg(err)


def get_utc_time():
    return datetime.datetime.utcnow().strftime("%m%d")


def main():
    while True:
        time.sleep(0.5)
        ticker = 'BTC-MOVE-{}'.format(get_utc_time())
        print('starting craw trades of: {}'.format(ticker))
        get_ticker_trades(ticker)


if __name__ == '__main__':
    main()