from domain.api.model.api import Api
from infrastructure.api.api_exceptions import ApiNotFoundException


class ApiFactory:
    def __init__(self,
                 api_repo):
        self.__api_repo = api_repo

    def api_create(self, name, variables, request,validate,extract,setup_hooks):
        api = Api(name=name, variables=variables, request=request,validate=validate,extract=extract,setup_hooks=setup_hooks)

        return api

    def api_to_update(self, _id, name, variables, request,validate,extract,setup_hooks):
        api = self.__api_repo.get_by_id(_id)
        if not api:
            raise ApiNotFoundException(_id)

        api.name = name
        api.variables = variables
        api.request = request
        api.validate = validate
        api.extract = extract
        api.setup_hooks = setup_hooks

        return api
