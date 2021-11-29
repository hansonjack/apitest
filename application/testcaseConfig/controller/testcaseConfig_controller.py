from infrastructure.testcaseConfig.testcaseConfig_repository import ConfigRepository
from domain.testcaseConfig.model.testcaseConfig_factory import TestConfigFactory


class ConfigController:

    def __init__(self):
        self.__config_repo = ConfigRepository()
        self.__config_factory = TestConfigFactory(self.__config_repo)

    def get_config_list(self,project_id):
        return self.__config_repo.filter_by(project_id)

    def get_config(self, _id):
        return self.__config_repo.get_by_id(_id)

    def create_config(self, name, verify, base_url,variables,parameters,export, path,weight,status,createtime,updatetime,project_id):
        new_config = self.__config_factory.config_create(name, verify, base_url,variables,parameters,export, path,weight,status,createtime,updatetime,project_id)
        self.__config_repo.save(new_config)
        return new_config

    def update_config(self, _id, name, base_url,variables,parameters,export,updatetime):
        teststep = self.__config_factory.config_to_update(_id, name, base_url,variables,parameters,export,updatetime)
        self.__config_repo.save(teststep)

    def get_config_by_project_id(self,project_id):
        tmp = self.__config_repo.filter_by(project_id)
        if not tmp:
            return
        return tmp[0]
