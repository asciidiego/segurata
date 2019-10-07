import json
from json import JSONDecodeError
from .exceptions import *


def user_config_parse(path: str) -> dict:
    '''Return the user configuration as a Python `dict`.

    Raise:
        IncorrectExtensionError
        UserConfigNotFoundError
        UserConfigDecodeError
    '''
    if not path.lower().endswith('.json'):
        raise IncorrectExtensionError('File should end with `.json`.')
    try:
        with open(path) as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        raise UserConfigNotFoundError('User configuration was not found.')
    except JSONDecodeError:
        raise UserConfigDecodeError(
            'Could not decode user configuration.\n'
            'Have you tried validating it?'
        )

    return config
