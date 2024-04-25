from .. import main
from flask import request, jsonify, send_file
#from flask_login import login_required
from ...calculations.index import calc_index
from ...calculations.efficiency import save, calc_tec, calc_ctp, calc_eff, set_count_of_point
from .responses import default_json_response

# ТОКЕНЫ
from app.modules.blueprint.all_routes_settings import token_auth


# Расчёт ТЭЦ
@main.route("/calc_tec", methods=["POST"])
@token_auth.login_required
def api_calc_tec():
    try:
        data = calc_tec(request.json["cur_date"])
    except:
        data = None
    # print('tec ', data)
    return default_json_response(not data is None, "error" if data is None else data)


# Расчёт ЦТП
@main.route("/calc_ctp", methods=["POST"])
@token_auth.login_required
def api_calc_cpt():
    try:
        data = calc_ctp(request.json["cur_date"])
    except:
        data = None

    return default_json_response(not data is None, "error" if data is None else data)


# Скачивание эксель с текущими расчётами
@main.route("/save_cur", methods=["POST"])
@token_auth.login_required
def api_save_cur():
    print('Создается excel таблица..')
    res_excel = 'cur_results.xlsx'
    parametrs_of_build = request.json.get('parametrs_of_build')
    results = request.json.get('results')
    dop_results = request.json.get('dop_results')
    # build = [param.get(key) for param in parametrs_of_build for key in param]
    build = list(parametrs_of_build.values())
    # res = [item['val'] for item in results]
    res = list(results.values())
    # dop = [item['val'] for item in dop_results]
    dop = list(dop_results.values())
    data = res[2:17] + dop[:3] + dop[4:6] + res[17:] + dop[3:4] + dop[6:]
    save(build, data)

    print('Данные успешно сохранены в файл ', res_excel)
    return send_file(res_excel, as_attachment=True, download_name='current_results.xlsx')


# вычисление индекса
@main.route("/calc_index", methods=["POST"])
@token_auth.login_required
def api_calc_index():
    print(request.json.get('parametrs_of_reliability'))
    try:
        data = set_count_of_point(calc_index(request.json.get('parametrs_of_reliability')))
    except:
        data = None
    # print('Надёжность = ', data)
    return default_json_response(not data is None, "error" if data is None else data)


# вычисление эффективности
@main.route("/calc_efficiency", methods=["POST"])
@token_auth.login_required
def api_calc_eff():
    try:
        data = calc_eff(request.json["cur_date"])
    except:
        data = None

    # print('efficiency ', data)
    return default_json_response(not data is None, "error" if data is None else data)
