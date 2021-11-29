from infrastructure.exception_base import ExceptionBase


class TestcaseException(ExceptionBase):
    def __init__(self, messages):
        super().__init__(messages)


class TestcaseNotFoundException(TestcaseException):
    def __init__(self, _id):
        if _id:
            message = 'testcase {} not found!'.format(_id)
        else:
            message = 'testcase not found!'
        super().__init__(message)
