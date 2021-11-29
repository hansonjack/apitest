from infrastructure.exception_base import ExceptionBase


class ApiException(ExceptionBase):
    def __init__(self, messages):
        super().__init__(messages)


class ApiNotFoundException(ApiException):
    def __init__(self, _id):
        if _id:
            message = 'Api {} not found!'.format(_id)
        else:
            message = 'Api not found!'
        super().__init__(message)
