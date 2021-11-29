from infrastructure.debugtalk.debugtalk_repository import DebugtalkRepository
from domain.debugtalk.model.debugtalk_factory import DebugtalkFactory
import subprocess
from utils import str_decode

class DebugtalkController:

    def __init__(self):
        self.__debugtalk_repo = DebugtalkRepository()
        self.__debugtalk_factory = DebugtalkFactory(self.__debugtalk_repo)

    def get_debugtalk_list(self,project_id):
        return self.__debugtalk_repo.filter_by(project_id)

    def get_debugtalk(self, _id):
        return self.__debugtalk_repo.get_by_id(_id)

    def create_debugtalk(self, debugtalktext, project_id):
        print('8888888888888888888888')
        print(debugtalktext)
        new_debugtalk = self.__debugtalk_factory.debugtalk_create( debugtalktext, project_id)
        print(new_debugtalk)
        self.__debugtalk_repo.save(new_debugtalk)
        return new_debugtalk

    def update_debugtalk(self, _id, debugtalktext):
        print('dsaaaaaaaaaaaaaaaaaaaa')
        print(debugtalktext)
        debugtalk = self.__debugtalk_factory.debugtalk_to_update(_id, debugtalktext)
        print(debugtalk)
        self.__debugtalk_repo.save(debugtalk)

    def save_debugtalk_to_pyfile(self,debugtalk,path):
        if debugtalk:
            with open(path,'w',encoding='utf-8') as f:
                f.write(debugtalk)

    def run(slef,path):
        resp = str_decode(subprocess.check_output(['python', path], stderr=subprocess.STDOUT, timeout=60))
        return resp

    def get_debugtalk_by_project_id(self,project_id):
        tmp =  self.__debugtalk_repo.get_one_by_keyword({'project_id':project_id})
        if not tmp:
            return
        return tmp

