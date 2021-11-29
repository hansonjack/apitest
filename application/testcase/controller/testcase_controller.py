from infrastructure.testcase.testcase_repository import TestcaseRepository,TestcaseDetailRepository
from domain.testcase.model.testcase_factory import TestcaseDetailFactory,TestcaseFactory
from infrastructure.teststep.teststep_repository import TeststepRepository
from domain.teststep.model.teststep_factory import TeststepFactory
from infrastructure.testcaseConfig.testcaseConfig_repository import ConfigRepository
from application.testcaseConfig.controller.testcaseConfig_controller import ConfigController
from application.debugtalk.controller.debugtalk_controller import DebugtalkController
from infrastructure.teststep.teststep_repository import TeststepRepository
from application.teststep.controller.teststep_controller import TeststepController
import time
from utils import list2dict,hr_export,hr_teststep,hr_yml,create_httprunner_projiect,db2web_data
import random
import os
from infrastructure.redis_operation.redis_task import push_hr_task
from application.project.controller.project_controller import ProjectController

class TestcaseController:

    def __init__(self):
        self.__testcase_repo = TestcaseRepository()
        self.__testcase_factory = TestcaseFactory(self.__testcase_repo)
        self.__testcase_detail_repo = TestcaseDetailRepository()
        self.__testcase_detail_factory = TestcaseDetailFactory(self.__testcase_detail_repo)
        self.__teststep_repo = TeststepRepository()
        self.__config_repo = ConfigRepository()

    def get_testcase_list(self,project_id):
        testcases = self.__testcase_repo.get_many_by_keyword({'project_id':project_id})[::-1]
        tmp = []
        for i in testcases:
            testcase = i.as_json()
            tmp.append(self.get_testcase(testcase['id']))
        return tmp

    def get_testcase(self, _id):
        details = self.__testcase_detail_repo.get_many_by_keyword({'testcase_id':_id})
        tmp = []
        pre_apis = []
        for i in details:
            tmp.append(i.as_json())
            tmp1 = i.as_json()
            pre_apis.append({'pre_api':str(tmp1['teststep_id'])+'_'+str(_id)})
        testcase = self.__testcase_repo.get_by_id(_id).as_json()
        config = self.__config_repo.get_by_id(testcase['env']).as_json()
        env = testcase.pop('env')
        testcase['config'] = config
        testcase['env'] = {'env':env}
        testcase['teststeps'] = tmp
        testcase['teststeps_count'] = len(tmp)
        testcase['pre_apis'] = pre_apis
        print(testcase['teststeps'])
        return testcase

    def create_testcase(self, name, creator, project_id,env,teststeps):
        new_testcase = self.__testcase_factory.testcase_create(name, creator, project_id,env)
        new_testcase_id = self.__testcase_repo.save(new_testcase)
        ##为了方便，新增详情前，把该tescae的详情先删掉
        keyword = {'testcase_id':new_testcase_id}
        testcase_detail = self.__testcase_detail_repo.get_many_by_keyword(keyword)
        if testcase_detail:
            self.__testcase_detail_repo.delete(testcase_detail)

        for teststep in teststeps:
            teststep = self.__teststep_repo.get_by_id(teststep['pre_api']).as_json()
            new_detail = self.__testcase_detail_factory.testcase_detail_create(
                testcase_id=new_testcase_id, 
                teststep_id=teststep['id'],
                name=teststep['name'],
                variables=teststep['variables'], 
                validate=teststep['validate'], 
                extract=teststep['extract'], 
                setup_hooks=teststep['setup_hooks'], 
                teardown_hooks=teststep['teardown_hooks'],
                request=teststep['request']
            )
            self.__testcase_detail_repo.save(new_detail)
        return new_testcase

    def update_testcase(self, _id, name, env,teststeps):
        testcase = self.__testcase_factory.testcase_to_update(_id, name,env)
        testcase_id = self.__testcase_repo.save(testcase)
        ##为了方便，新增详情前，把该tescae的详情先删掉
        keyword = {'testcase_id':testcase_id}
        testcase_detail = self.__testcase_detail_repo.get_many_by_keyword(keyword)
        if testcase_detail:
            self.__testcase_detail_repo.delete(testcase_detail)
        for teststep in teststeps:
            teststep = self.__teststep_repo.get_by_id(teststep['pre_api']).as_json()
            new_detail = self.__testcase_detail_factory.testcase_detail_create(
                testcase_id=testcase_id, 
                teststep_id=teststep['id'],
                name=teststep['name'],
                variables=teststep['variables'], 
                validate=teststep['validate'], 
                extract=teststep['extract'], 
                setup_hooks=teststep['setup_hooks'], 
                teardown_hooks=teststep['teardown_hooks'],
                request=teststep['request']

            )
            self.__testcase_detail_repo.save(new_detail)

    def hr_testcase_with_run(self,data):
        teststep_controller = TeststepController()
        config_id = data.get('env').get('env')
        config_controller = ConfigController()
        config = config_controller.get_config(config_id).as_json()
        pre_apis = data.get('pre_apis') or []
        export = []
        teststeps = []
        ##前置teststep的提取参数,及teststep
        for i in pre_apis:
            teststep = teststep_controller.get_teststep(i['pre_api']).as_json()
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
        rand_str = time.strftime("%Y%m%d%H%M%S", time.localtime()) + str(random.randint(1,1000))
        testcase_id = data.get('id')
        if testcase_id:
            testcase_name = 'testcase_'+str(data['id']) + '_' +rand_str
        else:
            testcase_name = 'testcase_new_'+rand_str 
            
        hr_paths = ProjectController().hrproject_paths(int(data['project_id']))
        yml_path = os.path.join(hr_paths['hr_testcases'],testcase_name+'.yml')
        hr_yml(yml_path,hr_config_data,teststeps)
        print(yml_path)
        ##每次生成testcase时都从数据库拿debugtalk写入到本地
        debugtalk_path = os.path.join(hr_paths['hr_root'],'debugtalk.py')
        debugtalk_controller = DebugtalkController()
        debugtalk = debugtalk_controller.get_debugtalk_by_project_id(data['project_id']).as_json()
        if  debugtalk and debugtalk.get('debugtalktext'):
            debugtalk_controller.save_debugtalk_to_pyfile(debugtalk.get('debugtalktext'),debugtalk_path)
        report_url = str(data['project_id']) + '/reports/' + testcase_name + '.html'
        log_url = str(data['project_id']) + '/logs/' + 'test.log'
        yml_url = str(data['project_id']) + '/testcases/' + testcase_name + '.yml'
        debugtalk_url = str(data['project_id']) + '/debugtalk.py'
        ##推送yml到redis
        task = {
            'report_path':hr_paths['hr_reports'],
            'ymlpath':[yml_path],
            'name':testcase_name,
            'log_path':hr_paths['hr_logs'],
            'config_name':config['name'],
            'debugtalk':debugtalk.get('debugtalktext'),
            'report_url':report_url,
            'log_url':log_url,
            'yml_url':yml_url,
            'debugtalk_url':debugtalk_url
        }
        
        print('====================555555555555555555555555555555555')
        testcase_debug = data.get('testcase_debug') 
        print(testcase_debug)
        ###任务KEY，projectid_testcaseid_testcasedebug;若testcase新增，则testcaseid=new;若为批量运行则testcaseid=all
        if testcase_id:
            if testcase_debug:##编辑时运行hrun
                task_info = push_hr_task(data['project_id'],data['id'],task)
            else:##列表中运行hrun
                task_info = push_hr_task(data['project_id'],data['id'],task,debug=0)
        else:
            task_info = push_hr_task(data['project_id'],'new',task)
        print(task_info)
        return hr_paths['hr_root'],yml_path,config['name'],task_info

    def hr_testcase(self,testcase,env):
        config_id = env
        config_controller = ConfigController()
        config = config_controller.get_config(config_id).as_json()
        pre_apis = testcase.get('teststeps') or []
        export = []
        teststeps = []
        ##前置teststep的提取参数,及teststep
        for teststep in pre_apis:
            export = export + hr_export(teststep.get('extract'))
            tmp = db2web_data(teststep)
            teststeps.append(hr_teststep(tmp))
          
        hr_config_data = {
            'name': testcase['name'], 
            'variables': list2dict(config.get('variables')),
            'base_url': config['base_url'], 
            'verify': False, 
            'export': export
            }
        
    
        return hr_config_data,teststeps

    def hr_testcases(self,testcases,env,project):
        config_id = env
        config_controller = ConfigController()
        config = config_controller.get_config(config_id).as_json()
        hr_paths = ProjectController().hrproject_paths(int(project))
        ##每次生成testcase时都从数据库拿debugtalk写入到本地
        debugtalk_controller = DebugtalkController()
        debugtalk = debugtalk_controller.get_debugtalk_by_project_id(project).as_json()
        if  debugtalk and debugtalk.get('debugtalktext'):
            debugtalk_controller.save_debugtalk_to_pyfile(debugtalk.get('debugtalktext'),hr_paths['hr_debugtalk'])
        time.sleep(1)
        yml_paths = []
        yml_urls = []
        hr_paths = ProjectController().hrproject_paths(int(project))
        for i in testcases:
            hr_config_data,teststeps = self.hr_testcase(i,env)
            rand_str = time.strftime("%Y%m%d%H%M%S", time.localtime()) + str(random.randint(1,1000))
            testcase_name = 'testcase_' + str(i['id']) + '_' + rand_str
            yml_path = os.path.join(hr_paths['hr_testcases'],testcase_name+'.yml')
            yml_urls.append(str(project)+'/testcases/'+ testcase_name+'.yml' )
            hr_yml(yml_path,hr_config_data,teststeps)
            yml_paths.append(yml_path)
            
        print(yml_paths)
        ##推送yml到redis
        report_url = str(project) + '/reports/' + 'batch_run_' + rand_str +'.html'
        log_url = str(project) + '/logs/' + 'test.log'
        debugtalk_url = str(project) + '/debugtalk.py'
        ##推送yml到redis
        task = {
            'report_path':hr_paths['hr_reports'],
            'ymlpath':yml_paths,
            'name':'batch_run_'+rand_str,
            'log_path':hr_paths['hr_logs'],
            'config_name':config['name'],
            'debugtalk':debugtalk.get('debugtalktext'),
            'report_url':report_url,
            'log_url':log_url,
            'yml_urls':yml_urls,
            'debugtalk_url':debugtalk_url
        }
        task_info = push_hr_task(project,'all',task,debug=0)
        return hr_paths,yml_paths,task_info

    def get_testcase_detail(self,testcase_id):
        details = self.__testcase_detail_repo.get_many_by_keyword({'testcase_id':testcase_id})
        return details

    def testcase_teststep(self,teststep_id_and_testcase_id):
        if not teststep_id_and_testcase_id:
            return {'msg':'传参不能为空'}
        teststep_id = int(teststep_id_and_testcase_id.split('_')[0])
        testcase_id = int(teststep_id_and_testcase_id.split('_')[1])
        if testcase_id:
            keyword = {
                'testcase_id':testcase_id,
                'teststep_id':teststep_id
            }
            teststep = self.__testcase_detail_repo.get_by_and({'testcase_id':testcase_id},{'teststep_id':teststep_id})
        else:
            teststep = TeststepRepository().get_by_id(teststep_id)
        return teststep

    def update_testcase_detail(self, _id,  name, variables, validate, extract, setup_hooks, teardown_hooks, request):
        detail = self.__testcase_detail_factory.testcase_detail_to_update(_id, name, variables, validate, extract, setup_hooks, teardown_hooks, request)
        self.__testcase_detail_repo.save(detail)

