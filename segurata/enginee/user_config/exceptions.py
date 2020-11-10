from json import JSONDecodeError


class UserConfigBaseException(Exception):
    'Exception for all user-config related issues.'
    pass


class IncorrectExtensionError(UserConfigBaseException):
    pass


class UserConfigNotFoundError(UserConfigBaseException):
    pass


class UserConfigJSONError(UserConfigBaseException):
    'Exception that tackles JSON-related issues'
    pass


class UserConfigDecodeError(UserConfigJSONError):
    pass
