from .. import main
from flask import request, jsonify
#from flask_login import login_required
from ...calculations.index import calc_index
from ...calculations.efficiency import calc_tec, calc_ctp, calc_eff, calc_eff_wnd, calc_eff_wnd_inf, calc_eff_doors, calc_eff_doors_inf, \
calc_eff_constructs, calc_eff_roof, calc_eff_hws_pipes, calc_eff_heat_pipes, calc_eff_people, calc_eff_hws_cranes, \
calc_eff_hws_showers, calc_eff_electro, calc_eff_vent, calc_eff_floor, printGCal, convertGCal
from .responses import default_json_response

# ТОКЕНЫ
from app.modules.blueprint.all_routes_settings import token_auth


@main.route("/calc_tec", methods=["POST"])
@token_auth.login_required
def api_calc_tec():
    print(request.json["id"])
    try:
        data = calc_tec(request.json["id"])
    except:
        data = None

    return default_json_response(not data is None, "error" if data is None else data)


@main.route("/calc_ctp", methods=["POST"])
@token_auth.login_required
def api_calc_ctp():
    print(request.json["id"])
    try:
        data = calc_ctp(request.json["id"])
    except:
        data = None

    return default_json_response(not data is None, "error" if data is None else data)


# вычисление индекса
@main.route("/calc_index", methods=["POST"])
@token_auth.login_required
def api_calc_index():
    print(request.json["id"])
    try:
        data = calc_index(request.json["id"])
    except:
        data = None
    
    return default_json_response(not data is None, "error" if data is None else data)
    
# вычисление эффективности
@main.route("/calc_efficiency", methods=["POST"])
@token_auth.login_required
def api_calc_eff():
    # id_build
    try:
        data = calc_eff(request.json["id"])
    except:
        data = None

    #data = calc_eff(request.json)
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