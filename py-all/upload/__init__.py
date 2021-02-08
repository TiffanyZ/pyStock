from flask import Flask,render_template,request,redirect,url_for,json
from werkzeug.utils import secure_filename
from collections import OrderedDict
import os
import shutil

app = Flask(__name__)

# 获取homeId（lastId）——用于添加内容
@app.route('/edit/home_id', methods=['POST', 'GET'])
def home_id():
    basepath = os.path.dirname(__file__)
    curpath = os.path.join(basepath,'static/stock/json/homeId.json')
    home_id = open(curpath,'r+',encoding="utf-8")
    return json.loads(home_id.read(), strict=False)

# 重置homeId（lastId）——添加内容后更新
@app.route('/edit/home_id_reset', methods=['POST', 'GET'])
def home_id_reset():
    basepath = os.path.dirname(__file__)
    curpath = os.path.join(basepath,'static/stock/json/homeId.json')
    new_id = request.form['id']
    home_file = {}
    with open(curpath,'r+',encoding="utf-8") as load_f:
        load_file = load_f.read()
        home_file = json.loads(load_file, strict=False)
        home_file['data'] = new_id
    with open(curpath,'w+',encoding="utf-8") as write_f:
        write_f.write(json.dumps(home_file))
        return "更新成功！"
    
# homeData追加内容(add)——（homeAll）
@app.route('/edit/home_data_add', methods=['POST', 'GET'])
def home_data_add():
    basepath = os.path.dirname(__file__)
    curpath = os.path.join(basepath,'static/stock/json/homeData.json')
    param1 = request.form;
    home_file = []
    #    图片迁移
    if param1['img']:
        old_src = os.path.join(basepath,'static/stock/img/uploads/',param1['img'])
        new_src = os.path.join(basepath,'static/stock/img/allImg/',param1['img'])
        shutil.move(old_src, new_src)
    with open(curpath,'r+',encoding="utf-8") as load_f:
        load_file = load_f.read()
        home_file = json.loads(load_file, strict=False)
        home_file['data'].append(param1)
    with open(curpath,'w+',encoding="utf-8") as write_f:
        write_f.write(json.dumps(home_file))
        return "新增成功！"
    
   
# 获取homeAll(分页)
@app.route('/edit/home_all', methods=['POST', 'GET'])
def home_all():
    basepath = os.path.dirname(__file__)
    curpath = os.path.join(basepath,'static/stock/json/homeData.json')
    home_all = open(curpath,'r+',encoding="utf-8")
    all_info = json.loads(home_all.read(), strict=False)
    all_data = all_info['data']
#    增加分页
    all_len = len(all_data)
    current_no = int(request.form['page_no'])
    size = int(request.form['page_size'])
    start = size * (current_no - 1)
    end = size * current_no
    res = []
    show_obj = {}
    id = ''
    if current_no == -1:
        id = request.form['id']
    else:
        id = ''
    if id:
        for new in all_data:
            if new.id == id:
                res.append(new)
                all_len = 1
    else:
        res = all_data[start:end]
    show_obj = {"data": res, "total": all_len, "type": "homeAll"}
    return show_obj
#    return json.loads(home_all.read(), strict=False)

# homeData删除内容(homeAll)
@app.route('/edit/home_data_del', methods=['POST', 'GET'])
def home_data_del():
    basepath = os.path.dirname(__file__)
    curpath = os.path.join(basepath,'static/stock/json/homeData.json')
    del_id = request.form['id']
    home_file = []
    if request.form['oper_name'] == 'oper_010':
        #    图片删除
        if request.form['type'] == 'del' and request.form['img']:
            img_src = os.path.join(basepath,'static/stock/img/allImg/',request.form['img'])
            os.remove(img_src)
        with open(curpath,'r+',encoding="utf-8") as load_f:
            load_file = load_f.read()
            home_file = json.loads(load_file, strict=False)
            for item in home_file['data']:
                if item['id'] == del_id:
                    home_file['data'].remove(item)
                    break
        with open(curpath,'w+',encoding="utf-8") as write_f:
            write_f.write(json.dumps(home_file))
            return "删除成功！"

# 内容审核根据栏目分类，存储到对应栏目里（栏目id）
@app.route('/edit/home_list_set', methods=['POST', 'GET'])
def home_list_set():
    basepath = os.path.dirname(__file__)
    curpath = os.path.join(basepath,'static/stock/json/homeList/')
    param2 = request.form
    column = param2['column']
    if param2['oper_name'] == 'oper_010':
        realpath = curpath + column + '.json'
        home_file = []
        #    图片迁移
        if param2['img']:
            old_src = os.path.join(basepath,'static/stock/img/allImg/',param2['img'])
            new_src = os.path.join(basepath,'static/stock/img/listImg/',param2['img'])
            shutil.move(old_src, new_src)
        with open(realpath,'r+',encoding="utf-8") as load_f:
            load_file = load_f.read()
            home_file = json.loads(load_file, strict=False)
            home_file['data'].append(param2)
        with open(realpath,'w+',encoding="utf-8") as write_f:
            write_f.write(json.dumps(home_file))
            return "审核通过！"
    
# 获取homeList(根据栏目获取不同文件)
@app.route('/edit/home_list', methods=['POST', 'GET'])
def home_list():
    basepath = os.path.dirname(__file__)
    curpath = os.path.join(basepath,'static/stock/json/homeList/')
    #    栏目id
    param = request.form['id']
    realpath = curpath + param + '.json'
    home_file = open(realpath,'r+',encoding="utf-8")
    home_info = json.loads(home_file.read(), strict=False)
    all_data = home_info['data']
    #    增加分页
    all_len = len(all_data)
    current_no = int(request.form['page_no'])
    size = int(request.form['page_size'])
    start = size * (current_no - 1)
    end = size * current_no
    res = all_data[start:end]
    show_obj = {"data": res, "total": all_len, "type": "columnList"}
    return show_obj

# 获取tagList
@app.route('/edit/tag_list', methods=['POST', 'GET'])
def tag_list():
    basepath = os.path.dirname(__file__)
    curpath = os.path.join(basepath,'static/stock/json/tagList.json')
    tag_list = open(curpath,'r+',encoding="utf-8")
    return json.loads(tag_list.read(), strict=False)

# 获取columnList
@app.route('/edit/column_list', methods=['POST', 'GET'])
def column_list():
    basepath = os.path.dirname(__file__)
    curpath = os.path.join(basepath,'static/stock/json/columnList.json')
    column_list = open(curpath,'r+',encoding="utf-8")
    return json.loads(column_list.read(), strict=False)
    
# list内容撤回到all
@app.route('/edit/home_back_all', methods=['POST', 'GET'])
def home_back_all():
    basepath = os.path.dirname(__file__)
    curpath = os.path.join(basepath,'static/stock/json/homeList/')
    allpath = os.path.join(basepath,'static/stock/json/homeData.json')
    column = request.form['column']
    key = request.form['key']
    realpath = curpath + column + '.json'
    cur_data = {}
    home_all = {}
    if request.form['oper_name'] == 'oper_010':
        # 图片迁移
        if request.form['img']:
            old_src = os.path.join(basepath,'static/stock/img/listImg/',request.form['img'])
            new_src = os.path.join(basepath,'static/stock/img/allImg/',request.form['img'])
            shutil.move(old_src, new_src)
        # 删除
        with open(realpath,'r+',encoding="utf-8") as load_f:
            load_file = load_f.read()
            home_file = json.loads(load_file, strict=False)
            for item in home_file['data']:
                if item['key'] == key:
                    cur_data = item
                    home_file['data'].remove(item)
                    break
        with open(realpath,'w+',encoding="utf-8") as write_f:
            write_f.write(json.dumps(home_file))
        # 转存
        with open(allpath,'r+',encoding="utf-8") as all_f:
            all_file = all_f.read()
            home_all = json.loads(all_file, strict=False)
            all_data = home_all['data']
            all_data.append(cur_data)
        with open(allpath,'w+',encoding="utf-8") as write_all:
            write_all.write(json.dumps(home_all))
            return "撤回成功！"

# 图片上传成功页面
@app.route('/edit/upfile/upSuccess.html')
def query_user():
    """
      http://127.0.0.1:5000/test?id=1
    :return:
    """
    id=request.args.get('id')
    return "query user:"+id

# 图片上传(图片池)
@app.route('/edit/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
#        名称和后缀
        name, ext =os.path.splitext(f.filename)
        id=request.args.get('id')
        basepath = os.path.dirname(__file__)
        filepath = os.path.join(basepath,'static/stock/img/uploads')
        upload_path = os.path.join(filepath,secure_filename(f.filename))
        f.save(upload_path)
        os.rename(upload_path,os.path.join(filepath,id+ext))
        return id+ext
#        return redirect(url_for("query_user",param=id))

# home富文本内容保存
@app.route('/edit/save_draft', methods=['POST', 'GET'])
def save_draft():
    basepath = os.path.dirname(__file__)
    curpath = os.path.join(basepath,'static/stock/json/draft.json')
    content = request.form['content']
    home_file = {"data": "", "type": "draft"}
    with open(curpath,'r+',encoding="utf-8") as load_f:
        load_file = load_f.read()
        home_file = json.loads(load_file, strict=False)
        home_file['data'] = content
    with open(curpath,'w+',encoding="utf-8") as write_f:
        write_f.write(json.dumps(home_file))
        if content == "":
            return "草稿已清空！"
        else:
            return "草稿已保存！"

# home富文本内容
@app.route('/edit/get_draft', methods=['POST', 'GET'])
def get_draft():
    basepath = os.path.dirname(__file__)
    curpath = os.path.join(basepath,'static/stock/json/draft.json')
    with open(curpath,'r+',encoding="utf-8") as load_f:
        return json.loads(load_f.read(), strict=False)
        
# 操作员code校验
@app.route('/edit/oper_code', methods=['POST', 'GET'])
def oper_code():
    code = request.form['code']
    if code == 'ts010':
        return 'oper_010'

if __name__ =="__main__":
    app.run(
        host='127.0.0.1',
        port= 5002,
        debug=True
    )
