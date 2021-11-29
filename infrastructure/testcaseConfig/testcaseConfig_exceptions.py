from infrastructure.exception_base import ExceptionBase


class TestcaseConfigException(ExceptionBase):
    def __init__(self, messages):
        super().__init__(messages)


class testcaseConfigNotFoundException(TestcaseConfigException):
    def __init__(self, _id):
        if _id:
            message = 'Config {} not found!'.format(_id)
        else:
            message = 'Config not found!'
        super().__init__(message)
