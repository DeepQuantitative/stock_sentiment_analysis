#!/usr/bin/env python
# encoding: utf-8

# -------------------------------------------
# 功能：数据清洗：剔除无用的评论的数据
# Author: zx
# Software: PyCharm Community Edition
# File: main.py
# Time: 17-1-5 上午9:53
# -------------------------------------------
import sqlite3

stocks = []


def get_stock():
    """
    获取股票，导入3000多支股票。
    :return:
    """
    stock_path = "/home/zhangxin/work/[上线]文本分类相关/classify_dict/stock_words.words"
    for d in open(stock_path):
        d = d.decode("utf-8").strip("\n").split("\t")
        d = d[1].split(",")
        stocks.append(d[1])


def process(content):
    """
    按照规则对评论内容进行初步的数据预清洗
    :param content:
    :return:
    """
    get_stock()
    global stocks
    # 规则 1
    # 如果评论内容的超过300个字符则剔除
    if len(content) > 300:
        return False
    # 规则 2
    # 如果评论内容中包含url
    elif content.__contains__("http"):
        return False
    # 规则 3
    # 如果评论中包含超过5支股票的信息
    num_stocks = 5
    count = 0
    for s in stocks:
        if content.__contains__(s):
            count += 1
    if count > num_stocks:
        return False

    return True


def run():
    get_stock()
    conn = sqlite3.connect(
        "/home/zhangxin/文档/市场情绪分析/雪球数据/[剔除]data_xueqiu_sentiment_服务器_69.sqlite")
    cu = conn.cursor()

    # 获取所有表名
    str_tb = "SELECT name FROM sqlite_master WHERE type='table' order by name"
    cu.execute(str_tb)
    result = cu.fetchall()
    table_name = [r[0] for r in result]

    # 遍历表
    for tname in table_name:
        print "[%s]" % tname
        str_query = "select id, content from %s" % tname
        cu.execute(str_query)
        result = cu.fetchall()

        id = []
        content = []
        delete_id = []

        count_all = len(result)
        count_delete = 0

        for r in result:
            presult = process(r[1])
            if presult:
                # print presult
                id.append(r[0])
                content.append(r[1])
            else:
                count_delete += 1
                delete_id.append(r[0])
                str_delete = "delete from %s where id = '%s'" % (tname, r[0])
                cu.execute(str_delete)
                conn.commit()
                # print "   ", r[0], r[1]

        print "   %d / %d = %f" % (count_delete, count_all, float(count_delete) / count_all)


if __name__ == '__main__':
    run()
