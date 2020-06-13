Responder app
=============

### MySQL
- sqlalchemy ... The Database Toolkit for Python
  - https://pypi.org/project/SQLAlchemy/
  - https://github.com/sqlalchemy/sqlalchemy
- mysql-connector-pyton ... MySQL Driver for Python
  - https://pypi.org/project/mysql-connector-python/
  - https://dev.mysql.com/doc/connector-python/en/
- Almebic ... a database migrations tool for SQLAlchemy
  - https://alembic.sqlalchemy.org/en/latest/
  - https://github.com/sqlalchemy/alembic
  - https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment

#### Timezone
- DB は UTC に設定
- Application 側で localtime (ないしクライアントのtimezone) に変換する


### Commands
```sh
# Install a package
$ docker-compose run --rm web pipenv install mysql-connector-python
or
$ docker run --rm web pipenv install mysql-connector-python
```

#### Alembic
```sh
$ docker-compose exec web pipenv run alembic -h
```


### Notes
#### Alembic
- Alembic を使用する準備
  - [Tutorial — Alembic 1\.4\.2 documentation](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

```sh
# db_migrations ディレクトリを migration ディレクトリとして初期化
# - "db_migrations" の部分は任意
$ docker-compose exec web pipenv run alembic init db_migrations
```

- alembic.ini ... 設定ファイル
  - 基本的に `sqlalchemy.url` だけを設定すればいいっぽい

