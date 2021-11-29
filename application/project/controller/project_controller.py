from application import debugtalk
from infrastructure.project.project_repository import ProjectRepository
from domain.project.model.project_factory import ProjectFactory
from application.debugtalk.controller.debugtalk_controller import DebugtalkController
from utils import create_httprunner_projiect
import os

class ProjectController:

    def __init__(self):
        self.__project_repo = ProjectRepository()
        self.__project_factory = ProjectFactory(self.__project_repo)

    def get_project_list(self):
        return self.__project_repo.get_all()

    def get_project(self, _id):
        return self.__project_repo.get_by_id(_id)

    def get_project_by_id(self, id):
        return self.__project_repo.get_by_id(id)

    def create_project(self, name, desc):
        new_project = self.__project_factory.project_create(name, desc)
        self.__project_repo.save(new_project)
        
        return new_project

    def update_project(self, _id, name, desc,hrproject_path):
        project = self.__project_factory.project_to_update(_id, name, desc,hrproject_path)
        self.__project_repo.save(project)
    
    def create_reports_dir(self,_id):
        root_path = os.getcwd()
        static = os.path.join(root_path,'static')
        project = os.path.join(static,str(_id))
        report = os.path.join(project,'reports')
        log = os.path.join(project,'logs')
        if not os.path.isdir(report):
            print("Project folder {report} exists, please specify a new project name.".format(report))
            return report
        os.makedirs(report)
        os.makedirs(log)
        return report

    def hrproject_paths(self,_id):
        project = self.get_project(_id).as_json()
        hr_root = project['hrproject_path']
        if not hr_root:
            hr_root,testcase = create_httprunner_projiect(str(_id))
            self.update_project(_id,project['name'],project['desc'],hr_root)
            ##创建hr项目同时新增debugtalk到数据库
            hr_debugtalk = os.path.join(hr_root,'debugtalk.py')
            with open(hr_debugtalk,'r',encoding='utf-8') as f:
                debugtalk_controller = DebugtalkController()
                debugtalk_controller.create_debugtalk(f.read(),_id)


        hr_testcases = os.path.join(hr_root,'testcases')
        hr_reports = os.path.join(hr_root,'reports')
        hr_logs = os.path.join(hr_root,'logs')
        hr_debugtalk = os.path.join(hr_root,'debugtalk.py')
        hr_env = os.path.join(hr_root,'.env')
        hr_paths = {
            'hr_root':hr_root,
            'hr_testcases':hr_testcases,
            'hr_reports':hr_reports,
            'hr_debugtalk':hr_debugtalk,
            'hr_env':hr_env,
            'hr_logs':hr_logs
        }
        

        return hr_paths
