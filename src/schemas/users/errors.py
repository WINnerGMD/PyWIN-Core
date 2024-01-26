class UserNotFoundError(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(message)


class InvalidCreditionalsError(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(message)


class AccountIsDisabledError(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(message)


class EmailIsAlreadyInUseError(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(message)


class UsernameIsAlreadyInUseError(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(message)
