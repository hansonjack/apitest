from domain.testcase.model.testcase import Testcase,TestcaseDetail
from infrastructure.exception_base import ModelNotFoundException
import time

daytime = time.localtime()

class TestcaseFactory:
    def __init__(self,testcase_repo):
        self.__testcase_repo = testcase_repo

    def testcase_create(self, name, creator, project_id,env):
        testcase = Testcase(name=name, creator=creator, project_id=project_id,create_time=daytime,update_time=daytime,env=env)

        return testcase

    def testcase_to_update(self, _id, name,env):
        testcase = self.__testcase_repo.get_by_id(_id)
        if not testcase:
            raise ModelNotFoundException(_id)

        testcase.name = name
        testcase.env = env
        testcase.update_time = daytime

        return testcase

class TestcaseDetailFactory:
    def __init__(self,testcase_detail_repo):
        self.__testcase_detail_repo = testcase_detail_repo

    def testcase_detail_create(self, testcase_id, teststep_id,name, variables,validate,extract,setup_hooks,teardown_hooks,request):
        
        
        testcase_detail = TestcaseDetail(
            testcase_id=testcase_id, 
            teststep_id=teststep_id,
            name=name, 
            variables=variables,
            validate=validate,
            extract=extract,
            setup_hooks=setup_hooks,
            teardown_hooks=teardown_hooks,
            request=request
            )

        return testcase_detail

    def testcase_detail_to_update(self, _id,name, variables,validate,extract,setup_hooks,teardown_hooks,request):
        testcase_detail = self.__testcase_detail_repo.get_by_id(_id)
        if not testcase_detail:
            raise ModelNotFoundException(_id)
        testcase_detail.name = name
        testcase_detail.variables = variables
        testcase_detail.validate = validate
        testcase_detail.extract = extract
        testcase_detail.setup_hooks = setup_hooks
        testcase_detail.teardown_hooks = teardown_hooks
        testcase_detail.request = request

        return testcase_detail