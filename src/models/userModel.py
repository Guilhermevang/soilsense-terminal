class UserModel:
    _email          :str = None
    _access_token   :str = None
    _active         :bool = False
        
    def __init__(self) -> None:
        self.email          :str = UserModel._email
        self.access_token   :str = UserModel._access_token
        self.active         :bool = UserModel._active