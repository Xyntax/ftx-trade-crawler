# ftx-trade-crawler

FTX交易所数据爬取脚本

1. `btc_move_monitor.py` 实时爬取BTC-MOVE成交数据，秒级。
2. `btc_move_backtrace_30min.py` 补历史数据，半小时级。（每半小时拉最近200条交易数据，BTC-MOVE 90%以上时间成交数不足200，大概每天只有1h的数据有部分损失，其余时间是全量）

数据
1. db.sql 为2019-12-31 到2020-03-01 的历史数据，mysql格式，共89556条。