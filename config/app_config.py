import configparser
import os


def _detect_env(env = None):
    # Priority
    # arg env > os.environ['APP_ENV'] > default(None)
    if env:
        return env

    app_env = os.environ.get('APP_ENV')
    if app_env:
        return app_env

    return None


class AppConfig:
    def __init__(self, env = None):
        self.config = None
        self.env = _detect_env(env)
        self._load_config()


    def _load_config(self):
        # load config file
        cfg_file_path = f"./config/app.ini"
        if self.env:
            cfg_file_path = f"./config/app.{self.env}.ini"
        self.config = configparser.ConfigParser()
        self.config.read(cfg_file_path)

        # setup db url
        self.config.set('db', 'url', '{}+{}://{}:{}@{}:{}/{}'.format(
            self.config.get('db', 'dialect'),
            self.config.get('db', 'driver'),
            self.config.get('db', 'username'),
            self.config.get('db', 'password'),
            self.config.get('db', 'host'),
            self.config.get('db', 'port'),
            self.config.get('db', 'database')
        ))


    def get(self, section, option):
        return self.config.get(section, option)


