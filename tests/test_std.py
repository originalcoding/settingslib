import pytest

from settingslib import Settings


def test_setting():
    settings = Settings()

    settings['foo'] = 'bar'
    assert not settings
    assert settings == {}
    assert not hasattr(settings, 'foo')

    settings['BAR'] = 'baz'
    assert settings
    assert settings == {'BAR': 'baz'}
    assert settings.BAR == 'baz'

    settings.BAR = 'bar'
    assert settings == {'BAR': 'bar'}
    assert settings['BAR'] == 'bar'


def test_getting(tmpdir, monkeypatch):
    settings1 = Settings(A=1, B=2)
    assert settings1.A == 1
    pytest.raises(AttributeError, lambda: settings1.a)
    assert settings1.get('a') == None
    assert settings1.get('a', 42) == 42
    assert settings1['A'] == 1
    pytest.raises(KeyError, lambda: settings1['a'])

    module_name, module_dir = 'somemodule', tmpdir.mkdir('test_getting')
    module = module_dir.join(module_name + '.py')
    module.write('obj = {\'foo\': \'bar\'}')
    monkeypatch.syspath_prepend(str(module_dir))
    setting_name, setting_value = 'OBJ_FROM_OTHER_MODULE', module_name + ':obj'
    
    settings2 = Settings({setting_name: setting_value})
    assert settings2.get(setting_name, imp=True) == {'foo': 'bar'}
    assert settings2.get(setting_name, 'smth', imp=True) == {'foo': 'bar'}
    assert settings2.get(setting_name) == setting_value
    assert settings2.get('bbb', imp=True) is None
    assert settings2.get('aaa', 123, imp=True) == 123


def test_deleting():
    settings = Settings(A=1, B=2, C=3)

    delattr(settings, 'A')
    assert settings == {'B': 2, 'C': 3}
    pytest.raises(KeyError, lambda: settings['A'])
    pytest.raises(AttributeError, lambda: settings.A)

    del settings['C']
    assert settings == {'B': 2}
    pytest.raises(AttributeError, lambda: settings.C)
    pytest.raises(KeyError, lambda: settings['C'])

    def test_del():
        del settings['123']

    pytest.raises(KeyError, test_del)
    pytest.raises(AttributeError, lambda: delattr(settings, '123'))

    assert settings == {'B': 2}
    assert settings.__dict__ == {'B': 2}


def test_comparing_for_equality():
    settings1 = Settings()
    settings2 = Settings({})
    settings3 = Settings({}, {})
    
    assert settings1 == settings2
    assert settings2 == settings3
    assert settings1 != {'a': 1}

    settings4 = Settings(A=1, B=2)
    settings5 = Settings({'b': 1}, {'A': 1}, B=2)

    assert settings4 == {'A': 1, 'B': 2}
    assert settings4 == settings5


def test_updating(check_settings):
    expected_data = {'A': 1, 'B': 2, 'C': 3, 'D': 4}

    settings = Settings()
    settings.update({'A': 1, 'foo': 'bar'}, B=2, C=3)
    settings.update(D=4, bar='baz')

    settings = check_settings(settings, expected_data)

    settings.update()  # we can do this on dict


def test_copying():
    settings1 = Settings(A=1)
    settings2 = settings1.copy()

    assert not settings1 is settings2
    assert settings1 == settings2
    
    assert settings2.A == 1

    settings2['A'] = 2
    
    assert settings1.A != 2
    assert settings2.A == 2


def test_adding(check_settings):
    expected_data = {'A': 26, 'B': 2, 'C': 24}

    settings1 = Settings(A=1, B=2)
    settings2 = Settings(C=24, A=26)

    combined_settings = settings1 + settings2

    assert combined_settings != settings1
    assert combined_settings != settings2

    combined_settings = check_settings(combined_settings, expected_data)

    expected_data['A'] = 1
    combined_settings += dict(A=1)

    combined_settings = check_settings(combined_settings, expected_data)

    expected_data['A'] = -3
    combined_settings = combined_settings + dict(A=-3)
    
    check_settings(combined_settings, expected_data)

