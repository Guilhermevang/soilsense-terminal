class CommonBaseException(BaseException):
    def __init__(self, message:str) -> None:
        self.message:str = message
        super().__init__(message)

class InvalidValue(CommonBaseException):
    pass

class RestException(CommonBaseException):
    pass

class NotAuthorized(CommonBaseException):
    pass