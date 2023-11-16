from .. import main
from flask import g, request
from ...db.common_gets import *
from ...db.common_puts import *
from .responses import default_json_response
from ...calculations.efficiency import *
# ТОКЕНЫ
from app.modules.blueprint.all_routes_settings import token_auth


# аргументы в query string
#получение конфигураций зданий с заданными полями (пустая строка == все имеющиеся)
@main.route("/data/builds", methods=["GET"])
@token_auth.login_required
def api_data_builds():
    data = get_build(request.args)
    return default_json_response(not data is None, "error" if data is None else data)

# аргументы в query string
#получение конфигруации здания по build_id с заданными полями  (пустая строка == все имеющиеся)
@main.route("/data/build/<int:build_id>", methods=["GET"])
@token_auth.login_required
def api_data_build_by_id(build_id):
    data = get_build( request.args, build_id)
    return default_json_response(not data is None, "error" if data is None else data[0])


# аргументы в query string
#получение тестовой конфигурации
@main.route("/data/build/test", methods=["GET"])
@token_auth.login_required
def api_data_build_test():
    admin =  User.query.filter_by(name="admin").first()
    build = Build.query.filter_by(id_user=admin.id_user, name="Тестовая схема здания").first()
    data = get_build(request.args, build.id_build)
    return default_json_response(not data is None, "error" if data is None else data[0])


# аргументы в query string
#получение конфигураций зданий с заданными полями (пустая строка == все имеющиеся)
@main.route("/data/elements/<string:type>", methods=["GET"])
@token_auth.login_required
def api_data_elements(type):
    data = get_element(type, request.args)
    return default_json_response(not data is None, "error" if data is None else data)

# аргументы в query string
#получение конфигураций зданий с заданными полями (пустая строка == все имеющиеся)
@main.route("/data/element/<string:type>/<int:id>", methods=["GET"])
@token_auth.login_required
def api_data_element(type, id):
    data = get_element(type,request.args,  id)
    return default_json_response(not data is None, "error" if data is None else data[0])


# push metods

#добавление конфигруации здания
@main.route("/data/build", methods=["PUT"])
@token_auth.login_required
def api_data_add_build():
    data = add_build(request.json)
    return default_json_response(not data is None, "error" if data is None else data)


#добавление записи в таблицу по типу
@main.route("/data/element/<string:type>", methods=["PUT"])
@token_auth.login_required
def api_data_add_elem(type):
    data = add_elem(type, request.json)
    return default_json_response(not data is None, "error" if data is None else data)

#получение данных из полей 
@main.route("/data/cur_build", methods=["PUT"])
@token_auth.login_required
def update_iformation():
    print(request.json)
    data = update_cur_info(request.json)
    return default_json_response(not data is None, "error" if data is None else data)
