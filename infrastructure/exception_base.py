class ExceptionBase(ValueError):
    def __init__(self, messages):
        if not isinstance(messages, list):
            messages = [messages]
        super().__init__(messages)



class ModelNotFoundException(ExceptionBase):
    def __init__(self, _id):
        if _id:
            message = '{} not found!'.format(_id)
        else:
            message = 'Data not found!'
        super().__init__(message)

class ModelException(ExceptionBase):
    def __init__(self, messages):
        super().__init__(messages)