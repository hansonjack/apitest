# coding:utf-8
import redis
import re
import json
import time
from itertools import chain
from datetime import datetime, date
import subprocess
import os
import re
import requests

class ExpandJsonEncoder(json.JSONEncoder):
    '''
        采用json方式序列化传入的任务参数，而原生的json.dumps()方法不支持datetime、date，这里做了扩展
    '''

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

host = '192.168.50.95'
port = 6379
class MyRedisQueue(object):
    
    def __init__(self):
        self.pool = redis.ConnectionPool(host=host, port=port, decode_responses=True)
        self.redis_connect = redis.Redis(connection_pool=self.pool)
        
    def get_len(self, key):
        keys = self.get_keys(key)
        # 每个键的任务数量
        key_len = [(k, self.redis_connect.llen(k)) for k in keys]
        # 所有键的任务数量
        task_len = sum(dict(key_len).values())
        return task_len, key_len

    def get_keys(self, key):
        # Redis的键支持模式匹配
        keys = self.redis_connect.keys(key + '-[0-9]*')
        # 按优先级将键降序排序
        keys = sorted(keys, key=lambda x: int(x.split('-')[-1]), reverse=True)
        return keys

    def push_task(self, key, tasks, level=1):
        '''
        双端队列，左边推进任务
        :param level: 优先级(int类型)，数值越大优先级越高，默认1
        :return: 任务队列任务数量
        '''
        # 重新定义优先队列的key
        new_key = key + '-' + str(level)
        # 序列化任务参数
        tasks = [json.dumps(t, cls=ExpandJsonEncoder) for t in tasks]

        print ('RedisQueue info > the number of push tasks:', len(tasks))

        if not tasks:
            return self.get_len(key)

        self.redis_connect.lpush(new_key, *tasks)
        return self.get_len(key)

    def pop_task(self, keys=None, priority=False):
        '''
        双端队列 右边弹出任务
        :param keys: 键列表，默认为None（将获取所有任务的keys）
        :return:
        '''
        while True:
            # 避免在while循环中修改参数，将keys参数赋值到临时变量
            temp_keys = keys

            # 不指定keys，将获取所有任务
            if not keys:
                temp_keys = self.redis_connect.keys()
                temp_keys = list(set([re.sub('-\d+$', '', k) for k in temp_keys if re.findall('\w+-\d+$', k)]))

            # 根据key作为关键字获取所有的键
            all_keys = list(chain(*[self.get_keys(k) for k in temp_keys]))

            # 屏蔽任务差异性，只按优先级高到低弹出任务
            if priority:
                all_keys = sorted(all_keys, key=lambda x: int(x.split('-')[-1]), reverse=True)

            if all_keys:
                task_key, task = self.redis_connect.brpop(all_keys)
                return task_key, json.loads(task)
            time.sleep(2)



def str_decode(s):
    try:
        return s.decode('utf-8')

    except UnicodeDecodeError:
        return s.decode('gbk')


def pop_report_task():
    redis_queue = MyRedisQueue()
    while True:
        task_type, task = redis_queue.pop_task(keys=['report'], priority=True)
        print (task_type, task,type(task))
        report_key = task_type.split('-')
        if task.get('batch_url'):
            outprint = subprocess.run(["allure", "generate", task['report_path'],"-o",task['batch']],stdout=subprocess.PIPE)
        u = 'http://192.168.50.129:5000/report/v1/reports'
        d = {
            'name':task['name'],
            'summarys':task,
            'testcase_id':report_key[2],
            'project_id':report_key[1],
            'config_name':task['config_name']
        }
        try:
            r = requests.post(u,json=d)
        except:
            r = requests.post(u,json=d)
            print('报告写入数据库，成功！')
        if r.status_code != 200 or r.json()['status'] != 0:
            print('调report新增接口失败！')


pop_report_task()