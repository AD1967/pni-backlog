from .. import main
#from flask_login import login_required
from ...db.common_gets import *
from ...db.old_requests import *
from .responses import default_json_response
from app.modules.blueprint.all_routes_settings import token_auth


#получение конфигураций зданий
@main.route("/buildings", methods=["GET"])
@token_auth.login_required
def api_buildings_all():
    data = get_buildings()
    return default_json_response(not data is None, "error" if data is None else data)

#получение тестовой конфигурации
@main.route("/buildings/test", methods=["GET"])
@token_auth.login_required
def api_buildings_test():
    data = get_test_build()
    return default_json_response(not data is None, "not found" if data is None else data)

#получение конфигруации здания по build_id
@main.route("/buildings/<int:build_id>", methods=["GET"])
@token_auth.login_required
def api_buildings(build_id):
    data = get_building(build_id)
    return default_json_response(not data is None, "not found" if data is None else data)

#получение данных из разных таблиц по типу (список)
@main.route("/elements/<string:type>", methods=["GET"])
@token_auth.login_required
def api_elements_all(type):
    data = get_elements(type)
    return default_json_response(not data is None, "error" if data is None else data)

#получение данных из разных таблиц по типу (по id)
@main.route("/elements/<string:type>/<int:id>", methods=["GET"])
@token_auth.login_required
def api_elements(type, id):
    data = get_element(type, id)
    return default_json_response(not data is None, "not found" if data is None else data)


#получение "полной" конфигруации здания по build_id
@main.route("/data/full/<int:build_id>", methods=["GET"])
@token_auth.login_required
def api_get_data_full(build_id):
    q_reheating = get_one_by_id_build(Q_reheating, build_id)
    reliability = get_one_by_id_build(Reliability, build_id)
    readings_vents = get_readings_vents(reliability.id_reliability)
    period = get_one_from_table(Period, q_reheating.id_period)

    readings_vents_values = []
    for r in readings_vents:
        readings_vents_values.append(r.value)
    build = reliability.build
    return default_json_response(
        True,
        {
            "id_build": build.id_build,

            "name": build.name,
            "floors": build.floors,
            "date_build": build.date_build.strftime('%Y-%m-%d'),
            "shut_off": reliability.id_shutoffvalve,
            "pipe_type": reliability.id_pipe,
            "radiator_type": reliability.id_radiator,
            "crane_type": reliability.id_crane,


            "len_a": build.len_a,
            "len_b": build.len_b,
            "len_sum": build.len_sum,
            "height": build.height,
            "doors": q_reheating.count_doors,
            "shkaf": q_reheating.count_shkaf,
            "divan": q_reheating.count_divan,
            "table": q_reheating.count_table,
            "shkafchik": q_reheating.count_shkafchik,

            "period":  period.name,
            "walls_material": q_reheating.walls_material,
            "floors_material": q_reheating.floors_materials,
            "doors_material": q_reheating.doors_material,
            "mebel_material": q_reheating.mebel_material,
            "divan_material": q_reheating.divan_material,
            "table_material": q_reheating.table_material,
            "shkafchik_material": q_reheating.shkafchik_material,



            "ihp" : reliability.ihp,
            "pump": reliability.id_pump,
            "heat_exchanger": reliability.id_heatexchanger,

            "vent_system": reliability.ventsys,
            "air_heaters_lines": readings_vents_values,

            "ascents_hws": reliability.ascents_hws,
            "descents_hws": reliability.descents_hws,
            "crane_count": reliability.count_crane,

            "ascents_heat": reliability.ascents_heat,
            "descents_heat": reliability.descents_heat,
            "radiator_count": reliability.count_radiator
        }
    )