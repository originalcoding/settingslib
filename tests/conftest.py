from settingslib import Settings


def pytest_funcarg__check_settings(request):
    
    def check_settings(arg, expected_data):
        if not isinstance(arg, Settings):
            settings = Settings(arg)
        else:
            settings = arg  # reuse passed instance
        
        assert settings == expected_data
        
        for k, v in expected_data.items():
            assert getattr(settings, k) == v
            
        return settings

    return check_settings

