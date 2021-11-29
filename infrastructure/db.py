import pymysql
from flask_sqlalchemy import SQLAlchemy

from infrastructure.persistence.mapping.mapping import custom_metadata


class DbManager:
    DB = None

    @classmethod
    def start_db(cls, app):
        pymysql.install_as_MySQLdb()
        cls.DB = SQLAlchemy(app, metadata=custom_metadata)
        cls.DB.init_app(app)
        return cls.DB

    @classmethod
    def drop_db(cls, app):
        cls.DB = SQLAlchemy(app, metadata=custom_metadata)
        cls.DB.init_app(app)
        return cls.DB

