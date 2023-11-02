from datetime import datetime, time, date
from app.modules.db.model import DbGetError, Weather
from ..db.model import *
import itertools
from flask import g

from_tablename_to_methodname = {
    'Q_people' : 'q_peoples',
    'Q_reheating' : 'q_reheat',
    'doors' : 'door',
    'readings_vent' : 'reading'
}

#для таблиц без id_build
def element_to_klass(type):
    if type == "doors":
        type = "door"
    return get_elem_class_by_str(first_char_to_upper(type))

#для таблиц без id_build
def element_to_id_klass(type):
    return f"id_{type}"

# получение значения из таблицы  reliability по id_build
def get_one_by_id_build(klass, id_build):
    try:
        res = klass.query.filter_by(id_build=id_build).first()
        if(res == None):
            raise
        return res
    except:
        raise DbGetError(f"get_by_id_build, ошибка чтения из БД, id_build = {id_build}")

# получение значения из таблицы  klass по id_klass
def get_one_from_table(klass, id):
    try:
        res = klass.query.filter_by(**{f"id_{klass.__tablename__.lower() if from_tablename_to_methodname.get(klass.__tablename__) is None else from_tablename_to_methodname.get(klass.__tablename__)}": id}).first()
        if(res == None):
            raise
        return res
    except:
        raise DbGetError(f"get_from_table, ошибка чтения из БД, id_{klass.__tablename__.lower()} = {id}")

# получение значения из readings_vent  airheater по reliability
def get_readings_vents(id_reliability):
    try:
        return Readings_vent.query.filter_by(id_reliability=id_reliability).all()
    except:
        raise DbGetError(f"get_readings_vents, ошибка чтения из БД, id_reliability = {id_reliability}")


# получение конфигурации(й) с заданными полями (или со всеми) (при ошибке - None)
# работает только в запросах с токенами (нужен юзер)
def get_build(fields, id_build = None):
    data = []
    try:
        if(id_build is None):
            user = g.current_user
            admin = User.query.filter_by(name="admin").first()
            admin_builds = Build.query.filter_by(id_user=admin.id_user).all()
            if admin.id_user != user.id_user:
                user_builds = Build.query.filter_by(id_user=user.id_user).all()
            else:
                user_builds = []
        else:
            admin_builds = []
            user_builds = [Build.query.filter_by(id_build = id_build).first()]
        
        for build in itertools.chain(admin_builds, user_builds):
            q_reheating = Q_reheating.query.filter_by(id_build=build.id_build).first()
            reliability = Reliability.query.filter_by(id_build=id_build).first()

            full_build = build.columns_to_dict()
            full_build["date_build"] = build.date_build.strftime('%Y-%m-%d')
            if(not reliability is None):
                readings_vents = get_readings_vents(reliability.id_reliability)
                if len(readings_vents) != 0:
                    readings_vents_values = []
                    for r in readings_vents:
                        readings_vents_values.append(r.value)
                    full_build["readings_vents"] = readings_vents_values
            
            for table in [Q_floor,Q_construct_roof, Q_person, Q_door, Q_wnd, Q_elec]:
                elem = table.query.filter_by(id_build=build.id_build).first()
                if(not elem is None):
                    if(table == Q_door):
                        tmp = elem.columns_to_dict()
                        tmp["q_doors_count_doors"] = tmp["count_doors"]
                        del tmp["count_doors"]
                        full_build.update(tmp)
                    else:
                        full_build.update(elem.columns_to_dict())
                    if(table == Q_wnd):
                        full_build[ 'date_wnd'] = full_build[ 'date_wnd'].strftime('%Y-%m-%d')
                    elif(table == Q_door):
                        full_build[ 'date_doors'] = full_build[ 'date_doors'].strftime('%Y-%m-%d')
            #period
            for elem in [q_reheating, reliability]:
                if(not elem is None):
                    full_build.update(elem.columns_to_dict())
            
            if(len(fields) != 0):
                fields_list = set(fields.keys())
                keys = list(full_build.keys())
                for key in keys:
                    if not key in fields_list:
                        del full_build[key]
            data.append(full_build)
    except:
        data = None
        print(f"get_build error")
    return data


# получение элемента(ов) заданного типа с заданными полями (или со всеми) (при ошибке - None)
# работает только в запросах с токенами (нужен юзер)
get_element_elements = [
    "convector", "period", "volume", "airheater", "tempcontroller", "energoeff", "shutoffvalve",
    "heatexchanger", "pump", "crane", "radiator", "pipe", "material", "doors", "window"
]
def get_element(type, fields, id = None):
    if type in get_element_elements:
        data = []
        try:
            if type in from_tablename_to_methodname:
                type = from_tablename_to_methodname[type]
            klass = get_elem_class_by_str(first_char_to_upper(type))
            if(id is None):
                elems = klass.query.all()
            else:
                elems = [klass.query.filter_by(**{f"id_{type}": id}).first()]
            
            for elem in elems:
                elem_dict = elem.columns_to_dict()
                if(len(fields) != 0):
                    fields_list = set(fields.keys())
                    keys = list(elem_dict.keys())
                    for key in keys:
                        if not key in fields_list:
                            del elem_dict[key]
                data.append(elem_dict)
        except:
            data = None
            print(f"get_element error")
    else: 
        data = None
    return data
#Получение данных о погоде на ттекуущий момент времени 
def get_weather_by_time(cur_time):
    try:
        res = 1
        cur_time = datetime.combine(cur_time.date(), time(cur_time.hour, (30 if cur_time.minute >= 30 else 0), cur_time.second))
        res = Weather.query.filter(Weather.Time == datetime.strftime(cur_time, "%Y-%m-%d %H:%M:%S")).first();
        if res == None : 
            raise
        return res
    except:
        raise DbGetError(f"get_by_id_build, ошибка чтения из БД, weather")

