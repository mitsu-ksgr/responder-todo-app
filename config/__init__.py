#
# App config
#

import configparser

def __load_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

app_config = __load_config('./config/app.ini')
app_config.set('db', 'url', '{}+{}://{}:{}@{}:{}/{}'.format(
    app_config.get('db', 'dialect'), app_config.get('db', 'driver'),
    app_config.get('db', 'username'), app_config.get('db', 'password'),
    app_config.get('db', 'host'), app_config.get('db', 'port'),
    app_config.get('db', 'database')
))

