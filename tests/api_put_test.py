from for_all_tests import test_with_auth_put
from for_all_tests import test_with_auth_add
# import requests
# import json

json1 = {
    # build
    "name": "Моя схема1",
    "floors": 3,
    "len_a": 10,
    "len_b": 20,
    "len_sum": 30,
    "height": 100,
    "date_build": "2015-01-01",
    "temp_inside": 20,
    "temp_outside": 30,

    # Q_floor
    "height_floor": 100,

    # Q_people
    "mens": 2,
    "womens": 1,
    "time_average": 200,

    # Q_doors
    "q_doors_count_doors": 5, 
    "length_door": 120,
    "height_door": 200,
    "id_door": 6,                   # обязательный айдишник
    "date_doors": "2015-01-01",

    # Q_wnd
    "count_windows": 5,
    "length_wnd": 200,
    "height_wnd": 200,
    "id_window": 3,                 # обязательный айдишник
    "date_wnd": "2015-01-01",

    # Q_reliability
    "id_pipe": 2,           # обязательный айдишник
    "id_radiator": 2,       # обязательный айдишник
    "id_crane": 2,          # обязательный айдишник
    "ihp": 1,               # необязательное поле
    "id_pump": 2,           # необязательный айдишник
    "id_heatexchanger": 2,  # необязательный айдишник
    "id_shutoffvalve": 2,   # обязательный айдишник
    "ventsys": 1,           # необязательное поле *
    "ascents_hws": 2,       # необязательное поле
    "descents_hws": 2,      # необязательное поле
    "count_crane": 1,       # необязательное поле
    "ascents_heat": 3,      # необязательное поле
    "descents_heat": 3,     # необязательное поле
    "count_radiator": 1,    # необязательное поле
    
    # Q_readings_vent
    # необязательное поле *
    "readings_vents" : [300, 300, 80, 80 , 120 , 50, 80, 50, 80],

    # # Q_reheating
    # "count_doors": 10,
    # "count_shkaf": 9,
    # "count_divan": 10,
    # "count_table": 11,
    # "count_shkafchik": 10,
    # "id_period": 2,         # необязательный айдишник
    # "walls_material": 1,
    # "floors_materials": 17,
    # "doors_material": 5,
    # "mebel_material": 16,
    # "divan_material": 14,
    # "table_material": 15,
    # "shkafchik_material": 11,

    # "constructs_energoeff": 5,  # обязательный айдишник
    # "roof_energoeff": 5,        # необязательный айдишник

#elec
    "elec_consumption_by_period": 100

}

json2 = {
    # build
    "name": "Моя схема2",
    "floors": 2,
    "len_a": 150,
    "len_b": 200,
    "len_sum": 350,
    "height": 100,
    "date_build": "2022-01-01",
    "temp_inside": 15,
    "temp_outside": 20,

    # Q_floor
    "height_floor": 150,

    # Q_people
    "mens": 5,
    "womens": 0,
    "time_average": 150,

    # # Q_vent
    # "vent_temp_inside": 20,
    # "vent_temp_outside": 31,

    # Q_doors
    "q_doors_count_doors": 3, 
    "length_door": 130,
    "height_door": 220,
    "id_door": 6,
    "date_doors": "2022-01-01",

    # Q_wnd
    "count_windows": 4,
    "length_wnd": 200,
    "height_wnd": 200,
    "id_window": 3,
    "date_wnd": "2022-01-01",

    # Q_reliability
    "id_pipe": 2, 
    "id_radiator": 2,
    "id_crane": 2,
    # "ihp": 1,
    # "id_pump": 2,
    # "id_heatexchanger": 2,
    "id_shutoffvalve": 2,
    "ventsys": 1,
    "ascents_hws": 2,
    "descents_hws": 2,
    "count_crane": 1,
    "ascents_heat": 3,
    "descents_heat": 3,
    "count_radiator": 1,
    
    # Q_readings_vent
    "readings_vents" : [300, 300, 80, 80 , 120 , 50, 80, 50, 80],

    # Q_reheating
    "count_doors": 10,
    "count_shkaf": 9,
    "count_divan": 10,
    "count_table": 11,
    "count_shkafchik": 10,
    #"id_period": 2,
    "walls_material": 1,
    "floors_materials": 17,
    "doors_material": 5,
    "mebel_material": 16,
    "divan_material": 14,
    "table_material": 15,
    "shkafchik_material": 11,

    "constructs_energoeff": 5,
    "roof_energoeff": 5,

}

json3 = {
    # build
    "name": "Моя схема3",
    "floors": 3,
    "len_a": 10,
    "len_b": 20,
    "len_sum": 30,
    "height": 100,
    "date_build": "2015-01-01",
    "temp_inside": 10,
    "temp_outside": 15,

    # Q_floor
    "height_floor": 100,

    # Q_people
    "mens": 2,
    "womens": 1,
    "time_average": 200,

    # # Q_vent
    # "vent_temp_inside": 15,
    # "vent_temp_outside": 30,

    # Q_doors
    "q_doors_count_doors": 5, 
    "length_door": 120,
    "height_door": 200,
    "id_door": 6,
    "date_doors": "2015-01-01",

    # Q_wnd
    "count_windows": 5,
    "length_wnd": 200,
    "height_wnd": 200,
    "id_window": 3,
    "date_wnd": "2015-01-01",

    # Q_reliability
    #"id_pipe": 2,
    "id_radiator": 2,
    "id_crane": 2,
    "ihp": 1,
    "id_pump": 2,
    "id_heatexchanger": 2,
    "id_shutoffvalve": 2,
    "ventsys": 1,
    "ascents_hws": 2,
    "descents_hws": 2,
    "count_crane": 1,
    "ascents_heat": 3,
    "descents_heat": 3,
    "count_radiator": 1,
    
    # Q_readings_vent
    "readings_vents" : [300, 300, 80, 80 , 120 , 50, 80, 50, 80],

    # Q_reheating
    "count_doors": 10,
    "count_shkaf": 9,
    "count_divan": 10,
    "count_table": 11,
    "count_shkafchik": 10,
    "id_period": 2,
    "walls_material": 1,
    "floors_materials": 17,
    "doors_material": 5,
    "mebel_material": 16,
    "divan_material": 14,
    "table_material": 15,
    "shkafchik_material": 11,

    "constructs_energoeff": 5,
    "roof_energoeff": 5,

}

json4 = {
    # build
    "name": "Моя схема1",
    "floors": 2,
    "len_a": 150,
    "len_b": 200,
    "len_sum": 350,
    "height": 100,
    "date_build": "2022-01-01",
    "temp_inside": 15,
    "temp_outside": 20,

    # Q_floor
    "height_floor": 150,

    # Q_people
    "mens": 5,
    "womens": 0,
    "time_average": 150,

    # # Q_vent
    # "vent_temp_inside": 20,
    # "vent_temp_outside": 31,

    # Q_doors
    "q_doors_count_doors": 3, 
    "length_door": 130,
    "height_door": 220,
    "id_door": 6,
    "date_doors": "2022-01-01",

    # Q_wnd
    "count_windows": 4,
    "length_wnd": 200,
    "height_wnd": 200,
    "id_window": 3,
    "date_wnd": "2022-01-01",

    # Q_reliability
    "id_pipe": 2, 
    "id_radiator": 2,
    "id_crane": 2,
    # "ihp": 1,
    # "id_pump": 2,
    # "id_heatexchanger": 2,
    "id_shutoffvalve": 2,
    "ventsys": 1,
    "ascents_hws": 2,
    "descents_hws": 2,
    "count_crane": 1,
    "ascents_heat": 3,
    "descents_heat": 3,
    "count_radiator": 1,
    
    # Q_readings_vent
    "readings_vents" : [300, 300, 80, 80 , 120 , 50, 80, 50, 80],

    # Q_reheating
    "count_doors": 10,
    "count_shkaf": 9,
    "count_divan": 10,
    "count_table": 11,
    "count_shkafchik": 10,
    #"id_period": 2,
    "walls_material": 1,
    "floors_materials": 17,
    "doors_material": 5,
    "mebel_material": 16,
    "divan_material": 14,
    "table_material": 15,
    "shkafchik_material": 11,

#
    "constructs_energoeff": 5,
    "roof_energoeff": 5,

}

# Добавление и изменение конфигураций
test_with_auth_put("1", url = "http://127.0.0.1:5000/data/build", json=json1)
test_with_auth_put("2", url = "http://127.0.0.1:5000/data/build", json=json2)
test_with_auth_put("3", url = "http://127.0.0.1:5000/data/build", json=json3)
test_with_auth_put("4", url = "http://127.0.0.1:5000/data/build", json=json4)


elem_json = {
    "name": "Мой конвектор",
    "power": 150,
    "lambd": 330,
}

elem_json2 = {
    "name": "Мой радиатор",
    "power_section": 550,
    "count_section": 1000,
    "lambd": 100
}

# Добавление новых записей в таблицы, которые не связаны по id_build
# test_with_auth_add("1", url = "http://127.0.0.1:5000/data/element/convector", json=elem_json)
# test_with_auth_add("2", url = "http://127.0.0.1:5000/data/element/radiator", json=elem_json2)
# test_with_auth_add("3", url = "http://127.0.0.1:5000/data/element/convector", json=elem_json3)
# test_with_auth_add("4", url = "http://127.0.0.1:5000/data/element/airheater", json=elem_json4)
