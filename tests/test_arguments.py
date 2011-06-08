import sys
import types

import pytest

from settingslib import Settings


def py(path):
    return path + '.py'


def test_empty_arguments():
    settings1 = Settings()
    assert not settings1

    settings2 = Settings({})
    assert not settings2

    settings3 = Settings({}, {}, {})
    assert not settings3


def test_single_argument():
    settings = Settings({'a': 1})
    assert not settings

    settings = Settings({'A': 1})
    assert settings
    assert settings == {'A': 1}
    assert settings.A == 1


def test_few_arguments():
    settings1 = Settings(A=1, b=2)
    assert settings1
    assert settings1 == {'A': 1}
    assert settings1.A == 1
    assert not hasattr(settings1, 'b')

    settings2 = Settings({}, A=1)
    assert settings2
    assert settings2 == {'A': 1}
    assert settings2.A == 1

    assert settings1 == settings2


def test_class_and_instance_arguments():
    class MyObj(object):
        a = 1
        B = 2

    settings1 = Settings(MyObj)
    assert settings1
    assert settings1 == {'B': 2}
    assert settings1.B == 2
    assert not hasattr(settings1, 'a')

    settings2 = Settings(MyObj())
    assert settings2
    assert settings2 == {'B': 2}
    assert settings2.B == 2
    assert not hasattr(settings2, 'a')

    assert settings1 == settings2


def test_module_argument():
    module_name = 'testmodule'
    module = types.ModuleType(module_name)
    module.B = 2
    module.a = 1

    settings = Settings(module)
    assert settings
    assert settings == {'B': 2}
    assert settings.B == 2
    assert not hasattr(settings, 'a')

    assert 'settings' not in sys.modules
    assert module_name not in sys.modules


def test_generator_argument():
    def settings_generator():
        for k, v in (('a', 1), ('B', 2)):
            yield k, v

    settings = Settings(settings_generator())
    assert settings
    assert settings == {'B': 2}
    assert settings.B == 2
    assert not hasattr(settings, 'a')


def test_module_name_argument(tmpdir, monkeypatch, check_settings):
    pytest.raises(ImportError, lambda: Settings('settings'))

    module_data = {'ONE': 1, 'TWO': 2, 'THREE': 3, 'NOT_THREE': 4}
    module_name = 'testsettingsmodule'
    module_dir = tmpdir.mkdir('test_module_name_argument')
    module = module_dir.join(py(module_name))
    module.write('''ONE = 1
TWO = 2


THREE = 3


# Some comment.
NOT_THREE = 4

''')
    monkeypatch.syspath_prepend(str(module_dir))

    check_settings(module_name, module_data)

    assert 'settings' not in sys.modules
    assert module_name not in sys.modules


def test_module_and_object_path_notation_argument(
    tmpdir, monkeypatch, check_settings
):
    pytest.raises(ImportError, lambda: Settings('a.b.c'))
    pytest.raises(ImportError, lambda: Settings('bar:foo'))
    pytest.raises(ImportError, lambda: Settings('bar::foo'))

    pkg_name = 'test_module_name_argument'
    pkg_dir = tmpdir.mkdir(pkg_name)
    monkeypatch.syspath_prepend(str(tmpdir))

    pkg_variable_name = 'some_configuration'
    pkg_variable_data = {'FOO': 'bar'}
    pkg_dir.join('__init__.py').write(
        '%s = %r' % (pkg_variable_name, pkg_variable_data)
    )

    module_one_data = {'ONE': 1, 'TWO': 2, 'THREE': 3, 'NOT_THREE': 4}
    module_one_name = 'testsettingsmodule'
    module_one = pkg_dir.join(py(module_one_name))
    module_one.write('''ONE = 1
TWO = 2


THREE = 3


# Some comment.
NOT_THREE = 4

''')

    module_two_name = 'othertestsettingsmodule'
    module_two = pkg_dir.join(py(module_two_name))
    module_two_variable_name = 'conf'
    module_two_variable_data = {'HERE': '1', 'FOO': 'Bar'}
    module_two.write(
        '%s = %r' % (module_two_variable_name, module_two_variable_data)
    )

    check_settings(':'.join((pkg_name, pkg_variable_name)), pkg_variable_data)
    check_settings('.'.join((pkg_name, module_one_name)), module_one_data)
    check_settings(
        '%s.%s:%s' % (pkg_name, module_two_name, module_two_variable_name),
        module_two_variable_data
    )
    
    assert 'settings' not in sys.modules
    assert pkg_name not in sys.modules
    assert module_one_name not in sys.modules
    assert module_two_name not in sys.modules


def test_environment_variable_name_argument(tmpdir, monkeypatch, check_settings):
    env_variable_name = (
        'ENV_VARIABLE_WITH_UNIQUE_'
        'NAME_OF_TEST_SETTINGS_MODULE'
    )
    module_data = {'ONE': 1, 'TWO': 2, 'THREE': 3, 'NOT_THREE': 4}
    module_name = 'envtestsettingsmodule'
    module_dir = tmpdir.mkdir('test_environment_variable_name_argument')
    module = module_dir.join(py(module_name))
    module.write('''ONE = 1
TWO = 2


THREE = 3


# Some comment.
NOT_THREE = 4

''')
    monkeypatch.syspath_prepend(str(module_dir))
    monkeypatch.setenv(env_variable_name, module_name)

    check_settings(env_variable_name, module_data)

    assert 'settings' not in sys.modules


def test_path_to_python_module_argument(tmpdir, check_settings):
    test_dir = tmpdir.mkdir('test_path_to_python_module_argument')

    # Nonexisting file.
    pytest.raises(
        IOError,
        lambda: Settings(str(test_dir.join('settings')))
    )

    # Empty file.
    empty_module = test_dir.join('config')
    empty_module.write('')
    
    empty_settings = Settings(str(empty_module))
    assert not empty_settings
    assert empty_settings == {}

    # Non-empty .py file.
    modules_data = {
        'LETTERS': {'a': 1, 'b': 2},
        'NUMBERS': [1, 2, 3],
        'STRING': 'one.two.three',
    }
    module_contents = '''# -*- coding: utf-8 -*-

LETTERS = {'a': 1, 'b': 2}

NUMBERS = [1, 2, 3]  # another comment.

# Some comment.
STRING = 'one.two.three'
'''

    module_py = test_dir.join('settings.py')
    module_py.write(module_contents)

    settings_py = check_settings(str(module_py), modules_data)

    # Non-empty .py.local file.
    module_py_local = test_dir.join('settings.py.local')
    module_py_local.write(module_contents)
    
    settings_py_local = check_settings(str(module_py_local), modules_data)

    # .py and .py.local files have equal contents.
    assert settings_py == settings_py_local

    assert 'settings' not in sys.modules

