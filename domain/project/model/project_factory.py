from domain.project.model.project import Project
from infrastructure.project.project_exceptions import ProjectNotFoundException


class ProjectFactory:
    def __init__(self,
                 project_repo):
        self.__project_repo = project_repo

    def project_create(self, name, desc,hrproject_path=None):
        project = Project(name=name, desc=desc,hrproject_path=hrproject_path)

        return project

    def project_to_update(self, _id, name, desc,hrproject_path):
        project = self.__project_repo.get_by_id(_id)
        if not project:
            raise ProjectNotFoundException(_id)

        project.name = name
        project.desc = desc
        project.hrproject_path = hrproject_path

        return project
