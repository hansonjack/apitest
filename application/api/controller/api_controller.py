from infrastructure.api.api_repository import ApiRepository
from domain.api.model.api_factory import ApiFactory


class ApiController:

    def __init__(self):
        self.__api_repo = ApiRepository()
        self.__api_factory = ApiFactory(self.__api_repo)

    def get_api_list(self):
        return self.__api_repo.get_all()

    def get_api(self, _id):
        return self.__api_repo.get_by_id(_id)

    def create_api(self, name, variables, request,validate,extract,setup_hooks):
        new_api = self.__api_factory.api_create(name, variables, request,validate,extract,setup_hooks)
        self.__api_repo.save(new_api)
        return new_api

    def update_api(self, _id, name, variables, request,validate,extract,setup_hooks):
        api = self.__api_factory.api_to_update(_id, name, variables, request,validate,extract,setup_hooks)
        self.__api_repo.save(api)
