from packages.shared.settings import settings


class BaseConfig:
    SECRET_KEY = settings.SECRET_KEY
    TEMPLATES_AUTO_RELOAD = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    DEBUG = False


config_by_env = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
