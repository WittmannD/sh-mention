from dotenv import load_dotenv
import os

load_dotenv()


class BaseConfig(object):
    TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID', None)
    TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH', None)
    TELEGRAM_PHONE_NUMBER = os.getenv('TELEGRAM_PHONE_NUMBER', None)
    TELEGRAM_SESSION = os.getenv('TELEGRAM_SESSION', None)

    if TELEGRAM_API_ID is None or TELEGRAM_API_HASH is None:
        raise ValueError('env file is malformed, check .env file and try again')

    if TELEGRAM_PHONE_NUMBER is None and TELEGRAM_SESSION is None:
        raise ValueError('at least one "TELEGRAM_PHONE_NUMBER" or "TELEGRAM_SESSION" parameter must be defined. '
                         'check .env file and try again')

    TELEGRAM_SESSION = TELEGRAM_SESSION or 'bot'


class ProductionConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    pass


configs = {'development': DevelopmentConfig, 'production': ProductionConfig}
current_config = configs[os.getenv('ENV', 'development')]()
