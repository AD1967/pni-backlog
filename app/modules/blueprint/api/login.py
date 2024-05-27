from .. import main
from flask import request, jsonify, g
from ...db.login_requests import *
#from flask_login import login_user, login_required, logout_user, current_user
###
from werkzeug.security import generate_password_hash, check_password_hash
from  ...User import UserLogin

#ТОКЕНЫ
#from app.modules.blueprint.all_routes_settings import basic_auth
from app.modules.db import db 
from app.modules.blueprint.all_routes_settings import token_auth
from app.modules.blueprint.all_routes_settings import basic_auth

# выход
@main.route("/logout", methods=['POST'])
def api_logout():
    try:
        tok = request.json['token']
        user = UserLogin.check_token(tok) if tok else None
        user.token_expiration = datetime.utcnow() - timedelta(seconds=1)
        db.session.commit()
        print(user.token_expiration)
    except:
        user = None
    finally:
        if not user is None:
            print("Выход из аккаунта выполнен")
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "error" : ""})

# регистрация
@main.route("/registration", methods=['POST'])
def api_registration():
    # Простенькая проверка логинов и паролей при регистрации
    if len(request.json['name']) > 4 \
        and len(request.json['psw']) > 4 and request.json['psw'] == (request.json['psw2']):
        hash = generate_password_hash(request.json['psw'], method = 'pbkdf2')
        res = addUser(request.json['name'], hash)
        if res:
            print("Вы успешно зарегистрировались")
            return jsonify({"success": True, "result": '/enter'})
        else:
            print("Некорректные данные при регистрации", "error")
            return jsonify({"success": False, "error" : "", "result": '/registration'})
    return jsonify({"success": False, "error" : "", "result": '/registration'})



# ТОКЕНЫ
@main.route("/tokens", methods=['POST'])
@basic_auth.login_required
def get_token():
    token = UserLogin.get_token(g.user)
    return jsonify({"success": True, "result": token})


@main.route("/check_token_for_server", methods=['POST']) # GET
#@basic_auth.login_required
def token_for_server():
    token = UserLogin.check_token(request.json['token'])
    if token:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})