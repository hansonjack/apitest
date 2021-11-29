from application import teststep
from infrastructure.teststep.teststep_repository import TeststepRepository
from domain.teststep.model.teststep_factory import TeststepFactory
from application.testcaseConfig.controller.testcaseConfig_controller import ConfigController
from application.debugtalk.controller.debugtalk_controller import DebugtalkController
from utils import list2dict,hr_export,hr_teststep,hr_yml,create_httprunner_projiect,db2web_data
import random
import os
import time

class TeststepController:

    def __init__(self):
        self.__teststep_repo = TeststepRepository()
        self.__teststep_factory = TeststepFactory(self.__teststep_repo)

    def get_teststep_list(self,project_id):
        return self.__teststep_repo.filter_by(project_id)

    def get_teststep(self, _id):
        return self.__teststep_repo.get_by_id(_id)

    def create_teststep(self, name, variables, request,validate,extract,setup_hooks,teardown_hooks,project_id):
        new_teststep = self.__teststep_factory.teststep_create(name, variables, request,validate,extract,setup_hooks,teardown_hooks,project_id)
        self.__teststep_repo.save(new_teststep)
        return new_teststep

    def update_teststep(self, _id, name, variables, request,validate,extract,setup_hooks,teardown_hooks):
        teststep = self.__teststep_factory.teststep_to_update(_id, name, variables, request,validate,extract,setup_hooks,teardown_hooks)
        self.__teststep_repo.save(teststep)

    def hr_testcase(self,data,isteststep=True):
        
        
        config_id = data.get('env').get('env')
        config_controller = ConfigController()
        config = config_controller.get_config(config_id).as_json()
        pre_apis = data.get('pre_apis') or []
        export = []
        teststeps = []
        ##前置teststep的提取参数,及teststep
        for i in pre_apis:
            teststep = self.get_teststep(i['pre_api']).as_json()
            export = export + hr_export(teststep.get('extract'))
            tmp = db2web_data(teststep)
            teststeps.append(hr_teststep(tmp))
          
        hr_config_data = {
            'name': data['name'], 
            'variables': list2dict(config.get('variables')),
            'base_url': config['base_url'], 
            'verify': False, 
            'export': export
            }
        if isteststep:
            teststeps.append(hr_teststep(data))
        # print('************&&&&&&&&&&&&&&&&&&&&&&&&&&&')  
        # print(pre_teststep)
        rand_str = str(random.randint(1,1000))
        hr_project_path,hr_testcase_path = create_httprunner_projiect(data['project_id'])
        time.sleep(1)
        yml_path = os.path.join(hr_testcase_path,rand_str+'.yml')
        hr_yml(yml_path,hr_config_data,teststeps)
        print(yml_path)

        ##每次生成testcase时都从数据库拿debugtalk写入到本地
        debugtalk_path = os.path.join(hr_project_path,'debugtalk.py')
        debugtalk_controller = DebugtalkController()
        debugtalk = debugtalk_controller.get_debugtalk_by_project_id(data['project_id']).as_json()
        if  debugtalk and debugtalk.get('debugtalktext'):
            debugtalk_controller.save_debugtalk_to_pyfile(debugtalk.get('debugtalktext'),debugtalk_path)
        
        return hr_project_path,yml_path,config['name']

    def get_select_teststeps(self,project_id):
        keyword = {
            'project_id':project_id
        }
        teststeps = self.__teststep_repo.get_many_by_keyword(keyword=keyword)


    