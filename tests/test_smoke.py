from app.settings import Settings


def test_settings_loads_without_secrets():
    s = Settings.load()
    assert s.app_env
    assert s.log_level
