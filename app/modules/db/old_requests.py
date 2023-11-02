from . import db
from .model import Build, get_elem_class_by_str, first_char_to_upper

# получение конфигурации
def get_building(id):
    try:
        res = Build.query.filter_by(id_build=id).first()
        if(res == None):
            return {}
        return res.columns_to_dict()
    except:
        print("get_building, ошибка чтения из БД")
        return None

# получение всех конфигураций
def get_buildings():
    try:
        res = Build.query.all()
        result = []
        for r in res:
            result.append({"id": r.id_build, "name": r.name})
        return result
    except:
        print("db_get_buildings, ошибка чтения из БД")
        return None
    
# получение "тестовой" конфигурации (дефолтная)
def get_test_build():
    try:
        res = Build.query.filter_by(name="Тестовая схема здания").first()
        if(res == None):
            return {}
        return res.columns_to_dict()
    except:
        print("get_building, ошибка чтения из БД")
        return None

# получение "элемента" (т.е. строка таблицы type c id_{type} равным id)
def get_element(type, id):
    try:
        elem = get_elem_class_by_str(first_char_to_upper(type))
        res = elem.query.filter_by(**{f"id_{type}": id}).first()
        if(res == None):
            return {}
        return res.columns_to_dict()
    except:
        print(f"get_element, ошибка чтения из БД, id_{type} = {id}")
        return None

# получение "элементов" (т.е. строки таблицы type c id_{type} равным id)
def get_elements(type):
    try:
        elem = get_elem_class_by_str(first_char_to_upper(type))
        res = elem.query.all()
        result = []
        i = 0
        for r in res:
            result.append({"id": getattr(r, f'id_{type}'), "name": r.name})
        return result
    except:
        print("get_elements, ошибка чтения из БД")
        return None