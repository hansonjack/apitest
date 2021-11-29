from infrastructure.exception_base import ExceptionBase


class StudentException(ExceptionBase):
    def __init__(self, messages):
        super().__init__(messages)


class StudentNotFoundException(StudentException):
    def __init__(self, _id):
        if _id:
            message = 'Student {} not found!'.format(_id)
        else:
            message = 'Student not found!'
        super().__init__(message)
