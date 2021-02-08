import requests
import json
from flask import Flask,render_template,request,redirect,url_for,json
import os
import shutil

app = Flask(__name__)

def mkdir(path):
    isExists=os.path.exists(path)
    if not isExists:
        os.mknod(path)
#        os.makedirs(path)
        return True
    else:
        return False

@app.route('/music/get_id', methods=['POST', 'GET'])
def get_id():
    basepath = os.path.dirname(__file__)
    curpath = os.path.join(basepath,'static/stock/json/mid.json')
    home_id = open(curpath,'r+',encoding="utf-8")
    return json.loads(home_id.read(), strict=False)
    
@app.route('/music/update_id', methods=['POST', 'GET'])
def update_id():
    basepath = os.path.dirname(__file__)
    curpath = os.path.join(basepath,'static/stock/json/mid.json')
    new_id = request.form['key']
    home_file = {}
    with open(curpath,'r+',encoding="utf-8") as load_f:
        load_file = load_f.read()
        home_file = json.loads(load_file, strict=False)
        home_file['key'] = new_id
    with open(curpath,'w+',encoding="utf-8") as write_f:
        write_f.write(json.dumps(home_file))
        return "更新成功！"

@app.route('/music/search_music', methods=['POST', 'GET'])
def search_music():
    song = request.form['name']
    page = 1

    ua = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'Referer':'https://www.kuwo.cn/search/list?key=%E5%91%A8%E6%9D%B0%E4%BC%A6',
        'csrf':'72WEGN0DZQW',
        'Cookie':'_ga=GA1.2.597767892.1600353982; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1600353981,1602857940; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1602857940; _gid=GA1.2.392097668.1602857940; _gat=1; Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c=1600353987,1602857947; Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c=1602857947; kw_token=72WEGN0DZQW'}
    allsong = []

    for i in range(1,page+1):
        url = f'https://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={song}&pn={i}&rn=5&httpsStatus=1&reqId=a7f88d70-0fba-11eb-815d-ff35e4c1b385'
        getdata = requests.get(url=url,headers=ua).text
        jsondata = json.loads(getdata, strict=False)
        for j in jsondata['data']['list']:
            rid = j['rid']
            name = j['name']
            url2 = f'https://www.kuwo.cn/url?format=mp3&rid={rid}&response=url&type=convert_url3&br=128kmp3&from=web&t=1602859842960&httpsStatus=1&reqId=f7260901-0fbe-11eb-9629-9502ac4404c0'
            getdata2 = requests.get(url=url2,headers=ua).text
            jsondata2 = json.loads(getdata2, strict=False)
            musiclink = jsondata2['url']
            j['songurl'] = musiclink
            allsong.append(j)
#            music = requests.get(url=musiclink,headers=ua).content
#            musicfile = curpath + '/' + name + '.' + musiclink.split('.')[-1]
#            with open(musicfile,'wb') as fp:
#                fp.write(music)
#                return 'ok'
#    return 'ok'
    return json.dumps(allsong)

@app.route('/music/download_music', methods=['POST', 'GET'])
def download_music():
    song = request.form['name']
    songurl = request.form['songurl']
    basepath = os.path.dirname(__file__)
    poolpath = os.path.join(basepath,'static/stock/json/pool.json')
    with open(poolpath,'r+',encoding="utf-8") as load_f:
       load_file = load_f.read()
       home_file = json.loads(load_file, strict=False)
       for item in home_file['data']:
           if item['name'] == song:
               return 'repeat'
           
    # 名称和后缀
    name, ext =os.path.splitext(songurl)
    ua = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Referer':'https://www.kuwo.cn/search/list?key=%E5%91%A8%E6%9D%B0%E4%BC%A6',
    'csrf':'72WEGN0DZQW',
    'Cookie':'_ga=GA1.2.597767892.1600353982; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1600353981,1602857940; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1602857940; _gid=GA1.2.392097668.1602857940; _gat=1; Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c=1600353987,1602857947; Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c=1602857947; kw_token=72WEGN0DZQW'}
    music = song + ext
    curpath = os.path.join(basepath,'static/stock/music/pool/')
    musicpath = curpath + song + ext
    content = requests.get(url=songurl,headers=ua).content
    # 判断路径是否存在
#    flag = mkdir(musicpath)
    with open(musicpath,'wb') as fp:
        fp.write(content)
        return 'ok'

# pool基本信息保存
@app.route('/music/add_pool', methods=['POST', 'GET'])
def add_pool():
    basepath = os.path.dirname(__file__)
    curpath = os.path.join(basepath,'static/stock/json/pool.json')
    param1 = request.form
    home_file = []
    with open(curpath,'r+',encoding="utf-8") as load_f:
        load_file = load_f.read()
        home_file = json.loads(load_file, strict=False)
        home_file['data'].append(param1)
    with open(curpath,'w+',encoding="utf-8") as write_f:
           write_f.write(json.dumps(home_file))
           return "保存信息成功！"


@app.route('/music/pool_music', methods=['POST', 'GET'])
def pool_music():
    basepath = os.path.dirname(__file__)
    curpath = os.path.join(basepath,'static/stock/json/pool.json')
    home_all = open(curpath,'r+',encoding="utf-8")
    all_info = json.loads(home_all.read(), strict=False)
    all_data = all_info['data']
    # 增加分页
    all_len = len(all_data)
    current_no = int(request.form['page'])
    size = int(request.form['page_size'])
    start = size * (current_no - 1)
    end = size * current_no
    res = all_data[start:end]
    show_obj = {"data": res, "total": all_len, "type": "poolList"}
    return show_obj
    
# delete
@app.route('/music/delete_pool', methods=['POST', 'GET'])
def delete_pool():
    basepath = os.path.dirname(__file__)
    curpath = os.path.join(basepath,'static/stock/json/pool.json')
    del_id = request.form['key']
    home_file = []
    #    文件删除
    file_src = os.path.join(basepath,'static/stock/music/pool/',request.form['url'])
    os.remove(file_src)
        
    with open(curpath,'r+',encoding="utf-8") as load_f:
        load_file = load_f.read()
        home_file = json.loads(load_file, strict=False)
        for item in home_file['data']:
            if item['key'] == del_id:
                home_file['data'].remove(item)
                break
    with open(curpath,'w+',encoding="utf-8") as write_f:
        write_f.write(json.dumps(home_file))
        return "删除成功！"

# pass
@app.route('/music/add_list', methods=['POST', 'GET'])
def add_list():
    basepath = os.path.dirname(__file__)
    poolpath = os.path.join(basepath,'static/stock/json/pool.json')
    listpath = os.path.join(basepath,'static/stock/json/list.json')
    param = request.form
    home_file = []
    home_file1 = []
    #    文件迁移
    if param['name']:
        old_src = os.path.join(basepath,'static/stock/music/pool/',param['url'])
        new_src = os.path.join(basepath,'static/stock/music/list/',param['url'])
        shutil.move(old_src, new_src)
    with open(listpath,'r+',encoding="utf-8") as load_f:
        load_file = load_f.read()
        home_file = json.loads(load_file, strict=False)
        home_file['data'].append(param)
    with open(listpath,'w+',encoding="utf-8") as write_f:
        write_f.write(json.dumps(home_file))
    # delete pool
    with open(poolpath,'r+',encoding="utf-8") as load_f1:
        load_file1 = load_f1.read()
        home_file1 = json.loads(load_file1, strict=False)
        for item in home_file1['data']:
            if item['key'] == param['key']:
                home_file1['data'].remove(item)
                break
    with open(poolpath,'w+',encoding="utf-8") as write_f1:
        write_f1.write(json.dumps(home_file1))
        return "审核通过！"
@app.route('/music/get_list', methods=['POST', 'GET'])
def get_list():
    basepath = os.path.dirname(__file__)
    curpath = os.path.join(basepath,'static/stock/json/list.json')
    home_all = open(curpath,'r+',encoding="utf-8")
    all_info = json.loads(home_all.read(), strict=False)
    all_data = all_info['data']
    # 增加分页
    all_len = len(all_data)
    current_no = int(request.form['page'])
    size = int(request.form['page_size'])
    start = size * (current_no - 1)
    end = size * current_no
    res = all_data[start:end]
    show_obj = {"data": res, "total": all_len, "type": "list"}
    return show_obj

@app.route('/music/back_list', methods=['POST', 'GET'])
def back_list():
    basepath = os.path.dirname(__file__)
    poolpath = os.path.join(basepath,'static/stock/json/pool.json')
    listpath = os.path.join(basepath,'static/stock/json/list.json')
    param = request.form
    home_file = []
    home_file1 = []
    #    文件迁移list
    if param['name']:
        old_src = os.path.join(basepath,'static/stock/music/list/',param['url'])
        new_src = os.path.join(basepath,'static/stock/music/pool/',param['url'])
        shutil.move(old_src, new_src)
    with open(poolpath,'r+',encoding="utf-8") as load_f:
        load_file = load_f.read()
        home_file = json.loads(load_file, strict=False)
        home_file['data'].append(param)
    with open(poolpath,'w+',encoding="utf-8") as write_f:
        write_f.write(json.dumps(home_file))
    # delete list
    with open(listpath,'r+',encoding="utf-8") as load_f1:
        load_file1 = load_f1.read()
        home_file1 = json.loads(load_file1, strict=False)
        for item in home_file1['data']:
            if item['key'] == param['key']:
                home_file1['data'].remove(item)
                break
    with open(listpath,'w+',encoding="utf-8") as write_f1:
        write_f1.write(json.dumps(home_file1))
        return "撤回通过！"

if __name__ =="__main__":
    app.run(
        host='127.0.0.1',
        port= 5001,
        debug=True
    )
