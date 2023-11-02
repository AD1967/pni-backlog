from flask import current_app, g, abort
from . import main
# from . import login_manager
from  app.modules.User import UserLogin

# для токенов
from flask_httpauth import HTTPBasicAuth
from flask_httpauth import HTTPTokenAuth
from ..db.model import User

#действия пере началом запроса
@main.before_request
def before_request():
    pass

#действия после окончания запроса (даже с ошибкой)
#разрыв соединения с базой данных
@main.teardown_app_request
def close_db(err):
    pass


# ТОКЕНЫ
# Класс HTTPBasicAuth из Flask-HTTPAuth-это класс, реализующий основной поток проверки подлинности. 
# Две необходимые функции настраиваются с помощью декораторов verify_password и error_handler соответственно.

# Функция проверки получает имя пользователя и пароль, предоставленные клиентом, и возвращает True, 
# если учетные данные действительны, или False, если нет. 
# Для проверки пароля я используется метод check_password() класса UserLogin, 
# Я сохраняю аутентифицированного пользователя в g.user, так что я могу получить доступ к нему из функций представления API.
basic_auth = HTTPBasicAuth()
@basic_auth.verify_password
def verify_password(name, password):
    print(name,password)
    g.user = User.query.filter_by(name=name).first()
    print(g.user)
    if g.user is None:
        return False
    return UserLogin.check_password(g.user, password)

@basic_auth.error_handler
def basic_auth_error():
    abort(401)



# При использовании аутентификации по токенам Flask-HTTPAuth использует функцию verify_token, 
# но кроме этого аутентификация токена работает так же, как и базовая аутентификация. 
# Функция проверки токена использует UserLogin.check_token(), чтобы найти пользователя, которому принадлежит предоставленный токен. 
# Функция также обрабатывает случай отсутствующего токена, установив текущего пользователя в None. 
# Возвращаемое значение True или False определяет, может ли Flask-HTTPAuth разрешить выполнение функции просмотра или нет.
token_auth = HTTPTokenAuth()
@token_auth.verify_token
def verify_token(token):
    print("Проверка токена:")

    # #временно
    # print("Временно отключена")
    # g.current_user = User.query.filter_by(id_user = 0).first()

    print(token)
    g.current_user = UserLogin.check_token(token) if token else None
    return g.current_user is not None

@token_auth.error_handler
def token_auth_error():
    abort(401)