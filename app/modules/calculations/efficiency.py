from datetime import datetime, timedelta, time, date
import math
import os
from ..db.common_gets import *
from ..db.model import *
import pandas as pd

count_of_point = 3  # Количество выводимых знаков после запятой
dt = 1  # Единичный временной промежуток

tec = {
    8: [75, 44],
    7: [75, 44],
    6: [75, 44],
    5: [75, 44],
    4: [75, 44],
    3: [76, 44],
    2: [79, 44],
    1: [82, 45],
    0: [85, 46],
    -1: [87, 47],
    -2: [90, 48],
    -3: [93, 49],
    -4: [95, 50],
    -5: [98, 51],
    -6: [101, 52],
    -7: [103, 53],
    -8: [106, 54],
    -9: [109, 55],
    -10: [111, 56],
    -11: [114, 57],
    -12: [117, 58],
    -13: [119, 59],
    -14: [122, 60],
    -15: [124, 61],
    -16: [127, 62],
    -17: [130, 63],
    -18: [130, 62],
    -19: [130, 61],
    -20: [130, 60],
    -21: [130, 59],
    -22: [130, 58],
    -23: [130, 57],
    -24: [130, 56],
    -25: [130, 55],
    -26: [130, 54]
}
ctp = {
    8: [41, 35],
    7: [43, 36],
    6: [44, 37],
    5: [46, 38],
    4: [48, 39],
    3: [49, 40],
    2: [51, 41],
    1: [52, 42],
    0: [54, 43],
    -1: [56, 45],
    -2: [57, 46],
    -3: [59, 47],
    -4: [61, 48],
    -5: [62, 49],
    -6: [64, 50],
    -7: [65, 51],
    -8: [67, 52],
    -9: [69, 53],
    -10: [70, 54],
    -11: [72, 55],
    -12: [74, 56],
    -13: [76, 57],
    -14: [77, 58],
    -15: [79, 59],
    -16: [80, 60],
    -17: [82, 62],
    -18: [84, 63],
    -19: [85, 64],
    -20: [87, 65],
    -21: [89, 66],
    -22: [90, 67],
    -23: [92, 68],
    -24: [93, 69],
    -25: [95, 70]
}


def toGCal(value):
    new_value = value * 2.3884e-10
    return float(f"{new_value:.{count_of_point}f}")


def convertGCal(value):
    new_value = value * 4230.7e-6
    return f"{new_value:.{count_of_point}f} Гкал"


def set_count_of_point(value):
    return float(f"{value:.{count_of_point}f}")


#######################################################################################################################
test_temp = -20
k_men = 0.98
k_women = 0.98
k_children = 0.98
air_humidity = 0.7
P0 = 101325
cur_info = {}
is_first_day = True
df = []

test_date = ""
#######################################################################################################################


def update_cur_info(data):
    global cur_info
    global is_first_day
    cur_info = data
    is_first_day = True
    create_excel()
    return ""


# Сохранение текущих расчётов
def save(parameters_of_build, data_results, name_excel):
    name_parameters = {
        "name_build": "Название здания",
        "floors": "Этажность здания",
        "length_build": "Длина здания, м",
        "width_build": "Ширина здания, м",
        "length_wall": "Длина стен на одном этаже, м",
        "height_wall": "Высота стен на одном этаже, м",
        "temp_inside": "Температура внутреннего воздуха, °С",
        "temp_outside": "Температура наружного воздуха, °С",
        "date_construction": "Дата постройки",
        "count_windows": "Число окон в здании",
        "length_windows": "Длина типового окна, м",
        "height_windows": "Высота типового окна, м",
        "date_windows": "Дата установки окон",
        "type_windows": "Тип окон",
        "count_doors": "Число дверей",
        "length_doors": "Длина типовой входной двери, м",
        "height_doors": "Высота типовой входной двери, м",
        "type_doors": "Тип дверей",
        "date_doors": "Дата установки дверей",
        "class_energoeff": "Класс энергетической эффективности ограждающих конструкций",
        "count_closet": "Число шкафов",
        "count_sofa": "Число диванов",
        "count_table": "Число столов",
        "count_small_closet": "Число навесных шкафчиков",
        "count_men": "Максимальное число посетителей мужчин",
        "count_women": "Максимальное число посетителей женщин",
        "count_children": "Максимальное число посетителей детей",
        "time_guests": "Среднее время пребывания посетителей в сутки",
        "count_sink": "Количество помещений с раковинами на этаже",
        "height_basement": "Высота подвала, м",
        "period_energosave": "Период энергосбережения",
        "walls_material": "Материал стен",
        "floors_material": "Материал пола",
        "doors_material": "Материал дверей",
        "furniture_material": "Материал мебели",
        "sofa_material": "Материал диванов",
        "table_material": "Материал столов",
        "type_pipe": "Тип трубы"
    }
    name_results = {
        'loss': 'ТЕПЛОПРИТОКИ',
        'loss_trans': 'Потери через ограждающие конструкции (трансмиссионные)',
        'heat_los_win': 'окна',
        'heat_los_inpgr': 'входная группа (двери)',
        'heat_los_heatcond_benv': 'стены',
        'heat_los_heatcond_roof': 'кровля',
        'heat_los_floor': 'пол и фундамент',
        'loss_inf': 'Потери инфильтрационные',
        'inf_win': 'окна',
        'inf_inpgr': 'входная группа (двери)',
        'heat_los_vent': 'система естественной вентиляции',
        'add_heatcosts': 'прогрев здания перед рабочим днем',
        'sum_los': 'СУММА теплопотерь',
        'gains': 'ТЕПЛОПОТЕРИ',
        'heat_gains_people': 'от людей',
        'heat_gains_washstands': 'от магистральных трубопроводов и стояков ГВС к рукомойникам',
        'heat_gains_showers': 'от магистральных трубопроводов и стояков ГВС к душевым',
        'heat_gains_electriclighting': 'от электрооборудования',
        'heat_gains_GVS': 'от неизолированных трубопроводов ГВС',
        'heat_gains_pipelines': 'от неизолированных трубопроводов отопления',
        'sum_add': 'СУММА теплопритоков',
        'razn_los_add': 'РАЗНИЦА теплопотерь и теплопритоков',
        'eclg_sp_tut': 'Эк. ущерб СП т.у.т ',
        'eclg_sp_co2': 'Эк. ущерб СП CO2',
        'tec': 'Расчет ТЭЦ',
        'ctp': 'Расчет ЦТП',
        'razn_tec_ctp': 'Разница ТЭЦ и ЦТП',
        'eclg_tec_ctp_tut': 'Эк. ущерб ТЭЦ/ЦТП т.у.т ',
        'eclg_tec_ctp_co2': 'Эк. ущерб ТЭЦ/ЦТП CO2'
    }

    build = pd.DataFrame.from_dict({name_parameters[key]: parameters_of_build[key] for key in name_parameters.keys()
                                      if parameters_of_build[key] != ''}, orient='index')
    results = pd.DataFrame.from_dict({name_results[key]: data_results.get(key, '') for key in name_results.keys()
                                      if data_results.get(key, ' ') != ''}, orient='index')

    with pd.ExcelWriter('app/' + name_excel, engine='xlsxwriter') as writer:
        build.to_excel(writer, sheet_name='Build')
        results.to_excel(writer, sheet_name='Results')

        # Установить ширину столбцов
        worksheet = writer.sheets['Build']
        worksheet.set_column('A:A', 58)
        worksheet.set_column('B:B', 10)
        worksheet = writer.sheets['Results']
        worksheet.set_column('A:A', 58)
        worksheet.set_column('B:B', 10)


# Расчёт ТЭЦ
def calc_tec(cur_date):
    st = datetime.strptime(cur_date, "%Y-%m-%d")
    st = datetime.combine(st.date(), time(0, 0, 0))
    fn = datetime.combine(st.date(), time(23, 59, 59))
    t = 0
    while st <= fn:
        global test_date
        test_date = st
        weather = get_weather_by_time(st)
        t += weather.T
        st += timedelta(seconds=1800)

    t = int(t / 48)
    # print(" t tec = ", t)

    if t in tec:
        t1, t2 = tec[t]
    else:
        t1, t2 = 0, 0

    res = 0.0643 * 4190 / 3 * (t1 - t2) * 8.5984 * 10 ** (-7) * 24
    return {'tec': res}


# Расчёт ЦТП
def calc_ctp(cur_date):
    st = datetime.strptime(cur_date, "%Y-%m-%d")
    st = datetime.combine(st.date(), time(0, 0, 0))
    fn = datetime.combine(st.date(), time(23, 59, 59))
    t = 0
    while st <= fn:
        global test_date
        test_date = st
        weather = get_weather_by_time(st)
        t += weather.T
        st += timedelta(seconds=1800)

    t = int(t / 48)
    # print(" t ctp = ", t)

    if t in ctp:
        t1, t2 = ctp[t]
    else:
        t1, t2 = 0, 0

    res = 0.0643 * 4190 * (t1 - t2) * 8.5984 * 10 ** (-7) * 24
    return {'ctp': res}


funcs = ['Q_wnd', 'Q_wnd_inf', 'Q_doors_', 'Q_doors_inf', 'Q_constructs', 'Q_roof', 'Q_floor_', 'Q_vent',
         'calc_add_heatcosts', 'Q_people', 'Q_hws_cranes', 'Q_hws_showers', 'Q_electro', 'Q_hws_pipes', 'Q_heat_pipes']
const_calc = []
result_keys = ['heat_los_win', 'inf_win', 'heat_los_inpgr', 'inf_inpgr', 'heat_los_heatcond_benv', 'heat_los_heatcond_roof', 'heat_los_floor', 
          'heat_los_vent', 'add_heatcosts', 'heat_gains_people', 'heat_gains_washstands', 'heat_gains_showers', 'heat_gains_electriclighting', 
          'heat_gains_GVS', 'heat_gains_pipelines']


def add_to_excel(dict_res):
    global df
    df = pd.concat([df, pd.Series(dict_res)], axis=1, ignore_index=True)


def create_excel():
    column = {
        'cur_date': 'Дата',
        'heat_los_win': 'Теплопотери трансмиссионные через окна',
        'inf_win': 'Теплопотери инфильтрационные через окна',
        'heat_los_inpgr': 'Теплопотери трансмиссионные через входную группу',
        'inf_inpgr': 'Теплопотери инфильтрационные через входную группу',
        'heat_los_heatcond_benv': 'Теплопотери теплопроводность через стены',
        'heat_los_heatcond_roof': 'теплопроводность через кровлю',
        'heat_los_floor': 'теплопроводность через пол',
        'heat_los_vent': 'через систему вытяжной вентиляции',
        'add_heatcosts': 'прогрев здания перед рабочим днем',
        'heat_gains_people': 'Теплопритоки от людей',
        'heat_gains_washstands': 'Теплопритоки от ГВС рукомойников',
        'heat_gains_showers': 'Теплопритоки от ГВС душевых',
        'heat_gains_electriclighting': 'Теплопритоки от электрооборудования',
        'heat_gains_GVS': 'Теплопритоки от неизолированных трубопроводов ГВС',
        'heat_gains_pipelines': 'Теплопритоки от неизолированных трубопроводов отопления'
    }
    global df
    df = pd.DataFrame()
    df = pd.concat([df, pd.Series(column)], axis=1, ignore_index=True)


def get_excel(name_excel):
    global df
    if os.path.exists(name_excel):
        os.remove(name_excel)

    with pd.ExcelWriter('app/' + name_excel, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Results', index=False)
        worksheet = writer.sheets['Results']
        worksheet.set_column('A:A', 58)
        worksheet.set_column('B:JN', 10)


def calc_eff(cur_date):
    results = []
    global const_calc
    global funcs
    global result_keys
    global is_first_day

    for name in funcs[:8]:
        func = globals()[name]
        st = datetime.strptime(cur_date, "%Y-%m-%d")
        st = datetime.combine(st.date(), time(0, 0, 0))
        fn = datetime.combine(st.date(), time(23, 59, 59))
        res = 0.
        while (st <= fn):
            global test_date
            test_date = st
            res += func()
            st += timedelta(seconds=1800)
        results.append(set_count_of_point(res))
    
    if is_first_day:  # Если вычисления в первый день, то вычисляем также то, что не зависит от даты, и потом сохраняем в массив
        for name in funcs[8:]:
            func = globals()[name]
            if name == 'calc_add_heatcosts':
                res = func()
            else:
                res = 48 * func()
            results.append(set_count_of_point(res))
        const_calc = results[8:]
        is_first_day = False
    else:  # Если вычисляется уже не первый день, то используем ранее вычисленные данные, которые не зависят от даты
        results.extend(const_calc)

    dict_results = dict(zip(result_keys, results))
    dict_results['cur_date'] = cur_date
    add_to_excel(dict_results)
    return dict(zip(result_keys, results))


######################################################################################################################
# ДОПОЛНИТЕЛЬНЫЕ ЗАТРАТЫ НА ПРОГРЕВ
def Q_walls():
    heat = 20
    dezh = 12
    period = get_one_from_table(Period, int(cur_info['period_energosave']))
    material = get_one_from_table(Material, int(cur_info['walls_material']))
    brick = get_one_from_table(Material, 1)
    rotband = get_one_from_table(Material, 8)
    shtukaturka = get_one_from_table(Material, 9)

    return float(cur_info['height_wall']) * float(cur_info['length_wall']) * float(cur_info['floors']) * (material.capacity * brick.thickness * \
                material.density + rotband.capacity * rotband.thickness * rotband.density + shtukaturka.capacity * \
                shtukaturka.thickness * shtukaturka.density) * (heat - dezh) * period.T


def Q_floors():
    period = get_one_from_table(Period, int(cur_info['period_energosave']))
    material = get_one_from_table(Material, int(cur_info['floors_material']))
    heat = 20
    dezh = 12
    brick = get_one_from_table(Material, 1)
    sosna = get_one_from_table(Material, 5)
    rotband = get_one_from_table(Material, 8)
    shtukaturka = get_one_from_table(Material, 9)
    plitka = get_one_from_table(Material, 12)
    linoleum = get_one_from_table(Material, 17)
    glue = get_one_from_table(Material, 18)
    fanera = get_one_from_table(Material, 19)
    parket = get_one_from_table(Material, 20)

    Q = (float(cur_info['length_build']) * float(cur_info['width_build']) - (float(cur_info['length_wall']) * float(cur_info['floors']) * \
                (brick.thickness + rotband.thickness + shtukaturka.thickness))) * (heat - dezh)

    # Вместо умножения на период в конце
    Q = Q * period.T

    # В оригинале тут === и сравнение с '0' и '1' соответсвенно
    # Но как я понял, имеется в виду, что '0' – это линолеум, а '1' – плиточный клей + плитка
    # Если что – исправим

    if int(cur_info['floors_material']) == 17:
        return Q * (material.capacity * linoleum.thickness * material.density)
    elif int(cur_info['floors_material']) == 12:
        return Q * ((material.capacity * plitka.thickness * material.density) + \
                    rotband.capacity * glue.thickness * rotband.density)
    else:
        return Q * ((material.capacity * parket.thickness * material.density) + \
                    sosna.capacity * fanera.thickness * sosna.density)


def Q_doors():
    V = get_one_from_table(Volume, 1).value
    heat = 20
    dezh = 12

    period = get_one_from_table(Period, int(cur_info['period_energosave']))
    material = get_one_from_table(Material, int(cur_info['doors_material']))
    return material.capacity * float(cur_info['count_doors']) * V * material.density * (heat - dezh) * period.T


def Q_shkaf():
    heat = 20
    dezh = 12
    V = get_one_from_table(Volume, 2).value
    period = get_one_from_table(Period, int(cur_info['period_energosave']))
    material = get_one_from_table(Material, int(cur_info['furniture_material']))
    return material.capacity * float(cur_info['count_closet']) * V * material.density * (heat - dezh) * period.T


def Q_divan():
    V = get_one_from_table(Volume, 3).value
    period = get_one_from_table(Period, int(cur_info['period_energosave']))
    material = get_one_from_table(Material, int(cur_info['sofa_material']))
    heat = 20
    dezh = 12

    return material.capacity * float(cur_info['count_sofa']) * V * material.density * (heat - dezh) * period.T


def Q_table():
    V = get_one_from_table(Volume, 5).value
    period = get_one_from_table(Period, int(cur_info['period_energosave']))
    material = get_one_from_table(Material, int(cur_info['table_material']))
    heat = 20
    dezh = 12

    return material.capacity * float(cur_info['count_table']) * V * material.density * (heat - dezh) * period.T


def Q_shkafchik():
    heat = 20
    dezh = 12
    V = get_one_from_table(Volume, 6).value
    period = get_one_from_table(Period, int(cur_info['period_energosave']))
    material = get_one_from_table(Material, int(cur_info['furniture_material']))
    count = float(cur_info['count_small_closet'])
    material_capacity = material.capacity
    material_density = material.density

    return material_capacity * count * V * material_density * (heat - dezh) * period.T

######################################################################################################################

def calc_add_heatcosts():
    # print(cur_info)
    q_walls = Q_walls()
    q_floors = Q_floors()
    q_shkaf = Q_shkaf()
    q_shkafchik = Q_shkafchik()
    q_divan = Q_divan()
    q_table = Q_table()
    q_doors = Q_doors()
    q_all = q_walls + q_floors + q_shkaf + q_shkafchik + q_divan + q_table + q_doors
    # result = [q_all, q_walls, q_floors, q_doors, q_shkaf, q_divan, q_table, q_shkafchik]
    result = [toGCal(q_all), toGCal(q_walls), toGCal(q_floors), toGCal(q_doors), toGCal(q_shkaf), toGCal(q_divan), \
              toGCal(q_table), toGCal(q_shkafchik)]
    return toGCal(q_all)


def Q_wnd():
    this_date = test_date
    weather = get_weather_by_time(this_date)

    dYears = 365
    t = math.floor((this_date - datetime.strptime(cur_info['date_windows'], '%Y-%m-%d')).days) / dYears
    window_type = get_one_from_table(Window, int(cur_info['type_windows']))
    k = 1
    if t >= 40:
        k = 1.68
    elif t > 1:
        k = 1 + 0.0169 * t
    return (int(cur_info['temp_inside']) - weather.T) * 1.1 * int(cur_info['count_windows']) * int(cur_info['length_windows']) * int(cur_info['height_windows']) * \
           k * 8.5984e-7 * dt / window_type.R


def Q_wnd_inf():
    this_date = test_date
    weather = get_weather_by_time(this_date)
    window_type = get_one_from_table(Window, int(cur_info['type_windows']))
    return 1.005 * dt * 2.388458966275e-7 * (int(cur_info['temp_inside']) - weather.T) * int(cur_info['count_windows']) * \
           (2 * int(cur_info['length_windows']) + 2 * int(cur_info['height_windows'])) * window_type.q * window_type.a


def Q_doors_():
    this_date = test_date
    weather = get_weather_by_time(this_date)
    dYears = 365
    t = math.floor((this_date - datetime.strptime(cur_info['date_doors'], '%Y-%m-%d')).days) / dYears

    door_type = get_one_from_table(Door, int(cur_info['type_doors']))
    k = 1
    if t >= 40:
        k = 1.68
    elif t > 1:
        k = 1 + 0.0169 * t

    return (float(cur_info['temp_inside']) - weather.T) * (1.1 + door_type.beta * float(cur_info['height_wall']) * float(cur_info['floors'])) * \
           float(cur_info['count_doors']) * float(cur_info['length_doors']) * float(cur_info['height_doors']) * k * 8.5984e-7 * dt / door_type.R


def Q_doors_inf():
    this_date = test_date
    weather = get_weather_by_time(this_date)
    door_type = get_one_from_table(Door, int(cur_info['type_doors']))

    return 1.005 * dt * 2.388458966275e-7 * (float(cur_info['temp_inside']) - weather.T) * float(cur_info['count_doors']) * \
           (2 * float(cur_info['length_doors']) + 2 * float(cur_info['height_doors'])) * door_type.q * door_type.a


def Q_constructs():
    energoeff = get_one_from_table(Energoeff, int(cur_info['class_energoeff']))

    this_date = test_date
    weather = get_weather_by_time(this_date)
    dYears = 365
    tBuild = math.floor((this_date - datetime.strptime(cur_info['date_construction'], '%Y-%m-%d')).days) / dYears
    k = 1
    if tBuild >= 40:
        k = 1.68
    elif tBuild > 1:
        k = 1 + 0.0169 * tBuild
    return (float(cur_info['temp_inside']) - weather.T) * \
           (1 + 0.1) * (2 * float(cur_info['length_build']) * float(cur_info['height_wall']) * float(cur_info['floors']) + \
                        2 * float(cur_info['width_build']) * float(cur_info['height_wall']) * float(cur_info['floors']) - \
                        float(cur_info['count_windows']) * float(cur_info['length_windows']) * float(cur_info['height_windows']) - \
                        float(cur_info['count_doors']) * float(cur_info['length_doors']) * float(cur_info['height_doors'])) * \
           k * 8.5984e-7 * dt / energoeff.R


def Q_roof():
    this_date = test_date
    weather = get_weather_by_time(this_date)
    energoeff = get_one_from_table(Energoeff, int(cur_info['class_energoeff']))
    return float(cur_info['length_build']) * float(cur_info['width_build']) * (float(cur_info['temp_inside']) - weather.T) * \
           8.5984e-7 * dt / energoeff.R

#######################################################################################################################
# ТЕПЛОПРИТОКИ

def Q_hws_pipes():
    k = 5
    if int(cur_info['type_pipe']) <= 2:
        k = 12
    h = float(cur_info['height_wall']) * (float(cur_info['floors']) - 1)
    l = 2 * h * int(cur_info['count_sink']) + \
        2 * (float(cur_info['length_build']) + float(cur_info['width_build']))

    return k * 3.14 * 0.028 * l * 0.3 * (60 - float(cur_info['temp_inside'])) * 8.5984e-7 * dt


def Q_heat_pipes():
    k = 5
    if int(cur_info['type_pipe']) <= 2:
        k = 12

    h = float(cur_info['height_wall'])
    l = 2 * (float(cur_info['length_build']) + float(cur_info['width_build'])) + h * float(cur_info['count_windows']) / 2.0

    return k * 3.14 * 0.028 * l * 0.3 * (90 - float(cur_info['temp_inside'])) * 8.5984e-7 * dt


def Q_people():
    n_men = k_men * int(cur_info['count_men'])
    n_women = k_women * int(cur_info['count_women'])
    n_children = k_children * int(cur_info['count_children'])
    return (n_men * (220 - 5 * float(cur_info['temp_inside'])) + \
            0.85 * n_women * (220 - 5 * float(cur_info['temp_inside'])) + 0.75 * n_children * (220 - 5 * float(cur_info['temp_inside']))) * \
           8.5984e-7 * dt


def Q_hws_cranes():
    n_men = k_men * int(cur_info['count_men'])
    n_women = k_women * int(cur_info['count_women'])
    n_children = k_children * int(cur_info['count_children'])
    return 0.00009 * 1000 * 4190 * (n_men + n_women + n_children) * (180.0 * (60 - 15) / 84600.0) * 8.5984e-7 * dt


def Q_hws_showers():
    n_men = k_men * int(cur_info['count_men'])
    n_women = k_women * int(cur_info['count_women'])
    n_children = k_children * int(cur_info['count_children'])
    return 0.00018 * 1000 * 4190 * (n_men + n_women + n_children) * \
           500 * (60 - 15) / 84600 * 8.5984e-7 * dt


def Q_electro():
    # if cur_info['elec_consumption_by_period'] is None:
    #     return 0.95 * float(cur_info['length_build']) * float(cur_info['width_build']) * float(cur_info['floors']) * 8.5984e-7 * dt
    # return 0.95 * float(cur_info['elec_consumption_by_period']) * 8.5984e-7 * dt
    return 0.95 * float(cur_info['length_build']) * float(cur_info['width_build']) * float(cur_info['floors']) * 8.5984e-7 * dt

#######################################################################################################################

def Q_vent():
    this_date = test_date
    weather = get_weather_by_time(this_date)

    t_in = float(cur_info['temp_inside'])
    t_out = weather.T
    air_humidity = weather.U

    n = 1.25
    if cur_info['name_build'].find('Офис') != -1:
        n = 3
    if cur_info['name_build'].find('Школа') != -1:
        n = 2.5
    A = float(cur_info['length_build']) * float(cur_info['width_build'])
    h = float(cur_info['height_wall'])

    # Расчет плотности воздуха
    Ps = 133.3 * math.exp(18.6 - 3992 / (t_out + 233.8))
    d = 622 * (air_humidity * Ps) / (P0 - air_humidity * Ps)
    P_vp = (d * P0) / (622 + d)
    P_sv = P0 - P_vp
    p_air = (P_sv * 0.029 + P_vp * 0.018) / (8.314 * (t_out + 273.15))

    return 0.28 * 1005 * 8.5984e-7 * p_air * A * float(cur_info['floors']) * h * n * (t_in - t_out) * dt


def Q_floor_():
    this_date = test_date
    weather = get_weather_by_time(this_date)

    t_in = float(cur_info['temp_inside'])
    t_out = weather.T
    a = float(cur_info['length_build'])
    b = float(cur_info['width_build'])
    h = float(cur_info['height_basement'])

    S = a * b
    P = 2 * (a + b)
    f1 = f2 = f3 = f4 = 0
    if h <= 2:
        f1_floor = S - (a - (2 - h) * 2) * (b - (2 - h) * 2)
        f1_walls = h * P
        f1 = f1_floor + f1_walls
        f2 = S - (a - 2 - (2 - h) * 2) * (b - 2 - (2 - h) * 2) - f1_floor
        f3 = S - (a - 4 - (2 - h) * 2) * (b - 4 - (2 - h) * 2) - f1_floor - f2
        f4 = S - f1_floor - f2 - f3
        if f2 < 0:
            f2 = S - f1_floor
            f3 = f4 = 0
        if f3 < 0:
            f3 = S - f1_floor - f2
            f4 = 0
    elif h <= 4:
        f1 = 2 * P
        f2_floor = S - (a - (2 - (h - 2)) * 2) * (b - (2 - (h - 2)) * 2)
        f2_walls = (h - 2) * P
        f2 = f2_floor + f2_walls
        f3 = S - (a - (4 - (h - 2)) * 2) * (b - (4 - (h - 2)) * 2) - f2_floor
        f4 = S - f2_floor - f3
        if f3 < 0:
            f3 = S - f2_floor
            f4 = 0
    elif h <= 6:
        f1 = 2 * P
        f2 = 2 * P
        f3_walls = (h - 4) * P
        f3_floor = S - (a - (2 - (h - 4)) * 2) * (b - (2 - (h - 4) * 2))
        f3 = f3_floor + f3_walls
        f4 = S - f3_floor
        if f3_floor < 0:
            f3_floor = S
            f3 = f3_floor + f3_walls
            f4 = 0
    return (0.476 * f1 + 0.233 * f2 + 0.116 * f3 + 0.07 * f4) * (t_in - t_out) * 8.5984e-7 * dt
