Responder Todo App
==================

![Python application](https://github.com/mitsu-ksgr/responder-todo-app/workflows/Python%20application/badge.svg)

Responder を使った TODO アプリの作成サンプル.

### Setup

```sh
# Run
$ docker-compose up -d

# Setup db
$ docker-compose exec web pipenv run alembic upgrade head
```

and, access http://localhost:8080/


### MySQL Connection Info (for dev)
- Database Type: `MySQL`
- Host: `localhost`
- Port: `33061`
- Database Name: `app`
- User Name: `dev_user`
- Password: `password`

```sh
# Access database
$ docker-compose exec db mysql --default-character-set=utf8mb4 -u root -proot_password
```

## References
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
- Application 側で localtime (ないしクライアントのtimezone) に変換する（予定）


## Command Notes
```sh
# Show logs
$ docker-compose logs -f

# Install a package
$ docker-compose run --rm web pipenv install mysql-connector-python
$ docker-compose run --rm web pipenv install --dev black
or
$ docker run --rm web pipenv install mysql-connector-python

# Run pytest
$ docker-compose run -e APP_ENV=test --rm web pipenv run pytest tests
```

### Alembic
```sh
$ docker-compose exec web pipenv run alembic -h

# Create migration file
$ docker-compose exec web pipenv run alembic revision -m "create users table"

# Running migrations
$ docker-compose exec web pipenv run alembic upgrade head

# Downgrades: downgrade just 1 step.
$ docker-compose exec web pipenv run alembic downgrade -1
```

### Linter
```sh
$ docker-compose exec web pipenv run flake8 app/*.py app/*/*.py
```

### Code formatting
```sh
$ docker-compose exec web pipenv run black app/*.py app/*/*.py
```

## Notes
#### Alembic
- Alembic を使用する準備
  - [Tutorial — Alembic 1\.4\.2 documentation](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

```sh
# db ディレクトリを migration ディレクトリとして初期化
# - "db" の部分は任意
$ docker-compose exec web pipenv run alembic init db
```

- alembic.ini ... 設定ファイル
  - 基本的に `sqlalchemy.url` だけを設定すればいいっぽい

