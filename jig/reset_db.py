#!/bin/env python

import argparse
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from config import app_config


def dump_db_info():
    print(f"Dialect : {app_config.get('db', 'dialect')}")
    print(f"Driver  : {app_config.get('db', 'driver')}")
    print(f"Host    : {app_config.get('db', 'host')}")
    print(f"Port    : {app_config.get('db', 'port')}")
    print(f"UserName: {app_config.get('db', 'username')}")
    print(f"URL     : {app_config.get('db', 'url')}")


def reset_db():
    import alembic.config
    import sqlalchemy

    # cleanup db
    engine = sqlalchemy.create_engine(app_config.get("db", "url"), echo=False)
    results = engine.execute("SHOW TABLES")
    for result in results:
        table = result[0]
        engine.execute(f"DROP TABLE IF EXISTS {table}")

    # migrate to head
    argv = ["upgrade", "head"]
    alembic.config.main(argv=argv)


def gen_dummy_users():
    import app.helpers.db_helper
    from db.dummy.users import generate_serial_users, generate_fake_users

    session = app.helpers.db_helper.session()
    session.bulk_save_objects(generate_serial_users())
    session.bulk_save_objects(generate_fake_users())
    session.commit()
    session.close()
    print("dummy users generated.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Reset the DB.')
    parser.add_argument(
        '--with-dummy-data',
        help="generate dummy data after reset",
        action='store_true')
    args = parser.parse_args()

    print("* Database Connection")
    dump_db_info()

    print("\n\n* Reset databases")
    reset_db()

    if args.with_dummy_data:
        print("\n\n* Generate dummy data")
        gen_dummy_users()

    print("all done!")
