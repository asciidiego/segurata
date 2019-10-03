import os
from pytest import mark
from pytest import raises, fixture
from segurata.enginee.enginee.user_config.parse import user_config_parse
from segurata.enginee.enginee.user_config.exceptions import *


PARAMETRIZE = mark.parametrize


@PARAMETRIZE('format', ['.csv', '.yaml', '.cfg'])
def test_incorrect_formats(format):
    dummy_path = f'./dummy{format}'
    with raises(IncorrectExtensionError):
        user_config_parse(dummy_path)


@fixture(params=['dummy.json', 'dummy.JSON', 'dummy.jSoN'])
def dummy_json_file(request):
    'Create and destroy dummy json files.'
    _file = request.param
    with open(_file, 'w') as f:
        f.write('{}')
    yield _file
    os.remove(_file)


def test_correct_formats(dummy_json_file):
    user_config = user_config_parse(dummy_json_file)
    assert isinstance(user_config, dict)
