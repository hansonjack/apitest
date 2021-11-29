from domain.testcaseConfig.model.testcaseConfig import TestConfig
from infrastructure.testcaseConfig.testcaseConfig_exceptions import testcaseConfigNotFoundException


class TestConfigFactory:
    def __init__(self,config_repo):
        self.__config_repo_repo = config_repo

    def config_create(self, name, verify, base_url,variables,parameters,export, path,weight,status,createtime,updatetime,project_id):
        config = TestConfig(name=name, verify=verify, base_url=base_url,
                            variables=variables,parameters=parameters,export=export,
                            path=path,weight=weight,status=status,
                            createtime=createtime,updatetime=updatetime,project_id=project_id)

        return config

    def config_to_update(self, _id, name, base_url,variables,parameters,export, updatetime):
        config = self.__config_repo_repo.get_by_id(_id)
        if not config:
            raise testcaseConfigNotFoundException(_id)

        config.name = name
        config.base_url = base_url
        config.variables = variables
        config.parameters = parameters
        config.export = export
        config.updatetime = updatetime

        return config