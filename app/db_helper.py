#
# DB Helper
#

import sqlalchemy
import sqlalchemy.orm

from config import app_config

def session():
    url = app_config.get('db', 'url')
    engine = sqlalchemy.create_engine(url, echo=False)

    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    return Session()


