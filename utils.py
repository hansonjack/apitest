import os
from posixpath import join
from httprunner import HttpRunner
from httprunner import loader
from httprunner.client import HttpSession
from httprunner.scaffold import create_scaffold
import shutil
from werkzeug.wrappers import request
import yaml
import json
import subprocess
from loguru import logger
import uuid
import codecs

def del_file(path):
    '''
    删除一个目录下所有文件
    '''
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)
def create_httprunner_projiect(project):
    #hrproject 与当前python项目同级
    project_path0 = os.path.abspath(os.path.dirname(os.getcwd()))
    project_path1 = os.path.join(project_path0, 'hrproject')
    project_path2 = os.path.join(project_path1, project)

    create_scaffold(project_path2)
    testcase_path = os.path.join(project_path2,'testcases')
    # del_file(testcase_path)
    # print(project_path,testcase_path)
    return project_path2,testcase_path


def run_testcase(fpath,hr_root):
    test_content = loader.load_test_file(fpath)
    testcase = loader.load_testcase(test_content)
    log_folder = os.path.join(hr_root,'logs')
    os.makedirs(log_folder,exist_ok=True)
    case_id = str(uuid.uuid4())
    case_id = ''.join(case_id.split('-'))
    log_path = os.path.join(log_folder,case_id+'.run.log')
    log_handler = logger.add(log_path, level="DEBUG")  ###利用日志add函数把日志写入文件
    summary_json = {}
    try:
        runner = HttpRunner()
        runner.with_session(HttpSession())
        project_meta = loader.load_project_meta(fpath)
        runner.with_project_meta(project_meta).run_testcase(testcase)
        summary = runner.get_summary()
        logger.remove(log_handler)
        
        summary_json = json.loads(summary.json())
    except:
        summary_json['success'] = False
        
    summary_json['case_id'] = case_id
    summary_json['log'] = log_path.replace(os.getcwd(),'')[1:].strip()
    return summary_json,case_id

def run_testcase_with_command(fpath):
    pass
def run_testcases(fpaths,hr_root):
    run_id = str(uuid.uuid4())
    summarys = []
    for i in fpaths:
        summary,case_id = run_testcase(i,hr_root)
        summarys.append(summary)
    return summarys,run_id

def rm_hrproject(path):
    shutil.rmtree(path)


def create_yml(path,content):
    if not isinstance(content,dict):
        return
    with open(path,'w',encoding="utf-8") as f:
        yaml.dump(content,f,encoding='utf-8',allow_unicode=True)

def list2dict(content):
    if not isinstance(content,list):
        return
    data = {}
    for i in content:
        data[i['key']] = i.get('value') or ''
    return data

def res_data(normal,abnormal=None):
    if not normal:
        return
    if not isinstance(normal,list):
        return
    data = list2dict(normal)
    data1 = list2dict(abnormal)
    if data1:
        data['encryption_params'] = data1
    return data

def hr_validate(content):
    if not content:
        return
    if not isinstance(content,list):
        return
    data = []
    for i in content:
        if i['value_type'] == 'string':
            data.append(
                {i['func']:[i['value1'],i['value2']]}
            )
        else:
           data.append(
                {i['func']:[i['value1'],int(i['value2'])]}
            ) 
    return data

def hr_req(content):
    if not content:
        return
    if not isinstance(content,dict):
        return
    req = {
        'method':'',
        'url':'',
        'headers':{}
    }
    req['method'] = content.get('method')
    req['url'] = content.get('url')
    req['headers'] = list2dict(content.get('headers')) or {}
    content_type = content.get('content_type')
    if content_type == 'application/x-www-form-urlencoded':
        if content.get('encryption'):
            req['json'] = res_data(content.get('normal'),content.get('encryption'))
        else:
            req['params'] = res_data(content.get('normal'))
    elif content_type == 'application/json':
        req['json'] = res_data(content.get('normal'),content.get('encryption'))
    elif content_type == 'multipart/form-data':
        if content.get('encryption'):
            req['json'] = res_data(content.get('normal'),content.get('encryption'))
        else:
            req['data'] = res_data(content.get('normal'))
    
    return req

def hr_teststep(content):
    if not content:
        return
    teststep = {
        'name':content.get('name'),
        'variables':list2dict(content.get('variables')) or {},
        'request':hr_req(content),
        'extract':list2dict(content.get('extract')) or {},
        'validate':hr_validate(content.get('validate')) or {},
        'setup_hooks':hr_hooks(content.get('setup_hooks')),
        'teardown_hooks':hr_hooks(content.get('teardown_hooks'))

    }

    return teststep

def hr_export(content):
    if not isinstance(content,list):
        return []
    data = []
    for i in content:
        data.append(i['key'])
    return data
def hr_hooks(content):
    if not isinstance(content,list):
        return []
    data = []
    for i in content:
        data.append(i['key'])
    return data

def hr_yml(path,config,teststeps):
    print(teststeps)
    if not config or not teststeps:
        return
    if not isinstance(config,dict):
        return
    if not isinstance(teststeps,list):
        return
    data = {
        'config':config,
        'teststeps':teststeps
    }
    create_yml(path,data)
    
    return path

def str_decode(s):
    try:
        return s.decode('utf-8')

    except UnicodeDecodeError:
        return s.decode('gbk')

def run_hr_with_command(path):
        resp = str_decode(subprocess.check_output(['hrun', path,' -s ----html=%s.html'%path], stderr=subprocess.STDOUT, timeout=60))
        return resp

def read_file(path):
    with codecs.open(path,'r') as f :
        return f.read()

def db2web_data(data):
    if not isinstance(data,dict):
        return
    request = data.get('request')
    data['method'] = request['method']
    data['url'] = request['url']
    for i in request['headers']:
        if i['key'] == 'content_type':
            data['content_type'] = i['value']

    data['headers'] = request['headers']
    data['normal'] = request['request_data_normal']
    data['encryption'] = request['request_data_encryption']

    return data


def time2str(daytime):
    print(type(daytime))
    if daytime:
        return daytime.strftime('%Y-%m-%d %H:%M:%S')
        
    else:
        return

def write_logs(log_src,log_des):
    with open(log_src,'r',encoding='utf-8') as f :
        with open(log_des,'w',encoding='utf-8') as f1:
            f1.write(f.read())