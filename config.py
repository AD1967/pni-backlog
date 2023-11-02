import os
basedir = os.path.abspath(os.path.dirname(__name__))

# данные для подключения
host = "10.1.6.74"
port = ":"+"3306"
db_name = "tci"
user = "dbuser"
password = "j0v461k"

#базовый класс конфигурации
class Config:
    #
    SECRET_KEY = os.getenv("SECRET_KEY") or "KEKW"
    #путь к json файлам для базы данных
    DATABASE_JSONS =    os.path.join(basedir, 'app', 'modules', 'db', 'jsons')
    #
    JSON_AS_ASCII = False

    @staticmethod
    def init_app(app):
        pass

#конфигурация для "разработки"
class DevConfig(Config):
    #путь к базе данных SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app', 'modules', 'db', 'local_db.db')
    DEBUG = True

class ProdConfig(Config):
    #путь к базе данных SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{user}:{password}@{host}{port}/{db_name}"
    pass

# выбор конфигурации
config = {
    'dev': DevConfig,
    'prod': ProdConfig,

    'default': DevConfig
}