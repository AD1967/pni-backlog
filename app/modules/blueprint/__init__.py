from flask import Blueprint
#from flask_login import LoginManager
from ..imports import import_submodules

#главный Blueprint
main = Blueprint('main', __name__)

# login_manager = LoginManager()
# login_manager.login_view = 'main.api_enter'  # Если пользователь выходит (или заходит на страницу, к которой закрыт доступ), 
#                                     #то он будет перенаправлен на страницу /enter

# предотвращение завистимостей от main, импорт всех подмодулей
import_submodules(__name__)