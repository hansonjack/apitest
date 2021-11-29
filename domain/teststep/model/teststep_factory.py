from domain.teststep.model.teststep import Teststep
from infrastructure.teststep.teststep_exceptions import TeststepNotFoundException


class TeststepFactory:
    def __init__(self,teststep_repo):
        self.__teststep_repo_repo = teststep_repo

    def teststep_create(self, name, variables, request,validate,extract,setup_hooks,teardown_hooks,project_id):
        teststep = Teststep(name=name, variables=variables, request=request,validate=validate,extract=extract,setup_hooks=setup_hooks,teardown_hooks=teardown_hooks,project_id=project_id)

        return teststep

    def teststep_to_update(self, _id, name, variables, request,validate,extract,setup_hooks,teardown_hooks):
        teststep = self.__teststep_repo_repo.get_by_id(_id)
        if not teststep:
            raise TeststepNotFoundException(_id)

        teststep.name = name
        teststep.variables = variables
        teststep.request = request
        teststep.validate = validate
        teststep.extract = extract
        teststep.setup_hooks = setup_hooks
        teststep.teardown_hooks = teardown_hooks

        return teststep