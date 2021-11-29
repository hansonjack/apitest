from infrastructure.exception_base import ExceptionBase


class ProjectException(ExceptionBase):
    def __init__(self, messages):
        super().__init__(messages)


class ProjectNotFoundException(ProjectException):
    def __init__(self, _id):
        if _id:
            message = 'project {} not found!'.format(_id)
        else:
            message = 'project not found!'
        super().__init__(message)
