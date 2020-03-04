# !/usr/bin/env python
#  -*- coding: utf-8 -*-
import time
import json
import math
import sys
import pymysql
from pymysql import escape_string
from ftx.ftx_client import FtxClient
import datetime
from datetime import timezone
from conf import *

'''
?limit={limit}&start_time={start_time}&end_time={end_time}
'''
ftx = FtxClient(FTX.AK, FTX.SK)

db = pymysql.connect(MYSQL.HOST, MYSQL.USER, MYSQL.PASS, MYSQL.DB)
print('connect mysql success.')


def get_trades(ticker, start_time, end_time, limit=200):
    try:
        result = ftx._get('/markets/{ticker}/trades?limit={limit}&start_time={start_time}&end_time={end_time}'.format(
            ticker=ticker,
            limit=limit,
            start_time=start_time,
            end_time=end_time
        ))
        return result
    except Exception as err:
        print(err)


def timestamp_to_ticker(timestamp):
    time_utc = datetime.datetime.fromtimestamp(timestamp, timezone.utc)
    ticker = 'BTC-MOVE-{}'.format(time_utc.strftime("%m%d"))

    # fix 2019 ticker
    if int(timestamp) < 1577750400:  # 2019-12-31 00:00:00
        ticker = 'BTC-MOVE-2019{}'.format(time_utc.strftime("%m%d"))
    return ticker


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
        ticker=ticker
    )
    cursor = database.cursor()
    cursor.execute(sql)
    database.commit()


def main():
    targets = json.load(open('200.json'))

    forget_200 = []
    try:
        for each in targets:

            ticker, pos, end = each
            print('handling: ', ticker, pos, end)

            while True:
                start_time = pos
                if start_time >= end:
                    break

                end_time = pos + 60
                ticker = timestamp_to_ticker(start_time)
                trades = get_trades(ticker, start_time, end_time)
                print(
                    '[-]cnt:{}, ticker:{}, timestart:{}, timeend:{}'.format(len(trades), ticker, start_time, end_time))
                if len(trades) == 200:
                    # print(ticker, start_time, end_time)
                    forget_200.append([ticker, start_time, end_time])

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
                pos -= 60
    except Exception as err:
        print(err)
        print(sys.exc_info()[0])
        json.dump(forget_200, open('200-1min.json', 'w'))


if __name__ == '__main__':
    main()
