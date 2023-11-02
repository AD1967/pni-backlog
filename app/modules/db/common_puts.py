from lib2to3.pytree import convert
from flask_sqlalchemy import SQLAlchemy
from app.modules.calculations.efficiency import Q_floor_
from app.modules.db.model import DbPutError
from ..db.model import *
import itertools
from flask import g
from datetime import date, datetime
from app.modules.db.model import DbPutError
from .common_gets import element_to_id_klass, element_to_klass

def check_map(map1, map2):
    for el in map1.keys():
        if not el in map2.keys():
            print(f"Отсутствует обязательное поле")
            raise DbPutError(f"Ошибка получения конфигурации: отсутствует обязательное поле")
        else:
            map1[el] = map2[el]

def check_optional_map(map1, map2):
    for el in map1.keys():
        if el in map2.keys():
            map1[el] = map2[el]

# проверка обязательных айдишников
def check_main_id(list_main_id, data):
    for el in list_main_id:
        if not el in data.keys():
            raise DbPutError(f"Ошибка получения конфигурации: отсутствует обязательный айдишник - {el}")

# Удаление старой конфигурации по названию
def del_config(name):
    res_map = {}
    res_list = []
    build_id_for_del = name.id_build
    db.session.delete(name)
    q_floor_del = Q_floor.query.filter_by(id_build=build_id_for_del).first()
    if q_floor_del:
        db.session.delete(q_floor_del)
        q_floor_id = q_floor_del.id_q_floor
        res_list.append(q_floor_id)
        res_map["q_floor_id"] = q_floor_id
    q_people_del = Q_person.query.filter_by(id_build=build_id_for_del).first()
    if q_people_del:
        db.session.delete(q_people_del)
        q_people_id = q_people_del.id_q_peoples
        res_list.append(q_people_id)
        res_map["q_people_id"] = q_people_id
    q_doors_del = Q_door.query.filter_by(id_build=build_id_for_del).first()
    if q_doors_del:
        db.session.delete(q_doors_del)
        q_doors_id = q_doors_del.id_q_doors
        res_list.append(q_doors_id)
        res_map["q_doors_id"] = q_doors_id
    q_wnd_del = Q_wnd.query.filter_by(id_build=build_id_for_del).first()
    if q_wnd_del:
        db.session.delete(q_wnd_del)
        q_wnd_id = q_wnd_del.id_q_wnd
        res_list.append(q_wnd_id)
        res_map["q_wnd_id"] = q_wnd_id
    reliability_del = Reliability.query.filter_by(id_build=build_id_for_del).first()
    if reliability_del:
        db.session.delete(reliability_del)
        q_reliability_id = reliability_del.id_reliability
        res_list.append(q_reliability_id)
        res_map["q_reliability_id"] = q_reliability_id
    
        readings_vents_del = Readings_vent.query.filter_by(id_reliability=reliability_del.id_reliability).all()
        q_vents_id_list = []
        if readings_vents_del:
            for el in readings_vents_del:
                db.session.delete(el)
                q_vents_id_list.append(el.id_reading)
            res_list.append(q_vents_id_list)
            res_map["q_vents_id_list"] = q_vents_id_list
    q_reheating_del = Q_reheating.query.filter_by(id_build=build_id_for_del).first()
    if q_reheating_del:
        db.session.delete(q_reheating_del)
        q_reheating_id = q_reheating_del.id_q_reheat
        res_list.append(q_reheating_id)
        res_map["q_reheating_id"] = q_reheating_id
    q_construct_roof_del = Q_construct_roof.query.filter_by(id_build=build_id_for_del).first()
    if q_construct_roof_del:
        db.session.delete(q_construct_roof_del)
        q_construct_roof_id = q_construct_roof_del.id_q_construct_roof
        res_list.append(q_construct_roof_id)
        res_map["q_construct_roof_id"] = q_construct_roof_id
    q_elec_del = Q_elec.query.filter_by(id_build=build_id_for_del).first()
    if q_elec_del:
        db.session.delete(q_elec_del)
        q_elec_id = q_elec_del.id_q_elec
        res_list.append(q_elec_id)
        res_map["q_elec_id"] = q_elec_id

    print(res_map)
    print("end of delete")
    
    return res_map


# def check_element(el, data, result):
#     if el["id"]:
#         is_in = el["klass"].query.filter_by(**{el['name']:data[el['name']]}).first()
#         if is_in:
#             result[el["name"]] = data[el["name"]]
#         else:
#             raise DbPutError(f"Ошибка получения конфигурации: отсутствует айдишник - {el['name']}")
#     else:
#         result[el["name"]] = data[el["name"]]

    # if not el["opt"] and el["id"]:      # Проверка обязательного айдишника
    #     # if not el["name"] in data.keys():
    #     #     raise DbPutError(f"Ошибка получения конфигурации: отсутствует обязательный айдишник - {el['name']}")
    #     # else:
    #         result[el["name"]] = data[el["name"]]

    # if el["opt"] and el["id"]:      # проверка необязательного айдишника
    #     # if el["name"] in data.keys():
    #         # klass = element_to_klass(el["klass"])   # ???
    #         is_in = klass.query.filter_by(**{el['name']:data[el['name']]}).first()
    #         if is_in:
    #             result[el["name"]] = data[el["name"]]

    # if not el["opt"] and not el["id"]:      # проверка обязательного поля
    #     # if not el["name"] in data.keys():
    #     #     print(f"Отсутствует обязательное поле")
    #     #     raise DbPutError(f"Ошибка получения конфигурации: отсутствует обязательное поле - {el['name']}")
    #     # else:
    #         result[el["name"]] = data[el["name"]]
    
    # if el["opt"] and not el["id"]:      # проверка необязательных полей
    #     # if el["name"] in data.keys():
    #         result[el["name"]] = data[el["name"]]
    
    

# class My_el:
#     def __init__(self, key, opt, id, klass):
#         self.map_el = {"name": key, "opt": opt, "id": id, "klass": klass}
def My_el( key, opt, id, klass, override_id = None):
     return {"name": key, "opt": opt, "id": id, "klass": klass,  "override_id": override_id}


def put_help(list_of_maps, data, build_id):
    count = 0
    flag = False
    result = {}
    for el in list_of_maps:
        if el["name"] in data.keys():
            count = count + 1
            if el["id"]:
                if not el[ "override_id"] is None:
                    id_name = el["override_id"]
                else:
                    id_name = el['name']
                #print({id_name:data[el['name']]}, el)
                if not el["klass"].query.filter_by(**{id_name:data[el['name']]}).first() is None:
                    result[el["name"]] = data[el["name"]]
                else:
                    print(result)
                    raise DbPutError(f"Ошибка получения конфигурации: отсутствует айдишник - "+el['name'])
            else:
                if(el['name'] == "q_doors_count_doors"): result["count_doors"] = data[el["name"]]
                else: result[el["name"]] = data[el["name"]]
        elif not el["opt"]:
            flag = True
            print( el["name"])
            if count != 0:
                print(result)
                raise DbPutError(f"Ошибка получения конфигурации: отсутствует обязательное поле - {el['name']}")
    
    if flag and count != 0:
        print(result)
        raise DbPutError(f"Ошибка получения конфигурации: присутсвуют не все обязательные поля")
    if count != 0:
        result["id_build"] = build_id
        print("comp:",count, len(result)-1)
    return count, result

def create_maps(main_fields, opt_fields, main_id = [], opt_id = []):
    result = []
    for el in main_fields:
        result.append(My_el(el, False, False, None))
    for el in opt_fields:
        result.append(My_el(el, True, False, None))
    for el in main_id:
        if(len(el) == 3):
            id = el[2]
        else:
            id = None
        result.append(My_el(el[0], False, True, el[1], id))
    for el in opt_id:
        if(len(el) == 3):
            id = el[2]
        else:
            id = None
        result.append(My_el(el[0], True, True, el[1], id))

    return result

add_Data = [
    {"klass": Q_floor, "id": ["id_q_floor", "q_floor_id"], "main_fields" : ["height_floor"]},
    {"klass": Q_person, "id": ["id_q_peoples", "q_people_id"], "main_fields" : ["mens", "womens", "time_average"]},
    {"klass": Q_door, "id": ["id_q_doors", "q_doors_id"], "main_fields" : ["q_doors_count_doors", "length_door", "height_door", "date_doors"],
      "main_id": [["id_door",Door]]
    },
    {"klass": Q_wnd, "id":["id_q_wnd", "q_wnd_id"], "main_fields" :["count_windows", "length_wnd", "height_wnd", "date_wnd"], 
        "main_id": [["id_window", Window]]
    },
    {"klass": Reliability, "id":["id_reliability", "q_reliability_id"], "opt_fields" : [ "ventsys", "ihp", "ascents_hws", "descents_hws", "count_crane", "ascents_heat", "descents_heat", "count_radiator"], 
        "main_id": [["id_pipe", Pipe], ["id_radiator", Radiator], ["id_crane", Crane], ["id_shutoffvalve", Shutoffvalve]],
        "opt_id": [["id_pump", Pump], ["id_heatexchanger", Heatexchanger]]
    },
    {"klass": Q_reheating, "id":["id_q_reheat", "q_reheating_id"], "main_fields":  ["count_doors", "count_shkaf", "count_divan", "count_table",
             "count_shkafchik"],
        "main_id" :  [["walls_material",Material, "id_material"], ["floors_materials",Material, "id_material"],
            ["doors_material",Material, "id_material"], ["mebel_material",Material, "id_material"], ["divan_material",Material, "id_material"],
            ["table_material",Material, "id_material"], ["shkafchik_material",Material, "id_material"]],
        "opt_id": [["id_period",Period]]
    },
    {"klass": Q_construct_roof, "id":["id_q_construct_roof","q_construct_roof_id"], "main_id" :[["constructs_energoeff",Energoeff, "id_energoeff"]],
        "opt_id": [["roof_energoeff",Energoeff, "id_energoeff"]]
    },
    {"klass": Q_elec, "id":["id_q_elec","q_elec_id"], "opt_fields" : ["elec_consumption_by_period"]},
]

# добавляет конфигурацию в таблицу
def add_build(data):
    result = None
    is_build = None
    try:
        # ТАБЛИЧКА build
        build = {"name" : "", "floors" : "", "len_a" : "", "len_b" : "", "len_sum" : "", "height" : "", "date_build" : "", "temp_inside": "", "temp_outside": ""}
        check_map(build, data)
        build['date_build'] = datetime.fromisoformat(build['date_build'])
        print("Пройдена проверка обязательных полей build")
        name_ = Build.query.filter_by(name=data['name']).first()
        if name_:   # Если такое название конфигурации уже есть в бд
            print("Такое название конфигурации уже есть")
            # Удалить все таблицы связанные с этой конфигурацией и обновить эти таблицы новыми данными
            map_of_id = del_config(name_)
            print(map_of_id)
            build["id_user"] = g.current_user.id_user
            print("User id:")
            print(build["id_user"])
            is_build = name_.id_build
            build["id_build"] = is_build
            db.session.add(Build(build))
            print("Табличка build Заменена в бд (db.session.add)")
            db.session.flush()
            print("Табличка build заменена в бд (db.session.flush)")          
            print("Id build:")
            print(is_build)
            # не забыть удалить если ошибка дальше
        else:   # Если такого названия конфигурации еще не было в бд
            build["id_user"] = g.current_user.id_user
            print("User id:")
            print(build["id_user"])
            db.session.add(Build(build))
            print("Табличка build добавлена в бд (db.session.add)")
            db.session.flush()
            print("Табличка build добавлена в бд (db.session.flush)")
            name_build = Build.query.filter_by(name=data['name']).first()
            is_build = name_build.id_build
            print("Id build:")
            print(is_build)
            # не забыть удалить если ошибка дальше
        
        data2 = build
        if "id_build" in data2:
            del data2["id_build"]
        if "id_user" in data2:
            del data2["id_user"]

        count_all = len(build) - 2

        for table_data in add_Data:
            lst = create_maps(
                table_data["main_fields"]  if "main_fields" in table_data else [],
                table_data["opt_fields"]  if "opt_fields" in table_data else [] ,
                table_data["main_id"]  if "main_id" in table_data else [] ,
                table_data["opt_id"]  if "opt_id" in table_data else []
            )
            count, result = put_help(lst, data, is_build)
            if len(result) != 0:
                if name_ and count != 0:
                    if table_data["id"][1] in map_of_id:
                        result[table_data["id"][0]] = map_of_id[table_data["id"][1]]
                if 'date_doors' in result:
                    result['date_doors'] = datetime.fromisoformat(result['date_doors'])
                if 'date_wnd' in result:
                    result['date_wnd'] = datetime.fromisoformat(result['date_wnd'])
                
                if table_data["klass"] == Reliability:
                    flag = True
                    if not "ventsys" in result:
                        if "readings_vents" in data.keys():
                            print(f"Присутствуют readings_vents, хотя не должны!")
                            raise DbPutError(f"Присутствуют readings_vents, хотя не должны!")
                        else:
                            flag = False
                    else:
                        if int(result["ventsys"]) == 1:
                            if not "readings_vents" in data.keys():
                                print(f"Отсутвуют readings_vents, хотя не должны!")
                                raise DbPutError(f"Отсутвуют readings_vents, хотя не присутствует ventsys!")
                        else:
                            flag = False
                        
                    print(f"table_data: {Reliability}, {result}")
                    data2.update(result)
                    if count != 0:
                        del data2["id_build"]
                        if name_:
                            if table_data["id"][1] in map_of_id:
                                del data2[table_data["id"][0]]
                    db.session.add(Reliability(result))
                    db.session.flush()
                    temp = Reliability.query.filter_by(id_build=result["id_build"]).first()
                    is_reliability = temp.id_reliability
                    print("Id reability:")
                    print(is_reliability)
                            # ТАБЛИЧКИ для readings_vent
                    if flag:
                        for i, el in enumerate(data['readings_vents']):
                            readings_vent = {"value" : el}
                            #check_map(readings_vent, el)
                            readings_vent["id_reliability"] = is_reliability
                            # if name_:
                            #     if"q_vents_id_list" in map_of_id:
                            #         readings_vent["id_reading"] = map_of_id["q_vents_id_list"][i]
                            db.session.add(Readings_vent(readings_vent))
                        count_all = count_all + 1
                        data2["readings_vents"] = data['readings_vents']
                        print(data['readings_vents'])
                        print(data2['readings_vents'])
                        print("Таблички readings_vents добавлены в бд")
                else:
                    print(f"table_data: {table_data['klass']}, {result}")
                    data2.update(result)
                    if count != 0:
                        del data2["id_build"]
                        if name_ and count != 0:
                            if table_data["id"][1] in map_of_id:
                                del data2[table_data["id"][0]]
                    if table_data["klass"] == Q_door:
                        data2["q_doors_count_doors"] = result["count_doors"]
                        del data2["count_doors"]
                    db.session.add(table_data["klass"](result))
                print(f"succ: {table_data['klass']}")
                count_all += count

        print(count_all, len(data), len(data2))
        if len(data2) != len(data):
            print(data)
            print(data2)
            for name in data2.keys():
                if name != "q_doors_count_doors":
                    print(f"{data[name]},{data2[name]} ")
            raise DbPutError(f"Ошибка получения конфигурации: лишние данные")

        db.session.commit() #только когда пройдут все проверки
        result = {"id_build": is_build}

    except Exception as e:
        db.session.rollback()
        result = None
        print(f"put_build error")
        print(e)
    return result


put_element_elements = [
    "convector", "period", "volume", "airheater", "tempcontroller", "energoeff", "shutoffvalve",
    "heatexchanger", "pump", "crane", "radiator", "pipe", "material", "doors", "window"
]

def check_elem(type, data, main_fields, optional_fields = {}):
    klass = element_to_klass(type)
    check_map(main_fields, data)
    print("Успешная проверка обязательных полей")
    check_optional_map(optional_fields, data)
    print("Успешная проверка необязательных полей")
    main_fields.update(optional_fields)
    print("Успешное объединение обязательных и необязательных полей")
    print(main_fields)
    if len(main_fields) < len(data):
        raise DbPutError(f"Ошибка получения данных: данных больше, чем требуется")
    name_ = klass.query.filter_by(name=data['name']).first()
    if name_:
        print(f"Такой {type} уже есть")
        # Удаляем все данные связанные с этим название и заполняем новыми
        old_id = getattr(name_, f"id_{type}")
        db.session.delete(name_)
        main_fields[f"id_{type}"] = old_id
    db.session.add(klass(main_fields))
    print(f"Успешное добавление нового {type} в бд")

# Добавление новых записей в таблицы, которые не связаны по id_build
def add_elem(type, data):
    result = None
    try:
        if type in put_element_elements:
            if type == "convector":
                main_fields = {"name": "", "lambd": ""}
                optional_fields = {"power": ""}
                check_elem(type, data, main_fields, optional_fields)
        
            elif type == "period":
                main_fields = {"name": "", "T": ""}
                check_elem(type, data, main_fields)
            
            elif type == "volume":
                main_fields = {"name": "", "value": ""}
                check_elem(type, data, main_fields)

            elif type == "airheater":
                main_fields = {"name": "", "lambd": ""}
                check_elem(type, data, main_fields)

            elif type == "tempcontroller":
                main_fields = {"name": "", "lambd": ""}
                check_elem(type, data, main_fields)

            elif type == "energoeff":
                main_fields = {"name": "", "R": ""}
                check_elem(type, data, main_fields)

            elif type == "shutoffvalve":
                main_fields = {"name": "", "lambd": ""}
                optional_fields = {"diam": ""}
                check_elem(type, data, main_fields, optional_fields)

            elif type == "heatexchanger":
                main_fields = {"name": "", "lambd": ""}
                optional_fields = {"temp_min": "", "temp_max": "", "consumption": "", "power": "", "p_max": ""}
                check_elem(type, data, main_fields, optional_fields)

            elif type == "pump":
                main_fields = {"name": "", "lambd": ""}
                optional_fields = {"power": ""}
                check_elem(type, data, main_fields, optional_fields)

            elif type == "crane":
                main_fields = {"name": "", "lambd": ""}
                check_elem(type, data, main_fields)
            
            elif type == "radiator":
                main_fields = {"name": "", "lambd": ""}
                optional_fields = {"power_section": "", "count_section": ""}
                check_elem(type, data, main_fields, optional_fields)

            elif type == "pipe":
                main_fields = {"name": "", "lambd": ""}
                optional_fields = {"length": "", "diam": "", "temp": "", "Q": ""}
                check_elem(type, data, main_fields, optional_fields)

            elif type == "material":
                main_fields = {"name": ""}
                optional_fields = {"coeff": "", "capacity": "", "density": "", "thickness": ""}
                check_elem(type, data, main_fields, optional_fields)

            elif type == "doors":
                main_fields = {"name": ""}
                optional_fields = {"R": "", "beta": "", "a": "", "q": ""}
                check_elem(type, data, main_fields, optional_fields)
            
            else:
            #elif type == "window":
                main_fields = {"name": ""}
                optional_fields = {"R": "", "a": "", "q": ""}
                check_elem(type, data, main_fields, optional_fields)

            db.session.commit()

            klass = element_to_klass(type)
            id_name = element_to_id_klass(type)
            result = {id_name: getattr(klass.query.filter_by(name = data["name"]).first(),  id_name)}
        else:
            return None
    except Exception as e:
        db.session.rollback()
        result = None
        print(f"put_elem error")
        print(e)
    return result