from infrastructure.exception_base import ExceptionBase


class DebugtalkException(ExceptionBase):
    def __init__(self, messages):
        super().__init__(messages)


class DebugtalkNotFoundException(DebugtalkException):
    def __init__(self, _id):
        if _id:
            message = 'debugtalk {} not found!'.format(_id)
        else:
            message = 'debugtalk not found!'
        super().__init__(message)
