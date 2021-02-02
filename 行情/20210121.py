import requests
import json
from flask import Flask,render_template,request,redirect,url_for,json
import os
import shutil
import pandas as pd
import tushare as ts
import datetime
import time
import threading
import csv
import json

app = Flask(__name__)
# tushare相关设置（token需要自己获取）
ts.set_token("***")
pro = ts.pro_api()

@app.route('/stock/get_daily', methods=['POST', 'GET'])
# 获取所有股票当日数据（all）
def get_daily():
    stock = ts.get_today_all()
    # 给数据添加一个日期
    stock['date'] = datetime.date.today()
    # 导出CSV格式的文件，原因有两个，一是pandas处理CSV格式的文件远比Excel快，二是Excel有最大行数限制，只能有104w行数据，而CSV没有这个限制
    today = datetime.date.today()
    # datetime转字符串
    show_time = datetime.datetime.strftime(today,'%Y-%m-%d')
    basepath = os.path.dirname(__file__)
    # 存储csv文件
    csv_name = show_time + ".csv"
    cvspath = os.path.join(basepath,'static/allstock/csv/' + csv_name)
    stock.to_csv(cvspath,encoding = 'utf-8',index=None)
    # 存储excel文件
    excel_name = show_time + ".xlsx"
    excelpath = os.path.join(basepath,'static/allstock/excel/' + excel_name)
    stock.to_excel(excelpath,encoding = 'utf-8',index=None)
    # 转为json存储
    json_name = show_time + ".json"
    josnpath = os.path.join(basepath,'static/allstock/json/' + json_name)
    result = stock.to_json(orient="records")
    parsed = json.loads(result)
    with open(josnpath,'w+',encoding="utf-8") as write_j:
        write_j.write(json.dumps(parsed, indent=4))
    return "save-ok"
    

@app.route('/stock/sleep_daily', methods=['POST', 'GET'])
# 定时查询所有股票当日数据
def sleep_daily():
    while True:
        now_hour = time.strftime("%H", time.localtime())
        now_min = time.strftime("%M", time.localtime())
        if now_hour < "16":
            rest = 16 - int(now_hour)
            sleeptime = (rest-1)*3600 + (60-int(now_min))*60
            time.sleep(sleeptime)
        elif now_hour > "16":
            rest = 16 - int(now_hour) + 24
            sleeptime = (rest-1)*3600 + (60-int(now_min))*60
            time.sleep(sleeptime)
        elif now_hour == "16":
            # 以下为定时任务
            test = get_daily()
            time.sleep(86400-int(now_min)*60)
            
@app.route('/stock/get_stock_basic', methods=['POST', 'GET'])
# 查询某一时间段个股数据（未复权行情）
def get_stock_basic():
#    code = "600519.SH"
#    begin = "20210120"
#    end = "20210121"
    param = request.form;
    if param['code']:
        code = param['code']
    if param['begin']:
        begin = param['begin']
    if param['end']:
        end = param['end']
    stock = pro.daily(ts_code=code, start_date=begin, end_date=end)
    basepath = os.path.dirname(__file__)
    basicpath = 'static/perstock/' + code
    today = datetime.date.today()
    show_time = datetime.datetime.strftime(today,'%Y-%m-%d')
    # 创建个股文件夹
    fileFlag = get_file_exist(basicpath, 'main')
    if fileFlag == '0':
        csvFlag = get_file_exist(basicpath, 'csv')
        if csvFlag == '0':
            excelFlag = get_file_exist(basicpath, 'excel')
            if excelFlag == '0':
                josnFlag = get_file_exist(basicpath, 'json')
    # 存储csv文件
    csv_name = code + "_" + show_time + ".csv"
    cvspath = os.path.join(basepath,basicpath + '/csv/' + csv_name)
    stock.to_csv(cvspath,encoding = 'utf-8',index=None)
    # 存储excel文件
    excel_name = code + "_" + show_time + ".xlsx"
    excelpath = os.path.join(basepath,basicpath + '/excel/' + excel_name)
    stock.to_excel(excelpath,encoding = 'utf-8',index=None)
    # 转为json存储
    json_name = code + "_" + show_time + ".json"
    josnpath = os.path.join(basepath,basicpath + '/json/' + json_name)
    result = stock.to_json(orient="records")
    parsed = json.loads(result)
    with open(josnpath,'w+',encoding="utf-8") as write_j:
        write_j.write(json.dumps(parsed, indent=4))
    return "ok-per"

def get_file_exist(i, j):
    basepath = os.path.dirname(__file__)
    if j == 'main':
        childpath = os.path.join(basepath,i)
    elif j == 'csv':
        childpath = os.path.join(basepath,i + '/csv')
    elif j == 'excel':
        childpath = os.path.join(basepath,i + '/excel')
    elif j == 'json':
        childpath = os.path.join(basepath,i + '/json')
    isFile = os.path.exists(childpath)
    if isFile:
        return '1'
    else:
        os.makedirs(childpath)
        return '0'


if __name__ =="__main__":
    app.run(
        host='127.0.0.1',
        port= 5005,
        debug=True
    )
