import requests
import json
from flask import Flask,render_template,request,redirect,url_for,json
import os
import shutil
import pandas as pd
import tushare as ts
import baostock as bs
import datetime
import time
import threading
import csv
import json

app = Flask(__name__)
# tushare相关设置
ts.set_token("***")
pro = ts.pro_api()
# baostock相关设置
lg = bs.login()

# 公共方法
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
    elif j == 'factor':
        childpath = os.path.join(basepath,i + '/factor')
    isFile = os.path.exists(childpath)
    if isFile:
        return '1'
    else:
        os.makedirs(childpath)
        return '0'

@app.route('/stock/get_daily', methods=['POST', 'GET'])
# 获取所有股票当日数据（all）——tushare
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
# 查询某一时间段个股数据（未复权行情）——tushare
def get_stock_basic():
    param = request.form;
    if param['code']:
        # 600519.SH
        code = param['code']
    if param['begin']:
        # 20210121
        begin = param['begin']
    if param['end']:
        end = param['end']
    if param['page_size']:
        page_size = int(param['page_size'])
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
    save_file = {"data": []}
    json_name = code + "_" + show_time + ".json"
    josnpath = os.path.join(basepath,basicpath + '/json/' + json_name)
    result = stock.to_json(orient="records")
    parsed = json.loads(result)
    save_file["data"] = parsed
    with open(josnpath,'w+',encoding="utf-8") as write_j:
        write_j.write(json.dumps(save_file, indent=4))
    # 从json获取数据（首页默认展示n条数据）
    all_len = len(parsed)
    show_data = parsed[0:page_size]
    show_obj = {"data": show_data, "total": all_len, "type": "searchPer"}
    return show_obj

@app.route('/stock/get_stock_basic_page', methods=['POST', 'GET'])
# 分页，查询某一时间段个股数据（未复权行情）——tushare
def get_stock_basic_page():
    param = request.form;
    if param['code']:
        # 600519.SH
        code = param['code']
    if param['page_no']:
        page_no = int(param['page_no'])
    if param['page_size']:
        page_size = int(param['page_size'])
    basepath = os.path.dirname(__file__)
    basicpath = 'static/perstock/' + code
    today = datetime.date.today()
    show_time = datetime.datetime.strftime(today,'%Y-%m-%d')
    json_name = code + "_" + show_time + ".json"
    josnpath = os.path.join(basepath,basicpath + '/json/' + json_name)
    data_file = open(josnpath,'r+',encoding="utf-8")
    all_info = json.loads(data_file.read(), strict=False)
    all_data = all_info['data']
    all_len = len(all_data)
    start = page_size * (page_no - 1)
    end = page_size * page_no
    res = all_data[start:end]
    show_obj = {"data": res, "total": all_len, "type": "columnList"}
    return show_obj


# 查询复权因子(积分权限限制未使用——tushare)
def get_adj_factors():
    param = request.form;
    if param['code']:
        code = param['code']
    if param['date']:
        date = param['date']
    stock = pro.adj_factor(ts_code=code, trade_date=date)
    basepath = os.path.dirname(__file__)
    basicpath = 'static/perstock/' + code
    today = datetime.date.today()
    show_time = datetime.datetime.strftime(today,'%Y-%m-%d')
    fileFlag = get_file_exist(basicpath, 'main')
    factorFlag = get_file_exist(basicpath, 'factor')
    # 转为json存储
    json_name = code + "_" + show_time + ".json"
    josnpath = os.path.join(basepath,basicpath + '/factor/' + json_name)
    result = stock.to_json(orient="records")
    parsed = json.loads(result)
    with open(josnpath,'w+',encoding="utf-8") as write_j:
        write_j.write(json.dumps(parsed, indent=4))
    return 'save-factor'

@app.route('/stock/get_adj_factor', methods=['POST', 'GET'])
# 查询复权因子（不定期）——baostock(sh.600000,2015-01-01)
def get_adj_factor():
    param = request.form;
    if param['code']:
        # sh.600000(600000.SH)
        code = param['code']
    if param['begin']:
        # 2015-01-01
        begin = param['begin']
    if param['end']:
        # 2015-01-01
        end = param['end']
    rs_list = []
    codelist = code.split('.', 1 )
    show_code = codelist[1].lower() + '.' + codelist[0]
    rs_factor = bs.query_adjust_factor(code=show_code, start_date=begin,end_date=end)
    while (rs_factor.error_code == '0') & rs_factor.next():
        rs_list.append(rs_factor.get_row_data())
    result_factor = pd.DataFrame(rs_list, columns=rs_factor.fields)
    # 保存路径
    basepath = os.path.dirname(__file__)
    basicpath = 'static/perstock/' + code
    today = datetime.date.today()
    show_time = datetime.datetime.strftime(today,'%Y-%m-%d')
    fileFlag = get_file_exist(basicpath, 'main')
    factorFlag = get_file_exist(basicpath, 'factor')
    csv_name = code + "_" + show_time + ".csv"
    cvspath = os.path.join(basepath,basicpath + '/factor/' + csv_name)
    result_factor.to_csv(cvspath, encoding="gbk", index=False)
    # 转为json存储
    json_name = code + "_" + show_time + ".json"
    josnpath = os.path.join(basepath,basicpath + '/factor/' + json_name)
    result = result_factor.to_json(orient="records")
    parsed = json.loads(result)
    with open(josnpath,'w+',encoding="utf-8") as write_j:
        write_j.write(json.dumps(parsed, indent=4))
    all_len = len(parsed)
    show_obj = {"data": parsed, "total": all_len, "type": "factorList"}
    return show_obj


if __name__ =="__main__":
    app.run(
        host='127.0.0.1',
        port= 5005,
        debug=True
    )
