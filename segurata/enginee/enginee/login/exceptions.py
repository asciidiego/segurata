class LoginBaseError(Exception):
    'Segurata was not able to login.'
    pass

class NotLoggedInError(LoginBaseError):
    'The css selector did not find any matching elements'
    pass
