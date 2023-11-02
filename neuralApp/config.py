import os

BASE_DIR = os.path.abspath(os.path.dirname(__name__))
print("BASE_DIR:", BASE_DIR)

UPLOAD_FOLDER = "app/static/files"
print("UPLOAD_FOLDER:", UPLOAD_FOLDER)
#ALLOWED_EXTENSIONS = {'txt', 'csv', 'xls', 'xlsx', 'pkl'}
ALLOWED_EXTENSIONS = {'xlsx'}
print("ALLOWED_EXTENSIONS:", ALLOWED_EXTENSIONS)
HIDDEN_LAYER_OPTIONS = ["Dense"]
print("HIDDEN_LAYER_OPTIONS:", HIDDEN_LAYER_OPTIONS)
ACTIVATION_OPTIONS = ["relu", "linear", "sigmoid", "tanh", "leakyrelu"]
print("ACTIVATION_OPTIONS:", ACTIVATION_OPTIONS)
COLUMNS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", 
"Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN", "AO", "AP", "AQ", "AR", "AS", "AT", "AU", 
"AV", "AW", "AX", "AY", "AZ"]
print("COLUMNS:", COLUMNS)
PATH_TO_UPLOAD = os.path.join(BASE_DIR, UPLOAD_FOLDER)
print("PATH_TO_UPLOAD:", PATH_TO_UPLOAD)

# Connection data
HOST = "10.1.6.74"
PORT = ":" + "3306"
DB_NAME = "tci"
USER = "dbuser"
PASSWORD = "j0v461k"

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or "IDK"
    print("SECRET_KEY:", SECRET_KEY)

    #путь к json файлам для базы данных
    #DATABASE_JSONS = os.path.join(basedir, 'app', 'modules', 'db', 'jsons')
    #JSON_AS_ASCII = False

    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #UPLOAD_FOLDER = 'static/files'

    @staticmethod
    def init_app(app):
        pass

# Development Configuration
class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, "instance", 'test.sqlite3')
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app', 'modules', 'db', 'local_db.db')
    print("SQLALCHEMY_DATABASE_URI:", SQLALCHEMY_DATABASE_URI)
    DEBUG = True

# Production Configuration
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}{PORT}/{DB_NAME}"
    print("SQLALCHEMY_DATABASE_URI:", SQLALCHEMY_DATABASE_URI)
    pass

# Choose configuration
config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': DevConfig
}