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
# tushare相关设置
ts.set_token("2794151c50d545d18c52aac9430c124cd017c12ee1ef274bf2038bcd")
pro = ts.pro_api()

@app.route('/stock/get_daily', methods=['POST', 'GET'])
def get_daily():
    # 获取所有股票当日数据
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
    cvspath = os.path.join(basepath,'static/all/csv/' + csv_name)
    stock.to_csv(cvspath,encoding = 'utf-8',index=None)
    # 存储excel文件
    excel_name = show_time + ".xlsx"
    excelpath = os.path.join(basepath,'static/all/excel/' + excel_name)
    stock.to_excel(excelpath,encoding = 'utf-8',index=None)
    # 转为json存储
    json_name = show_time + ".json"
    josnpath = os.path.join(basepath,'static/all/json/' + json_name)
    result = stock.to_json(orient="records")
    parsed = json.loads(result)
    with open(josnpath,'w+',encoding="utf-8") as write_j:
        write_j.write(json.dumps(parsed, indent=4))
#    stock.to_json(josnpath)
#    json_name = show_time + ".json"
#    josnpath = os.path.join(basepath,'static/json/' + json_name)
#    json_file = open(josnpath, 'w+', encoding='utf-8')
#    csv_file = open(cvspath, 'r', encoding='utf-8')
#    ls=[]
#    for line in csv_file:
#        line=line.replace("\n","")
#        ls.append(line.split(","))
#    csv_file.close()
#    for i in range(1,len(ls)):
#        ls[i]=dict(zip(ls[0],ls[i]))
#    b = json.dumps(ls[1:],sort_keys=True,indent=4,ensure_ascii=False)
#    json_file.write(b)
#    json_file.close()
    return "save-ok"
    

@app.route('/stock/sleep_daily', methods=['POST', 'GET'])
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
def get_stock_basic():
#    param = request.form;
    code = "600519.SH"
    begin = "20210120"
    end = "20210121"
#    if param['code']:
#        code = param['code']
#    if param['begin']:
#        begin = param['begin']
#    if param['end']:
#        end = param['end']
    stock = pro.daily(ts_code=code, start_date=begin, end_date=end)
    basepath = os.path.dirname(__file__)
    today = datetime.date.today()
    show_time = datetime.datetime.strftime(today,'%Y-%m-%d')
    # 存储csv文件
    csv_name = code + "_" + show_time + ".csv"
    cvspath = os.path.join(basepath,'static/per/csv/' + csv_name)
    stock.to_csv(cvspath,encoding = 'utf-8',index=None)
    # 存储excel文件
    excel_name = code + "_" + show_time + ".xlsx"
    excelpath = os.path.join(basepath,'static/per/excel/' + excel_name)
    stock.to_excel(excelpath,encoding = 'utf-8',index=None)
    # 转为json存储
    json_name = code + "_" + show_time + ".json"
    josnpath = os.path.join(basepath,'static/per/json/' + json_name)
    result = stock.to_json(orient="records")
    parsed = json.loads(result)
    with open(josnpath,'w+',encoding="utf-8") as write_j:
        write_j.write(json.dumps(parsed, indent=4))
    return "ok-per"


if __name__ =="__main__":
    app.run(
        host='127.0.0.1',
        port= 5005,
        debug=True
    )
