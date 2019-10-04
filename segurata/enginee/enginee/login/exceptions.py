class LoginBaseError(Exception):
    'Segurata was able not login.'
    pass

class NotLoggedInError(LoginGeneralError):
    'The css selector did not find any matching elements'
    pass
