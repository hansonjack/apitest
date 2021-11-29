from domain.debugtalk.model.debugtalk import Debugtalk
from infrastructure.debugtalk.debugtalk_exceptions import DebugtalkNotFoundException


class DebugtalkFactory:
    def __init__(self,debugtalk_repo):
        self.__debugtalk_repo_repo = debugtalk_repo

    def debugtalk_create(self, debugtalktext, project_id):
        print('pppppppppppppppppppppp1211111111111111111111')
        print(debugtalktext)
        debugtalk = Debugtalk(debugtalktext=debugtalktext, project_id=project_id)

        return debugtalk

    def debugtalk_to_update(self, _id, debugtalktext):
        debugtalk = self.__debugtalk_repo_repo.get_by_id(_id)
        if not debugtalk:
            raise DebugtalkNotFoundException(_id)

        debugtalk.debugtalktext = debugtalktext

        return debugtalk