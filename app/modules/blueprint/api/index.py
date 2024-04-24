from .. import main
from flask import request, jsonify, send_file
#from flask_login import login_required
from ...calculations.index import calc_index
from ...calculations.efficiency import save, calc_tec, calc_ctp, calc_add_heatcosts, calc_eff, calc_eff_wnd, calc_eff_wnd_inf, calc_eff_doors, calc_eff_doors_inf, \
calc_eff_constructs, calc_eff_roof, calc_eff_hws_pipes, calc_eff_heat_pipes, calc_eff_people, calc_eff_hws_cranes, \
calc_eff_hws_showers, calc_eff_electro, calc_eff_vent, calc_eff_floor, printGCal, convertGCal
from .responses import default_json_response

# ТОКЕНЫ
from app.modules.blueprint.all_routes_settings import token_auth


# Расчёт ТЭЦ
@main.route("/calc_tec", methods=["POST"])
@token_auth.login_required
def api_calc_tec():
    print(request.json["id"])
    try:
        data = calc_tec(request.json["id"])
    except:
        data = None
    print('tec ', data)
    return default_json_response(not data is None, "error" if data is None else data)


# Расчёт ЦТП
@main.route("/calc_ctp", methods=["POST"])
@token_auth.login_required
def api_calc_cpt():
    print(request.json["id"])
    try:
        data = calc_ctp(request.json["id"])
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
        data = calc_index(request.json.get('parametrs_of_reliability'))
    except:
        data = None
    print('Надёжность = ', data)
    return default_json_response(not data is None, "error" if data is None else data)


# вычисление эффективности
@main.route("/calc_efficiency", methods=["POST"])
@token_auth.login_required
def api_calc_eff():
    # id_build
    try:
        data = calc_eff()
    except:
        data = None

    print('efficiency ', data)
    return default_json_response(not data is None, "error" if data is None else data)


# вычисление эффективности (доп затрат на прогрев)
@main.route("/calc_efficiency_add_heatcosts", methods=["POST"])
@token_auth.login_required
def api_calc_eff_add_heatcosts():
    # id_build
    try:
        data = calc_add_heatcosts(request.json["id"])
    except:
        data = None

    return default_json_response(not data is None, "error" if data is None else data)

# вычисление эффективности (окна)
@main.route("/calc_efficiency_wnd", methods=["POST"])
@token_auth.login_required
def api_calc_eff_wnd():
    # id_build
    try:
        data = printGCal(calc_eff_wnd(request.json["id"]))
    except:
        data = None
    
    #data = calc_eff_wnd(request.json)
    return default_json_response(not data is None, "error" if data is None else data)
    
# вычисление эффективности (инф окна)
@main.route("/calc_efficiency_wnd_inf", methods=["POST"])
@token_auth.login_required
def api_calc_eff_wnd_inf():
    # id_build
    try:
        data = printGCal(calc_eff_wnd_inf(request.json["id"]))
    except:
        data = None
    
    #data = calc_eff_wnd(request.json) - calc_eff_wnd_inf(request.json)
    return default_json_response(not data is None, "error" if data is None else data)

# вычисление эффективности (двери)
@main.route("/calc_efficiency_doors", methods=["POST"])
@token_auth.login_required
def api_calc_eff_doors():
    # id_build
    try:
        data = printGCal(calc_eff_doors(request.json["id"]))
    except:
        data = None
    
    #data = calc_eff_doors(request.json)
    return default_json_response(not data is None, "error" if data is None else data)
    
# вычисление эффективности (инф двери)
@main.route("/calc_efficiency_doors_inf", methods=["POST"])
@token_auth.login_required
def api_calc_eff_doors_inf():
    # id_build
    try:
        data = printGCal(calc_eff_doors_inf(request.json["id"]))
    except:
        data = None
    
    #data = calc_eff_doors(request.json) - calc_eff_doors_inf(request.json)
    return default_json_response(not data is None, "error" if data is None else data)


# вычисление эффективности (ограждающие конструкции)
@main.route("/calc_efficiency_constructs", methods=["POST"])
@token_auth.login_required
def api_calc_eff_constructs():
    # id_build
    try:
        data = printGCal(calc_eff_constructs(request.json["id"]))
    except:
        data = None
    
    #data = calc_eff_constructs(request.json)
    return default_json_response(not data is None, "error" if data is None else data)

# вычисление эффективности (крыша)
@main.route("/calc_efficiency_roof", methods=["POST"])
@token_auth.login_required
def api_calc_eff_roof():
    # id_build
    try:
        data = printGCal(calc_eff_roof(request.json["id"]))
    except:
        data = None
    
    #data = calc_eff_roof(request.json)
    return default_json_response(not data is None, "error" if data is None else data)

# вычисление эффективности (теплоприток ГВС)
@main.route("/calc_efficiency_hws_pipes", methods=["POST"])
@token_auth.login_required
def api_calc_eff_hws_pipes():
    # id_build
    try:
        data = printGCal(calc_eff_hws_pipes(request.json["id"]))
    except:
        data = None
    
    #data = calc_eff_hws_pipes(request.json)
    return default_json_response(not data is None, "error" if data is None else data)

# вычисление эффективности (теплоприток отопление)
@main.route("/calc_efficiency_heat_pipes", methods=["POST"])
@token_auth.login_required
def api_calc_eff_heat_pipes():
    # id_build
    try:
        data = printGCal(calc_eff_heat_pipes(request.json["id"]))
    except:
        data = None
    
    #data = calc_eff_heat_pipes(request.json)
    return default_json_response(not data is None, "error" if data is None else data)

# вычисление эффективности (теплоприток от людей)
@main.route("/calc_efficiency_people", methods=["POST"])
@token_auth.login_required
def api_calc_eff_people():
    # id_build
    try:
        data = printGCal(calc_eff_people(request.json["id"]))
    except:
        data = None
    
    #data = calc_eff_people(request.json)
    return default_json_response(not data is None, "error" if data is None else data)

# вычисление эффективности (рукомойники)
@main.route("/calc_efficiency_hws_cranes", methods=["POST"])
@token_auth.login_required
def api_calc_eff_hws_cranes():
    # id_build
    try:
        data = printGCal(calc_eff_hws_cranes(request.json["id"]))
    except:
        data = None
    
    #data = calc_eff_hws_cranes(request.json)
    return default_json_response(not data is None, "error" if data is None else data)

# вычисление эффективности (душевые)
@main.route("/calc_efficiency_hws_showers", methods=["POST"])
@token_auth.login_required
def api_calc_eff_hws_showers():
    # id_build
    try:
        data = printGCal(calc_eff_hws_showers(request.json["id"]))
    except:
        data = None
    
    #data = calc_eff_hws_showers(request.json)
    return default_json_response(not data is None, "error" if data is None else data)

# вычисление эффективности (теплоприток электроосвещенияе)
@main.route("/calc_efficiency_electro", methods=["POST"])
@token_auth.login_required
def api_calc_eff_electro():
    # id_build
    try:
        data = printGCal(calc_eff_electro(request.json["id"]))
    except:
        data = None
    
    #data = calc_eff_electro(request.json)
    return default_json_response(not data is None, "error" if data is None else data)

# вычисление эффективности (вентиляция)
@main.route("/calc_efficiency_vent", methods=["POST"])
@token_auth.login_required
def api_calc_eff_vent():
    # id_build
    try:
        data = printGCal(calc_eff_vent(request.json["id"]))
    except:
        data = None

    #data = calc_eff_vent(request.json)
    return default_json_response(not data is None, "error" if data is None else data)

# вычисление эффективности (пол)
@main.route("/calc_efficiency_floor", methods=["POST"])
@token_auth.login_required
def api_calc_eff_floor():
    # id_build
    try:
        data = printGCal(calc_eff_floor(request.json["id"]))
    except:
        data = None
    
    #data = calc_eff_floor(request.json)
    return default_json_response(not data is None, "error" if data is None else data)
