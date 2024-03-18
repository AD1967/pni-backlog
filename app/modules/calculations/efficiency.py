from datetime import datetime, timedelta, time, date
import math
import pandas as pd
from ..db.common_gets import *
from ..db.model import *

# ДОПОЛНИТЕЛЬНЫЕ ЗАТРАТЫ НА ПРОГРЕВ

countOfPoint = 3 #Количество выводимых знаков после запятой
dt = 1 # Единичный временной промежуток

excel_template = pd.read_excel('app/modules/db/results_template.xlsx')
excel = excel_template.copy()

column_names = ['тепловые потери через окна', 'инфильтрация через окна', 'тепловые потери через входную группу',
                'инфильтрация через входную группу', 'тепловые потери через ограждающие конструкции',
                'тепловые потери через кровлю', 'тепловые потери через пол', 'тепловые потери, связанные с вентиляцией',
                'доп затраты теплоты', 'сумма потерь', 'теплопритоки от людей', 'затраты тепловой энергии на ГВС для рукомойников',
                'затраты тепловой энергии на ГВС для душевых', 'теплопритоки от систем электроосвещения и силового электроснабжения',
                'теплопритоки от неизолированных трубопроводов ГВС', 'теплопритоки от неизолированных трубопроводов отопления', 'сумма притоков']
df = pd.DataFrame(columns=column_names)

results = [0]*18

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
    8: [75, 33.94],
    7: [75, 34.90],
    6: [75, 35.87],
    5: [75, 36.83],
    4: [75, 37.80],
    3: [75, 38.76],
    2: [75, 39.73],
    1: [77, 40.09],
    0: [81, 41.65],
    -1: [84, 43.58],
    -2: [86, 44.55],
    -3: [89, 45.51],
    -4: [92, 46.48],
    -5: [95, 47.44],
    -6: [97, 48.41],
    -7: [100, 49.37],
    -8: [103, 50.34],
    -9: [106, 51.30],
    -10: [109, 52.57],
    -11: [111, 53.23],
    -12: [114, 54.19],
    -13: [117, 55.18],
    -14: [120, 56.12],
    -15: [122, 57.09],
    -16: [125, 58.05],
    -17: [128, 59.98],
    -18: [128, 60.65],
    -19: [128, 61.91],
    -20: [128, 62.65],
    -21: [128, 63.84],
    -22: [128, 64.81],
    -23: [128, 65.77],
    -24: [128, 66.73],
    -25: [128, 66.78]
}


def toGCal(value):
    new_value = value * 2.3884e-10
    return f"{new_value:.{countOfPoint}f}"

def convertGCal(value):
    new_value = value * 4230.7e-6
    return f"{new_value:.{countOfPoint}f} Гкал"


def printGCal(value):
    return f"{value:.{countOfPoint}f}"



#######################################################################################################################################################################
test_temp = -20
k_men  = 0.98
k_women = 0.98
k_children = 0.98
n_children = 200
coun_room_with_sinks = 4
air_humidity = 0.7
P0 = 101325
cur_info = ""

test_date = ""
########################################################################################################################################################################

#function Q_walls() {
#    let this_build = JSON.parse(localStorage.getItem("this_build"));
#    return (this_build['height'] * this_build['len_sum'] * this_build['floors']) * (materials[walls[this_build['walls_material']]['material']]['capacity'] * thickness['kirpich'] * materials[walls[this_build['walls_material']]['material']]['density'] +  materials['rotband']['capacity'] * thickness['rotband'] * materials['rotband']['density'] +  materials['shtukaturka']['capacity'] * thickness['shtukaturka'] * materials['shtukaturka']['density']) * (temp['heat'] - temp['dezh']);
#}
def update_cur_info(data):
    global cur_info
    cur_info = data
    return ""

def calc_tec():
    st = datetime.strptime(cur_info['cur_date'], "%Y-%m-%d")
    st = datetime.combine(st.date(), time(0, 0, 0))
    fn = datetime.combine(st.date(), time(23, 59, 59))
    res = 0.
    t = 0
    while (st <= fn):
        global test_date
        test_date = st
        weather = get_weather_by_time(st)
        t += weather.T
        st += timedelta(seconds=1800)

    t = int(t/48)
    print(" t tec = ", t)

    if t in tec:
        t1, t2 = tec[t]
    else:
        t1, t2 = 0, 0

    res = 0.0643 * 4190 * (t1 - t2)
    return res


def calc_ctp():
    st = datetime.strptime(cur_info['cur_date'], "%Y-%m-%d")
    st = datetime.combine(st.date(), time(0, 0, 0))
    fn = datetime.combine(st.date(), time(23, 59, 59))
    res = 0.
    t = 0
    while (st <= fn):
        global test_date
        test_date = st
        weather = get_weather_by_time(st)
        t += weather.T
        st += timedelta(seconds=1800)

    t = int(t/48)
    print(" t ctp = ", t)

    if t in ctp:
        t1, t2 = ctp[t]
    else:
        t1, t2 = 0, 0

    res = 0.0643 * 4190 * (t1 - t2)
    return res


def Q_walls(build_id):
    heat = 20
    dezh = 12
    #q_reheat = get_one_by_id_build(Q_reheating, build_id)
    period = get_one_from_table(Period, int(cur_info['id_period']))
    material = get_one_from_table(Material, int(cur_info['walls_material']))
    #build = q_reheat.build
    brick = get_one_from_table(Material, 1)
    rotband = get_one_from_table(Material, 8)
    shtukaturka = get_one_from_table(Material, 9)

    return float(cur_info['height']) * float(cur_info['len_sum']) * float(cur_info['floors']) * (material.capacity * brick.thickness * \
    material.density + rotband.capacity * rotband.thickness * rotband.density + shtukaturka.capacity * \
    shtukaturka.thickness * shtukaturka.density) * (heat - dezh) * period.T
    
########################################################################################################################################################################

#function Q_floors() {
#    let this_build = JSON.parse(localStorage.getItem("this_build"));
#    let Q = (this_build['len_a'] * this_build['len_b'] - (this_build['len_sum'] * this_build['floors'] * (thickness['kirpich'] + thickness['rotband'] + thickness['shtukaturka']))) * (temp['heat'] - temp['dezh']);

#    if (this_build['floors_material'] === '0')
#        return Q * (materials[floors_materials[this_build['floors_material']]['material']]['capacity'] * thickness['linoleum'] * materials[floors_materials[this_build['floors_material']]['material']]['density']);
#    else if (this_build['floors_material'] === '1')
#        return Q * ((materials[floors_materials[this_build['floors_material']]['material']]['capacity'] * thickness['plitka'] * materials[floors_materials[this_build['floors_material']]['material']]['density']) + materials['rotband']['capacity'] * thickness['glue'] * materials['rotband']['density']);
#    else
#        return Q * ((materials[floors_materials[this_build['floors_material']]['material']]['capacity'] * thickness['parket'] * materials[floors_materials[this_build['floors_material']]['material']]['density']) + materials['sosna']['capacity'] * thickness['fanera'] * materials['sosna']['density']);
#}

def Q_floors(build_id):
    #q_reheat = get_one_by_id_build(Q_reheating, build_id)
    #build = q_reheat.build
    period = get_one_from_table(Period, int(cur_info['id_period']))
    material = get_one_from_table(Material, int(cur_info['floors_materials']))
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

    Q = (float(cur_info['len_a']) * float(cur_info['len_b'])  - (float(cur_info['len_sum']) * float(cur_info['floors']) * \
        (brick.thickness + rotband.thickness + shtukaturka.thickness))) * (heat - dezh)

    # Вместо умножения на период в конце
    Q = Q * period.T

    # В оригинале тут === и сравнение с '0' и '1' соответсвенно
    # Но как я понял, имеется в виду, что '0' – это линолеум, а '1' – плиточный клей + плитка
    # Если что – исправим

    if int(cur_info['floors_materials']) == 17:
        return Q * (material.capacity * linoleum.thickness * material.density)
    elif int(cur_info['floors_materials']) == 12:
        return Q * ((material.capacity * plitka.thickness * material.density) + \
            rotband.capacity * glue.thickness * rotband.density)
    else:
        return Q * ((material.capacity * parket.thickness * material.density) + \
            sosna.capacity * fanera.thickness * sosna.density)

########################################################################################################################################################################

#function Q_doors() {
#    let this_build = JSON.parse(localStorage.getItem("this_build"));
#    return materials[materials_select[this_build['doors_material']]['material']]['capacity'] * this_build['doors'] * V['doors'] * materials[materials_select[this_build['doors_material']]['material']]['density'] * (temp['heat'] - temp['dezh']);
#}

def Q_doors(build_id):
    V = get_one_from_table(Volume, 1).value
    heat = 20
    dezh = 12
    
    #period = get_one_from_table(Period, q_reheat.id_period)
    period = get_one_from_table(Period, int(cur_info['id_period']))
    material = get_one_from_table(Material, int(cur_info['doors_material']))
    return material.capacity * float(cur_info['count_doors']) * V * material.density * (heat - dezh) * \
        period.T

########################################################################################################################################################################

#function Q_shkaf() {
#    let this_build = JSON.parse(localStorage.getItem("this_build"));
#    return materials[materials_select[this_build['mebel_material']]['material']]['capacity'] * this_build['shkaf'] * V['shkaf'] * materials[materials_select[this_build['mebel_material']]['material']]['density'] * (temp['heat'] - temp['dezh']);
#}

def Q_shkaf(build_id):
    heat = 20
    dezh = 12
    V = get_one_from_table(Volume, 2).value
    #q_reheat = get_one_by_id_build(Q_reheating, build_id)
    #period = get_one_from_table(Period, q_reheat.id_period)
    period = get_one_from_table(Period, int(cur_info['id_period']))
    material = get_one_from_table(Material, int(cur_info['mebel_material']))
    return material.capacity * float(cur_info['count_shkaf'])  * V * material.density * (heat - dezh) * \
        period.T

########################################################################################################################################################################

#function Q_divan() {
#    let this_build = JSON.parse(localStorage.getItem("this_build"));
#    return materials[materials_select[this_build['divan_material']]['material']]['capacity'] * this_build['divan'] * V['divan'] * materials[materials_select[this_build['divan_material']]['material']]['density'] * (temp['heat'] - temp['dezh']);
#}

def Q_divan(build_id):
    V = get_one_from_table(Volume, 3).value
    #q_reheat = get_one_by_id_build(Q_reheating, build_id)
    #period = get_one_from_table(Period, q_reheat.id_period)
    period = get_one_from_table(Period, int(cur_info['id_period']))
    material = get_one_from_table(Material, int(cur_info['divan_material']))
    heat = 20
    dezh = 12

    return material.capacity * float(cur_info['count_divan']) * V * material.density * (heat - dezh) * \
        period.T
########################################################################################################################################################################

#function Q_table() {
#    let this_build = JSON.parse(localStorage.getItem("this_build"));
#    return materials[materials_select[this_build['table_material']]['material']]['capacity'] * this_build['table'] * V['table'] * materials[materials_select[this_build['table_material']]['material']]['density'] * (temp['heat'] - temp['dezh']);
#}

def Q_table(build_id):    
    V = get_one_from_table(Volume, 5).value
    #q_reheat = get_one_by_id_build(Q_reheating, build_id)
    #period = get_one_from_table(Period, q_reheat.id_period)
    period = get_one_from_table(Period, int(cur_info['id_period']))
    material = get_one_from_table(Material, int(cur_info['table_material']))
    heat = 20
    dezh = 12

    return material.capacity * float(cur_info['count_table']) * V * material.density * (heat - dezh) * \
        period.T
########################################################################################################################################################################

#function Q_shkafchik() {
#    let this_build = JSON.parse(localStorage.getItem("this_build"));
#    return materials[materials_select[this_build['shkafchik_material']]['material']]['capacity'] * this_build['shkafchik'] * V['shkafchik'] * materials[materials_select[this_build['shkafchik_material']]['material']]['density'] * (temp['heat'] - temp['dezh']);
#}

def Q_shkafchik(build_id):
    heat = 20
    dezh = 12
    V = get_one_from_table(Volume, 6).value
    #q_reheat = get_one_by_id_build(Q_reheating, build_id)
    #period = get_one_from_table(Period, q_reheat.id_period)
    period = get_one_from_table(Period, int(cur_info['id_period']))
    material = get_one_from_table(Material, int(cur_info['mebel_material']))
    count = float(cur_info['count_shkafchik'])
    material_capacity = material.capacity
    material_density = material.density

    return material_capacity * count * V * material_density * (heat - dezh) * period.T

########################################################################################################################################################################

# Зачем-то копия Q_shkaf
#// function Q_bett() {
#//     return materials[materials_select[this_build['mebel_material']]['name']]['capacity'] * this_build['shkaf'] * V['shkaf'] * materials[materials_select[this_build['mebel_material']]['name']]['density'] * (temp['heat'] - temp['dezh']);
#// }

########################################################################################################################################################################

# Реализовано в calc_eff, но можно и выделить в функцию, если потом понадобится
# function Q_all() {
#    let this_build = JSON.parse(localStorage.getItem("this_build"));
#    return (Q_doors() + Q_shkaf() + Q_divan() + Q_table() + Q_shkafchik() + Q_walls() + Q_floors()) * period[this_build['period']]['T'];
# }

# Считает, используя функции Q_walls, ..., Q_doors, а также суммирует их вместо Q_all.
# Возвращает значение без перевода, надо ли его добавить?
def calc_eff(build_id):
    print(cur_info)
    q_walls = Q_walls(build_id)
    q_floors = Q_floors(build_id)
    q_shkaf = Q_shkaf(build_id)
    q_shkafchik = Q_shkafchik(build_id)
    q_divan = Q_divan(build_id)
    q_table = Q_table(build_id)
    q_doors = Q_doors(build_id)
    q_all = q_walls + q_floors + q_shkaf + q_shkafchik + q_divan + q_table + q_doors
    results[9] = q_all
    results[10] += q_all
    #result = [q_all, q_walls, q_floors, q_doors, q_shkaf, q_divan, q_table, q_shkafchik]
    # Если надо вернуть в ГКал. Не забыть изменить в calc_index.js:
    result = [toGCal(q_all), toGCal(q_walls), toGCal(q_floors), toGCal(q_doors), toGCal(q_shkaf), toGCal(q_divan), \
        toGCal(q_table), toGCal(q_shkafchik)]
    return result

# function print_coeff_eff() {
#    try {
#        // change_build();
#        let this_build = JSON.parse(localStorage.getItem("this_build"));
#        let result = Q_all();
#        if (typeof (result) != "undefined") {
#
#            $('#coeff_eff').html("Потребление тепловой энергии за отопительный период<br>Q<sub>∑</sub> = " + toGCal(Q_all()));
#            $('#coeff_more').html("Q<sub>стены</sub> = " + toGCal(Q_walls() * period[this_build['period']]['T']) + " ||| " + "Q<sub>пол</sub> = " + toGCal(Q_floors() * period[this_build['period']]['T']) + "<br>" + "Q<sub>дверь</sub> = " + toGCal(Q_doors() * period[this_build['period']]['T']) + " ||| " + "Q<sub>шкаф</sub> = " + toGCal(Q_shkaf() * period[this_build['period']]['T']) + "<br>" + "Q<sub>диван</sub> = " + toGCal(Q_divan() * period[this_build['period']]['T']) + " ||| " + "Q<sub>стол</sub> = " + toGCal(Q_table() * period[this_build['period']]['T']) + "<br>" + "Q<sub>нав. шкафчик</sub> = " + toGCal(Q_shkafchik() * period[this_build['period']]['T']) + "<br>")
#        }
#        else {
#            $('#coeff_eff').html("Q<sub>∑</sub> = " + Q_all());
#            $('#coeff_more').html("");
#        }
#
#    }
#    catch (err) {
#        alert(err);
#        $('#coeff_eff').html("Ошибка при попытке выполнения расчёта. Проверьте данные");
#    }
#}

########################################################################################################################################################################

#// ОКНА
#function Q_wnd() {
#    let this_build = JSON.parse(localStorage.getItem("this_build"));


#    let this_date = Date.now();
#    let msYears = 1000 * 60 * 60 * 24 * 365;
#    let t = Math.floor(this_date - Date.parse(this_build['date_windows'])) / msYears;
#    let tBuild = Math.floor(this_date - Date.parse(this_build['date_build'])) / msYears;
#    let k;
#    if (tBuild <= 1) k = 1;
#    else if (tBuild >= 40) k = 0.35;
#    else k = 1 - 0.0169 * t;

#    return (this_build['temp_windows_inside'] - this_build['temp_windows_outside']) *
#        (1 + 0.1) * this_build['windows'] * this_build['len_windows'] * this_build['height_windows'] *
#        k * (8.5984e-7 * 24 * 205) / windows[this_build['type_windows']].R;
#}

def Q_wnd_(build_id):
    #q_wnd = get_one_by_id_build(Q_wnd, build_id)
    #build = q_wnd.build
    #this_date = datetime.strptime(test_date, "%Y-%m-%d %H:%M:%S")
    this_date = test_date
    print(this_date)
    weather = get_weather_by_time(this_date)
    #msYears = 1000 * 60 * 60 * 24 * 365
    #t = math.floor((this_date - datetime.strptime(q_wnd.date_wnd.strftime('%Y-%m-%d'), '%Y-%m-%d')).total_seconds()) * 1000 / msYears
    #tBuild = math.floor((this_date - datetime.strptime(build.date_build.strftime('%Y-%m-%d'), '%Y-%m-%d')).total_seconds()) * 1000 / msYears

    dYears = 365 
    t = math.floor((this_date - datetime.strptime(cur_info['date_wnd'], '%Y-%m-%d')).days)/ dYears
    tBuild = math.floor((this_date - datetime.strptime(cur_info['date_build'], '%Y-%m-%d')).days)/ dYears
    window_type = get_one_from_table(Window, int(cur_info['id_window']))
    k = 1
    if tBuild >= 40:
        k = 1.68
    elif tBuild > 1:
        k = 1 + 0.0169 * tBuild
    res = (int(cur_info['temp_inside']) - weather.T) * 1.1 * int(cur_info['count_windows']) * int(cur_info['length_wnd'])* int(cur_info['height_wnd']) * \
        k * 8.5984e-7 * dt / window_type.R
    results[1] = res
    results[10] += res
    return res

########################################################################################################################################################################

#function Q_wnd_inf() {
#    let this_build = JSON.parse(localStorage.getItem("this_build"));
#    console.log(windows[this_build['type_windows']].q);
#    console.log(windows[this_build['type_windows']].a);
#    return 1.005 * 4000 * 2.388458966275e-7 * (this_build['temp_windows_inside'] - this_build['temp_windows_outside']) *
#        this_build['windows'] * (2 * this_build['len_windows'] + 2 * this_build['height_windows']) *
#        windows[this_build['type_windows']].q * windows[this_build['type_windows']].a;
#}

def Q_wnd_inf(build_id):
    #q_wnd = get_one_by_id_build(Q_wnd, build_id)
    #build = q_wnd.build
    #this_date = datetime.strptime(test_date, "%Y-%m-%d %H:%M:%S")
    this_date = test_date
    weather = get_weather_by_time(this_date)
    window_type = get_one_from_table(Window, int(cur_info['id_window_inf']))
    res =  1.005 * dt * 2.388458966275e-7 * (int(cur_info['temp_inside']) - weather.T) * int(cur_info['count_windows_inf']) * \
        (2 * int(cur_info['length_wnd_inf']) + 2 * int(cur_info['height_wnd_inf'])) * window_type.q * window_type.a
    results[2] = res
    results[10] += res
    return res

########################################################################################################################################################################

# function print_coeff_eff_wnd() {
    # try {
        # // let this_build = JSON.parse(localStorage.getItem("this_build"));
        # let result = Q_wnd();
        # if (typeof (result) != "undefined") {
            # $('#coeff_eff').html("Тепловые потери через окна<br>Q<sub>окон</sub> = " + printGCal(result));
        # }
        # else {
            # $('#coeff_eff').html("Q<sub>окон</sub> = " + result);
        # }
    # }
    # catch (err) {
        # alert(err);
        # $('#coeff_eff').html("Ошибка при попытке выполнения расчёта. Проверьте данные");
    # }
# }

# function print_coeff_eff_wnd_inf() {
    # try {
        # // let this_build = JSON.parse(localStorage.getItem("this_build"));
        # let result = Q_wnd() - Q_wnd_inf();
        # if (typeof (result) != "undefined") {
            # $('#coeff_eff').html("Инфильтрация через окна<br>Q<sub>рез окон</sub> = " + printGCal(result));
        # }
        # else {
            # $('#coeff_eff').html("Q<sub>окон</sub> = " + result);
        # }
    # }
    # catch (err) {
        # alert(err);
        # $('#coeff_eff').html("Ошибка при попытке выполнения расчёта. Проверьте данные");
    # }
# }

def calc_eff_wnd(build_id):
    print(datetime.strptime(cur_info['cur_date'], "%Y-%m-%d"))
    st = datetime.strptime(cur_info['cur_date'], "%Y-%m-%d")
    st = datetime.combine(st.date(), time(0, 0, 0))
    fn = datetime.combine(st.date(), time(23, 59, 59))
    res = 0.
    while(st <= fn):
        global test_date
        test_date = st
        results[0] = st
        res += Q_wnd_(build_id)
        st += timedelta(seconds = 1800)
    return res

def calc_eff_wnd_inf(build_id):
    print(datetime.strptime(cur_info['cur_date'], "%Y-%m-%d"))
    st = datetime.strptime(cur_info['cur_date'], "%Y-%m-%d")
    st = datetime.combine(st.date(), time(0, 0, 0))
    fn = datetime.combine(st.date(), time(23, 59, 59))
    res = 0.
    while(st <= fn):
        global test_date
        test_date = st
        res += Q_wnd_inf(build_id)
        st += timedelta(seconds = 1800)
    return res

########################################################################################################################################################################

# // ДВЕРИ
# function Q_doors_() {
    # let this_build = JSON.parse(localStorage.getItem("this_build"));


    # let this_date = Date.now();
    # let msYears = 1000 * 60 * 60 * 24 * 365;
    # let t = Math.floor(this_date - Date.parse(this_build['date_doors'])) / msYears;
    # let tBuild = Math.floor(this_date - Date.parse(this_build['date_build'])) / msYears;
    # let k;
    # if (tBuild <= 1) k = 1;
    # else if (tBuild >= 40) k = 0.35;
    # else k = 1 - 0.0169 * t;

    # return (this_build['temp_doors_inside'] - this_build['temp_doors_outside']) *
        # (1 + 0.1 + doors[this_build['type_doors']].beta * this_build['height'] * this_build['floors']) *
        # this_build['doors_count'] * this_build['len_doors'] * this_build['height_doors'] *
        # k * (8.5984e-7 * 24 * 205) / doors[this_build['type_doors']].R;
# }

def Q_doors_(build_id):
    #q_doors = get_one_by_id_build(Q_door, build_id)
    #build = q_doors.build
    #this_date = datetime.now()
    #this_date = datetime.strptime(test_date, "%Y-%m-%d %H:%M:%S")
    this_date = test_date
    weather = get_weather_by_time(this_date)
    #msYears = 1000 * 60 * 60 * 24 * 365
    #t = math.floor((this_date - datetime.strptime(q_doors.date_doors.strftime('%Y-%m-%d'), '%Y-%m-%d')).total_seconds()) * 1000 / msYears
    #tBuild = math.floor((this_date - datetime.strptime(build.date_build.strftime('%Y-%m-%d'), '%Y-%m-%d')).total_seconds()) * 1000 / msYears
    dYears = 365
    t = math.floor((this_date - datetime.strptime(cur_info['date_doors'], '%Y-%m-%d')).days)/ dYears
    tBuild = math.floor((this_date - datetime.strptime(cur_info['date_build'], '%Y-%m-%d')).days)/ dYears

    door_type = get_one_from_table(Door, int(cur_info['id_door']))
    k = 1
    if tBuild >= 40:
        k = 1.68
    elif tBuild > 1:
        k = 1 + 0.0169 * tBuild

    print(cur_info)

    res = (float(cur_info['temp_inside']) - weather.T) * (1.1 + door_type.beta * float(cur_info['height']) * float(cur_info['floors'])) * \
        float(cur_info['q_doors_count_doors']) * float(cur_info['length_door']) * float(cur_info['height_door']) * k * 8.5984e-7 * dt  / door_type.R

    results[3] = res
    results[10] += res
    return res
########################################################################################################################################################################

# function Q_doors_inf() {
    # let this_build = JSON.parse(localStorage.getItem("this_build"));
    # return 1.005 * 4000 * 2.388458966275e-7 * (this_build['temp_doors_inside'] - this_build['temp_doors_outside']) *
        # this_build['doors_count'] * (2 * this_build['len_doors'] + 2 * this_build['height_doors']) *
        # doors[this_build['type_windows']].q * doors[this_build['type_windows']].a;
# }

def Q_doors_inf(build_id):
    #q_doors = get_one_by_id_build(Q_door, build_id)
    #build = q_doors.build
    #this_date = datetime.strptime(test_date, "%Y-%m-%d %H:%M:%S")
    this_date = test_date
    weather = get_weather_by_time(this_date)
    door_type = get_one_from_table(Door, int(cur_info['id_door_inf']))
    print(cur_info)
    print(1.005 * dt * 2.388458966275e-7 * (float(cur_info['temp_inside']) - weather.T) * float(cur_info['count_doors_inf']) * \
        (2 * float(cur_info['length_door_inf']) + 2 * float(cur_info['height_door_inf'])) * door_type.q * door_type.a)
    res = 1.005 * dt * 2.388458966275e-7 * (float(cur_info['temp_inside']) - weather.T) * float(cur_info['count_doors_inf']) * \
        (2 * float(cur_info['length_door_inf']) + 2 * float(cur_info['height_door_inf'])) * door_type.q * door_type.a

    results[4] = res
    results[10] += res
    return res
########################################################################################################################################################################

# function print_coeff_eff_doors() {
    # try {
        # // let this_build = JSON.parse(localStorage.getItem("this_build"));
        # let result = Q_doors_();
        # if (typeof (result) != "undefined") {
            # $('#coeff_eff').html("Тепловые потери через входную группу<br>Q<sub>двери</sub> = " + printGCal(result));
        # }
        # else {
            # $('#coeff_eff').html("Q<sub>окон</sub> = " + result);
        # }
    # }
    # catch (err) {
        # alert(err);
        # $('#coeff_eff').html("Ошибка при попытке выполнения расчёта. Проверьте данные");
    # }
# }
# function print_coeff_eff_doors_inf() {
    # try {
        # // let this_build = JSON.parse(localStorage.getItem("this_build"));
        # let result = Q_doors_() - Q_doors_inf();
        # if (typeof (result) != "undefined") {
            # $('#coeff_eff').html("Инфильтрация через входную группу<br>Q<sub>рез двери</sub> = " + printGCal(result));
        # }
        # else {
            # $('#coeff_eff').html("Q<sub>окон</sub> = " + result);
        # }
    # }
    # catch (err) {
        # alert(err);
        # $('#coeff_eff').html("Ошибка при попытке выполнения расчёта. Проверьте данные");
    # }
# }

def calc_eff_doors(build_id):
    print(datetime.strptime(cur_info['cur_date'], "%Y-%m-%d"))
    st = datetime.strptime(cur_info['cur_date'], "%Y-%m-%d")
    st = datetime.combine(st.date(), time(0, 0, 0))
    fn = datetime.combine(st.date(), time(23, 59, 59))
    res = 0.
    while(st <= fn):
        global test_date
        test_date = st
        res += Q_doors_(build_id)
        st += timedelta(seconds = 1800)
    return res

def calc_eff_doors_inf(build_id):
    print(datetime.strptime(cur_info['cur_date'], "%Y-%m-%d"))
    st = datetime.strptime(cur_info['cur_date'], "%Y-%m-%d")
    st = datetime.combine(st.date(), time(0, 0, 0))
    fn = datetime.combine(st.date(), time(23, 59, 59))
    res = 0.
    while(st <= fn):
        global test_date
        test_date = st
        res += Q_doors_inf(build_id)
        st += timedelta(seconds = 1800)
    return res

########################################################################################################################################################################

# // ОГРАЖДАЮЩИЕ КОНСТРУКЦИИ И КРОВЛЯ
# function Q_constructs() {
    # let this_build = JSON.parse(localStorage.getItem("this_build"));


    # let this_date = Date.now();
    # let msYears = 1000 * 60 * 60 * 24 * 365;

    # let tBuild = Math.floor(this_date - Date.parse(this_build['date_build'])) / msYears;
    # let k;
    # if (tBuild <= 1) k = 1;
    # else if (tBuild >= 40) k = 0.35;
    # else k = 1 - 0.0169 * tBuild;

    # return (this_build['temp_windows_inside'] - this_build['temp_windows_outside']) *
        # (1 + 0.1) * (2 * this_build['len_a'] * this_build['height'] * this_build['floors'] +
        # 2 * this_build['len_b'] * this_build['height'] * this_build['floors'] -
        # this_build['windows'] * this_build['len_windows'] * this_build['height_windows'] -
        # this_build['doors_count'] * this_build['len_doors'] * this_build['height_doors']) *
        # k * (8.5984e-7 * 24 * 205) / energoeff[this_build['energoeff_construct']].R;
# }

def Q_constructs_(build_id):
    print(cur_info)
    #build = get_one_by_id_build(Build, build_id)
    #q_wnd = get_one_by_id_build(Q_wnd, build_id)
    #q_doors = get_one_by_id_build(Q_door, build_id)
    #construct = get_one_by_id_build(Q_construct_roof, build_id)
    energoeff = get_one_from_table(Energoeff, int(cur_info['constructs_energoeff']))

    #this_date = datetime.strptime(test_date, "%Y-%m-%d %H:%M:%S")
    this_date = test_date
    weather = get_weather_by_time(this_date)
    #msYears = 1000 * 60 * 60 * 24 * 365
    dYears = 365
    #tBuild = math.floor((this_date - datetime.strptime(build.date_build.strftime('%Y-%m-%d'), '%Y-%m-%d')).total_seconds()) * 1000 / msYears
    #tBuild = math.floor((this_date - datetime.strptime(build.date_build.strftime('%Y-%m-%d'), '%Y-%m-%d')).days) / dYears
    tBuild = math.floor((this_date - datetime.strptime(cur_info['date_build'], '%Y-%m-%d')).days)/ dYears
    k = 1
    if tBuild >= 40:
        k = 1.68
    elif tBuild > 1:
        k = 1 + 0.0169 * tBuild
    res = (float(cur_info['temp_inside'])- weather.T) * \
         (1 + 0.1) * (2 * float(cur_info['len_a']) * float(cur_info['height']) * float(cur_info['floors']) + \
         2 * float(cur_info['len_b']) * float(cur_info['height']) * float(cur_info['floors']) - \
         float(cur_info['count_windows_c']) * float(cur_info['length_wnd_c']) * float(cur_info['height_wnd_c']) - \
         float(cur_info['count_doors_c']) * float(cur_info['length_door_c']) * float(cur_info['height_door_c'])) * \
         k * 8.5984e-7  * dt/  energoeff.R
    results[5] = res
    results[10] += res
    return res

########################################################################################################################################################################

# function Q_roof() {
    # let this_build = JSON.parse(localStorage.getItem("this_build"));


    # let this_date = Date.now();
    # let msYears = 1000 * 60 * 60 * 24 * 365;

    # let tBuild = Math.floor(this_date - Date.parse(this_build['date_build'])) / msYears;
    # let k;
    # if (tBuild < 1) k = 1;
    # else if (tBuild >= 40) k = 0.35;
    # else k = 1 - 0.0169 * tBuild;

    # return (this_build['len_a'] * this_build['len_b']) * (this_build['temp_windows_inside'] - this_build['temp_windows_outside']) *
        # (8.5984e-7 * 24 * 205) / energoeff[this_build['energoeff_construct']].R;
# }


def Q_roof_(build_id):
    #roof = get_one_by_id_build(Q_construct_roof, build_id)
    #build = roof.build
    print(cur_info)
    #this_date = datetime.strptime(test_date, "%Y-%m-%d %H:%M:%S")
    this_date = test_date
    weather = get_weather_by_time(this_date)
    energoeff = get_one_from_table(Energoeff, int(cur_info['roof_energoeff']))
    res = float(cur_info['len_a']) * float(cur_info['len_b']) * (float(cur_info['temp_inside']) - weather.T) * \
        8.5984e-7 * dt / energoeff.R
    results[6] = res
    results[10] += res

    return res

########################################################################################################################################################################

# function print_coeff_eff_constructs() {
    # try {
        # // let this_build = JSON.parse(localStorage.getItem("this_build"));
        # let result = Q_constructs();
        # if (typeof (result) != "undefined") {
            # $('#coeff_eff').html("Теплопотери посредством теплопроводности через ограждающие конструкции <br>Q<sub>стен</sub> = " + printGCal(result));
        # }
        # else {
            # $('#coeff_eff').html("Q<sub>окон</sub> = " + result);
        # }
    # }
    # catch (err) {
        # alert(err);
        # $('#coeff_eff').html("Ошибка при попытке выполнения расчёта. Проверьте данные");
    # }
# }
# function print_coeff_eff_roof() {
    # try {
        # // let this_build = JSON.parse(localStorage.getItem("this_build"));
        # let result = Q_roof();
        # if (typeof (result) != "undefined") {
            # $('#coeff_eff').html("Теплопотери посредством теплопроводности через кровлю <br>Q<sub>стен инфильтр</sub> = " + printGCal(result));
        # }
        # else {
            # $('#coeff_eff').html("Q<sub>окон</sub> = " + result);
        # }
    # }
    # catch (err) {
        # alert(err);
        # $('#coeff_eff').html("Ошибка при попытке выполнения расчёта. Проверьте данные");
    # }
# }

def calc_eff_constructs(build_id):
    print(datetime.strptime(cur_info['cur_date'], "%Y-%m-%d"))
    st = datetime.strptime(cur_info['cur_date'], "%Y-%m-%d")
    st = datetime.combine(st.date(), time(0, 0, 0))
    fn = datetime.combine(st.date(), time(23, 59, 59))
    res = 0.
    while(st <= fn):
        global test_date
        test_date = st
        res += Q_constructs_(build_id)
        st += timedelta(seconds = 1800)
    return res

def calc_eff_roof(build_id):
    print(datetime.strptime(cur_info['cur_date'], "%Y-%m-%d"))
    st = datetime.strptime(cur_info['cur_date'], "%Y-%m-%d")
    st = datetime.combine(st.date(), time(0, 0, 0))
    fn = datetime.combine(st.date(), time(23, 59, 59))
    res = 0.
    while(st <= fn):
        global test_date
        test_date = st
        res += Q_roof_(build_id)
        st += timedelta(seconds = 1800)
    return res

########################################################################################################################################################################

# // ТЕПЛОПРИТОК ОТ ТРУБОПРОВОДОВ
# function Q_hws_pipes() {
    # let this_build = JSON.parse(localStorage.getItem("this_build"));
    # let k;
    # if (this_build['pipe_type'] <= 2) k = 12;
    # else k = 5;
    # let h = this_build['height'] * this_build['floors'];
    # let l = this_build['ascents_hws'] * h + this_build['descents_hws'] * h +
        # this_build['floors'] * (this_build['len_a'] + this_build['len_b']);
    # return k * 3.14 * 0.0028 * l * (1 - 0.7) * (60 - this_build['temp_windows_inside']) *
        # (8.5984e-7 * 24 * 205);
# }

def Q_hws_pipes(build_id):
    #build = get_one_by_id_build(Build, build_id)
    #reliability = get_one_by_id_build(Reliability, build_id)
    print(cur_info)
    k = 5
    if int(cur_info['hws_type']) <= 2:
       k = 12
    h = float(cur_info['height']) * (float(cur_info['floors']) - 1)
    l = 2 * h * int(cur_info['count_crane']) + \
        2 * (float(cur_info['len_a'])+ float(cur_info['len_b']))

    res = k * 3.14 * 0.028 * l * 0.3 * (60 - float(cur_info['temp_inside'])) * \
         8.5984e-7 * dt
    results[15] = res
    results[17] += res
    return res

########################################################################################################################################################################

# function Q_heat_pipes() {
    # let this_build = JSON.parse(localStorage.getItem("this_build"));
    # let k;
    # if (this_build['pipe_type'] <= 2) k = 12;
    # else k = 5;
    # let h = this_build['height'] * this_build['floors'];
    # let l = this_build['ascents_heat'] * h + this_build['descents_heat'] * h +
        # this_build['floors'] * (this_build['len_a'] + this_build['len_b']);
    # return k * 3.14 * 0.0028 * l * (1 - 0.7) * (60 - this_build['temp_windows_inside']) *
        # (8.5984e-7 * 24 * 205);
# }

def Q_heat_pipes(build_id):
    #build = get_one_by_id_build(Build, build_id)
    #reliability = get_one_by_id_build(Reliability, build_id)
    #q_wnd = get_one_by_id_build(Q_wnd, build_id)
    print(cur_info)
    k = 5
    if int(cur_info['pip_type']) <= 2:
       k = 12

    h = float(cur_info['height'])
    l = 2 * (float(cur_info['len_a']) + float(cur_info['len_b'])) + h * float(cur_info['count_windows_pip']) / 2.0

    # Заменили 60 на 90
    # См. файл с диска
    res = k * 3.14 * 0.028 * l * 0.3 * (90 - float(cur_info['temp_inside'])) * \
         8.5984e-7 * dt
    results[16] = res
    results[17] += res
    return res

########################################################################################################################################################################

# function print_coeff_eff_hws_pipes() {
    # try {
        # // let this_build = JSON.parse(localStorage.getItem("this_build"));
        # let result = Q_hws_pipes();
        # if (typeof (result) != "undefined") {
            # $('#coeff_eff').html("Теплоприток от неизолированных трубопроводов ГВС <br>Q<sub>труб. ГВС</sub> = " + convertGCal(result));
        # }
        # else {
            # $('#coeff_eff').html("Q<sub>окон</sub> = " + result);
        # }
    # }
    # catch (err) {
        # alert(err);
        # $('#coeff_eff').html("Ошибка при попытке выполнения расчёта. Проверьте данные");
    # }
# }
# function print_coeff_eff_heat_pipes() {
    # try {
        # // let this_build = JSON.parse(localStorage.getItem("this_build"));
        # let result = Q_heat_pipes();
        # if (typeof (result) != "undefined") {
            # $('#coeff_eff').html("Теплоприток от неизолированных трубопроводов отопления <br>Q<sub>труб. отопл.</sub> = " + convertGCal(result));
        # }
        # else {
            # $('#coeff_eff').html("Q<sub>окон</sub> = " + result);
        # }
    # }
    # catch (err) {
        # alert(err);
        # $('#coeff_eff').html("Ошибка при попытке выполнения расчёта. Проверьте данные");
    # }
# }

def calc_eff_hws_pipes(build_id):
    print(datetime.strptime(cur_info['cur_date'], "%Y-%m-%d"))
    st = datetime.strptime(cur_info['cur_date'], "%Y-%m-%d")
    st = datetime.combine(st.date(), time(0, 0, 0))
    fn = datetime.combine(st.date(), time(23, 59, 59))
    res = 0.
    while(st <= fn):
        global test_date
        test_date = st
        res += Q_hws_pipes(build_id)
        st += timedelta(seconds = 1800)
    return res

def calc_eff_heat_pipes(build_id):
    print(datetime.strptime(cur_info['cur_date'], "%Y-%m-%d"))
    st = datetime.strptime(cur_info['cur_date'], "%Y-%m-%d")
    st = datetime.combine(st.date(), time(0, 0, 0))
    fn = datetime.combine(st.date(), time(23, 59, 59))
    res = 0.

    while(st <= fn):
        global test_date
        test_date = st
        res += Q_heat_pipes(build_id)
        st += timedelta(seconds = 1800)

        #global excel
        #excel = pd.concat([excel, pd.Series(results)], ignore_index=True)
        #excel.append(pd.Series(results), ignore_index=True)
        #excel.to_excel('results_excel.xlsx', index=False)

        global df
        df.append(pd.Series(results), ignore_index=True)\
        #df = pd.concat([df, pd.Series(results)], ignore_index=True)
        #df.to_excel('results_.xlsx', index=False)

        results = [0]*18

    df.to_excel('results.xlsx', index=False)
    return res

########################################################################################################################################################################

# // ТЕПЛОПРИТОК ОТ ЛЮДЕЙ
# function Q_people() {
    # let this_build = JSON.parse(localStorage.getItem("this_build"));

    # return  (this_build['mens'] * (220 - 5 * this_build['temp_windows_inside']) +
            # 0.85 * this_build['womens'] * (220 - 5 * this_build['temp_windows_inside'])) *
            # (this_build['time'] / 24) * (8.5984e-7 * 24 * 205);
# }

def Q_people(build_id):
    #q_people = get_one_by_id_build(Q_person, build_id)
    #build = q_people.build
    print(cur_info)
    n_men = k_men * int(cur_info['mens'])
    n_women = k_women * int(cur_info['womens'])
    res = (n_men * (220 - 5 * float(cur_info['temp_inside'])) + \
            0.85 * n_women * (220 - 5 * float(cur_info['temp_inside'])) + 0.75 * n_children * k_children * (220 - 5 * float(cur_info['temp_inside']))) * \
            8.5984e-7 * dt
    results[11] = res
    results[17] += res
    return res

########################################################################################################################################################################

# function print_coeff_eff_people() {
    # try {
        # // let this_build = JSON.parse(localStorage.getItem("this_build"));
        # let result = Q_people();
        # if (typeof (result) != "undefined") {
            # $('#coeff_eff').html("Теплоприток от людей <br>Q<sub>персонал</sub> = " + printGCal(result));
        # }
        # else {
            # $('#coeff_eff').html("Q<sub>окон</sub> = " + result);
        # }
    # }
    # catch (err) {
        # alert(err);
        # $('#coeff_eff').html("Ошибка при попытке выполнения расчёта. Проверьте данные");
    # }
# }

def calc_eff_people(build_id):
    print(datetime.strptime(cur_info['cur_date'], "%Y-%m-%d"))
    st = datetime.strptime(cur_info['cur_date'], "%Y-%m-%d")
    st = datetime.combine(st.date(), time(0, 0, 0))
    fn = datetime.combine(st.date(), time(23, 59, 59))
    res = 0.
    while(st <= fn):
        global test_date
        test_date = st
        res += Q_people(build_id)
        st += timedelta(seconds = 1800)
    return res

########################################################################################################################################################################

# // ЗАТРАТЫ РУКОМОЙНИКИ
# function Q_hws_cranes() {
    # let this_build = JSON.parse(localStorage.getItem("this_build"));

    # return  0.00009 * 1000 * 4190 * (this_build['mens'] + this_build['womens']) *
        # 180 * (60 - 15) / 86400 * (8.5984e-7 * 24 * 205);
# }

def Q_hws_cranes(build_id):
    #q_people = get_one_by_id_build(Q_person, build_id)
    print(cur_info)
    n_men = k_men * int(cur_info['mens_w'])
    n_women = k_women * int(cur_info['womens_w'])
    res = 0.00009 * 1000 * 4190 * (n_men + n_women + k_children*n_children) * \
        (180.0 * (60 - 15) / 84600.0) * 8.5984e-7 * dt
    results[12] = res
    results[17] += res
    return res

########################################################################################################################################################################

# function print_coeff_eff_hws_cranes() {
    # try {
        # // let this_build = JSON.parse(localStorage.getItem("this_build"));
        # let result = Q_hws_cranes();
        # if (typeof (result) != "undefined") {
            # $('#coeff_eff').html("Затраты тепловой энергии на ГВС для рукомойников <br>Q<sub>рук</sub> = " + printGCal(result));
        # }
        # else {
            # $('#coeff_eff').html("Q<sub>окон</sub> = " + result);
        # }
    # }
    # catch (err) {
        # alert(err);
        # $('#coeff_eff').html("Ошибка при попытке выполнения расчёта. Проверьте данные");
    # }
# }

def calc_eff_hws_cranes(build_id):
    print(datetime.strptime(cur_info['cur_date'], "%Y-%m-%d"))
    st = datetime.strptime(cur_info['cur_date'], "%Y-%m-%d")
    st = datetime.combine(st.date(), time(0, 0, 0))
    fn = datetime.combine(st.date(), time(23, 59, 59))
    res = 0.
    while(st <= fn):
        global test_date
        test_date = st
        res += Q_hws_cranes(build_id)
        st += timedelta(seconds = 1800)
    return res

########################################################################################################################################################################

# // ЗАТРАТЫ ДУШЕВЫЕ
# function Q_hws_showers() {
    # let this_build = JSON.parse(localStorage.getItem("this_build"));

    # return  0.00018 * 1000 * 4190 * (this_build['mens'] + this_build['womens']) *
        # 500 * (60 - 15) / 86400 * (8.5984e-7 * 24 * 205);
# }

def Q_hws_showers(build_id):
    #q_people = get_one_by_id_build(Q_person, build_id)
    n_men = k_men * int(cur_info['mens_s'])
    n_women = k_women * int(cur_info['womens_s'])
    res =  0.00018 * 1000 * 4190 * (n_men + n_women + k_children*n_children) * \
        500 * (60 - 15) / 84600 * 8.5984e-7 * dt
    results[13] = res
    results[17] += res
    return res

########################################################################################################################################################################

# function print_coeff_eff_hws_showers() {
    # try {
        # // let this_build = JSON.parse(localStorage.getItem("this_build"));
        # let result = Q_hws_showers();
        # if (typeof (result) != "undefined") {
            # $('#coeff_eff').html("Затраты тепловой энергии на ГВС для душевых <br>Q<sub>душ</sub> = " + printGCal(result));
        # }
        # else {
            # $('#coeff_eff').html("Q<sub>окон</sub> = " + result);
        # }
    # }
    # catch (err) {
        # alert(err);
        # $('#coeff_eff').html("Ошибка при попытке выполнения расчёта. Проверьте данные");
    # }
# }

def calc_eff_hws_showers(build_id):
    print(datetime.strptime(cur_info['cur_date'], "%Y-%m-%d"))
    st = datetime.strptime(cur_info['cur_date'], "%Y-%m-%d")
    st = datetime.combine(st.date(), time(0, 0, 0))
    fn = datetime.combine(st.date(), time(23, 59, 59))
    res = 0.
    while(st <= fn):
        global test_date
        test_date = st
        res += Q_hws_showers(build_id)
        st += timedelta(seconds = 1800)
    return res

########################################################################################################################################################################

# function Q_electro() {
    # let this_build = JSON.parse(localStorage.getItem("this_build"));
    # if ($('input[name="W_ee_checkbox"]').is(':checked'))
        # return 0.95 * this_build['len_a'] * this_build['len_b'] * this_build['floors'] * 0.0008598/4000;
    # else
        # return 0.95 * $('#W_ee').val() * 0.0008598/4000;
# }

def Q_electro(build_id):
    #q_electro = get_one_by_id_build(Q_elec, build_id)
    print(cur_info)
    if cur_info['elec_consumption_by_period'] is None:
        #build = q_electro.build
        res = 0.95 * float(cur_info['len_a']) * float(cur_info['len_b'])* float(cur_info['floors']) * 8.5984e-7 * dt
    res = 0.95 * float(cur_info['elec_consumption_by_period']) * 8.5984e-7 * dt
    results[14] = res
    results[17] += res
    return res
########################################################################################################################################################################

# function print_coeff_eff_electro() {
    # try {
        # // let this_build = JSON.parse(localStorage.getItem("this_build"));
        # let result = Q_electro();
        # if (typeof (result) != "undefined") {
            # $('#coeff_eff').html("Теплоприток от системы электроосвещения и силового электроснабжения <br>Q<sub>ЭЭ ОТОП ПЕРИОД</sub> = " + printGCal(result));
        # }
        # else {
            # $('#coeff_eff').html("Q<sub>окон</sub> = " + result);
        # }
    # }
    # catch (err) {
        # alert(err);
        # $('#coeff_eff').html("Ошибка при попытке выполнения расчёта. Проверьте данные");
    # }
# }

def calc_eff_electro(build_id):
    print(datetime.strptime(cur_info['cur_date'], "%Y-%m-%d"))
    st = datetime.strptime(cur_info['cur_date'], "%Y-%m-%d")
    st = datetime.combine(st.date(), time(0, 0, 0))
    fn = datetime.combine(st.date(), time(23, 59, 59))
    res = 0.
    while(st <= fn):
        global test_date
        test_date = st
        res += Q_electro(build_id)
        st += timedelta(seconds = 1800)
    return res

########################################################################################################################################################################

# function Q_vent() {
    # let this_build = JSON.parse(localStorage.getItem("this_build"));

    # let t_in = this_build['temp_vent_inside'];
    # let t_out = this_build['temp_vent_outside'];

    # let n = 1.25;
    # if (this_build['name'].indexOf('офис') !== -1) {n = 3};
    # if (this_build['name'].indexOf('школа') !== -1) {n = 2.5};
    # let A = this_build['len_a'] * this_build['len_b'];
    # let h = this_build['height'];



    # return A * h * n * 1.206 * (t_in - t_out) * 0.24e-6;
# }

def Q_vent(build_id):
    #this_date = datetime.strptime(test_date, "%Y-%m-%d %H:%M:%S")
    this_date = test_date
    weather = get_weather_by_time(this_date)
    #build = get_one_by_id_build(Build, build_id)

    t_in = float(cur_info['temp_inside'])
    t_out = weather.T
    air_humidity = weather.U

    n = 1.25
    if cur_info['name'].find('Офис') != -1:
       n = 3
    if cur_info['name'].find('Школа') != -1: 
       n = 2.5
    A = float(cur_info['len_a']) * float(cur_info['len_b'])
    h = float(cur_info['height'])

    ####### Расчет плотности воздуха #########
    Ps = 133.3 * math.exp(18.6 - 3992/(t_out + 233.8))
    d = 622 * (air_humidity * Ps)/(P0 - air_humidity * Ps)
    P_vp = (d * P0)/(622 + d)
    P_sv = P0 - P_vp
    p_air = (P_sv * 0.029 + P_vp * 0.018)/(8.314 * (t_out + 273.15))
    #######################################
    res = 0.28 * 1005 * 8.5984e-7 * p_air * A * float(cur_info['floors']) * h * n * (t_in - t_out) * dt
    results[8] = res
    results[10] += res
    return res

########################################################################################################################################################################

# function print_coeff_eff_vent() {
    # try {
        # // let this_build = JSON.parse(localStorage.getItem("this_build"));
        # let result = Q_vent();
        # if (typeof (result) != "undefined") {
            # $('#coeff_eff').html("Тепловые потери от вентиляции<br>Q<sub>вент</sub> = " + printGCal(result)) + "<br>M<sub>CO<sub>2</sub></sub>" + (result * 215.76).toFixed(5) + "кг<sub>CO</sub>";
        # }
        # else {
            # $('#coeff_eff').html("Q<sub>окон</sub> = " + result);
        # }
    # }
    # catch (err) {
        # alert(err);
        # $('#coeff_eff').html("Ошибка при попытке выполнения расчёта. Проверьте данные");
    # }
# }

def calc_eff_vent(build_id):
    print(datetime.strptime(cur_info['cur_date'], "%Y-%m-%d"))
    st = datetime.strptime(cur_info['cur_date'], "%Y-%m-%d")
    st = datetime.combine(st.date(), time(0, 0, 0))
    fn = datetime.combine(st.date(), time(23, 59, 59))
    res = 0.
    while(st <= fn):
        global test_date
        test_date = st
        res += Q_vent(build_id)
        st += timedelta(seconds = 1800)
    return res

########################################################################################################################################################################

# function Q_floor() {
    # let this_build = JSON.parse(localStorage.getItem("this_build"));
    
    # let t_in = this_build['temp_floor_inside'];
    # let t_out = this_build['temp_floor_outside'];
    # let h = this_build['height_floor'];
    # let S = this_build['len_a'] * this_build['len_b'];
    # let P = 2 * (this_build['len_a'] + this_build['len_b']);
    # let a = this_build['len_a'];
    # let b = this_build['len_b'];
    # let f1 = 0;
    # let f2 = 0;
    # let f3 = 0;
    # let f4 = 0;
    # if (h <= 2) {
        # let f1_floor = S - (a - (2 - h) * 2) * (b - (2 - h) * 2);
        # let f1_walls = h * P;
        # f1 = f1_floor + f1_walls;
        # f2 = S - (a - 2 - (2 - h) * 2) * (b - 2 - (2 - h) * 2) - f1_floor;
        # f3 = S - (a - 4 - (2 - h) * 2) * (b - 4 - (2 - h) * 2) - f1_floor - f2;
        # f4 = S - f1_floor - f2 - f3;
        # if (f2 < 0) {
            # f2 = S - f1_floor;
            # f3 = 0; f4 = 0;
        # }
        # if (f3 < 0) {
            # f3 = S - f1_floor - f2;
            # f4 = 0;
        # }
    # } else if (h <= 4) {
        # f1 = 2 * P;
        # let f2_floor = S-(a-(2-(h-2))*2)*(b-(2-(h-2))*2);
        # let f2_walls = (h-2)*P;
        # f2 = f2_floor + f2_walls;
        # f3 = S-(a-(4-(h-2))*2)*(b-(4-(h-2))*2)-f2_floor;
        # f4 = S - f2_floor - f3;
        # if (f3 < 0) {
            # f3 = S-f2_floor;
            # f4 = 0;
        # }
    # }
    # else if (h <= 6) {
        # f1 = 2 * P;
        # f2 = 2*P;
        # let f3_walls = (h-4)*P;
        # let f3_floor = S-(a-(2-(h-4))*2)*(b-(2-(h-4)*2));
        # f3 = f3_floor + f3_walls;
        # f4 = S - f3_floor;
        # if (f3_floor < 0) {
            # f3_floor = S; f3 = f3_floor + f3_walls; f4 = 0;
        # }
    # }
    # return (0.476 * f1 + 0.233 * f2 + 0.116 * f3 + 0.07 * f4) * (t_in - t_out) * 3600e-9;
# }

def Q_floor_(build_id):

    #this_date = datetime.strptime(test_date, "%Y-%m-%d %H:%M:%S")
    this_date = test_date
    weather = get_weather_by_time(this_date)

    #build = get_one_by_id_build(Build, build_id)
    #q_floor = get_one_by_id_build(Q_floor, build_id)

    t_in = float(cur_info['temp_inside'])
    t_out = weather.T
    a = float(cur_info['len_a'])
    b = float(cur_info['len_a'])
    h = float(cur_info['height_floor'])

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
        f2_floor = S-(a-(2-(h-2))*2)*(b-(2-(h-2))*2)
        f2_walls = (h-2)*P
        f2 = f2_floor + f2_walls
        f3 = S-(a-(4-(h-2))*2)*(b-(4-(h-2))*2)-f2_floor
        f4 = S - f2_floor - f3
        if f3 < 0:
            f3 = S-f2_floor
            f4 = 0
    elif h <= 6:
        f1 = 2 * P
        f2 = 2*P
        f3_walls = (h-4)*P
        f3_floor = S-(a-(2-(h-4))*2)*(b-(2-(h-4)*2))
        f3 = f3_floor + f3_walls
        f4 = S - f3_floor
        if f3_floor < 0:
            f3_floor = S
            f3 = f3_floor + f3_walls 
            f4 = 0
    res = (0.476 * f1 + 0.233 * f2 + 0.116 * f3 + 0.07 * f4) * (t_in - t_out) * 8.5984e-7 * dt
    results[7] = res
    results[10] += res
    return res

########################################################################################################################################################################

# function print_coeff_eff_floor() {
    # try {
        # // let this_build = JSON.parse(localStorage.getItem("this_build"));
        # let result = Q_floor();
        # if (typeof (result) != "undefined") {
            # $('#coeff_eff').html("Тепловые потери через пол<br>Q<sub>пол</sub> = " + printGCal(result)) + "<br>M<sub>CO<sub>2</sub></sub>" + (result * 215.76).toFixed(5) + "кг<sub>CO<sub>2</sub></sub>";
        # }
        # else {
            # $('#coeff_eff').html("Q<sub>окон</sub> = " + result);
        # }
    # }
    # catch (err) {
        # alert(err);
        # $('#coeff_eff').html("Ошибка при попытке выполнения расчёта. Проверьте данные");
    # }
# }

def calc_eff_floor(build_id):
    print(datetime.strptime(cur_info['cur_date'], "%Y-%m-%d"))
    st = datetime.strptime(cur_info['cur_date'], "%Y-%m-%d")
    st = datetime.combine(st.date(), time(0, 0, 0))
    fn = datetime.combine(st.date(), time(23, 59, 59))
    res = 0.
    while(st <= fn):
        global test_date
        test_date = st
        res += Q_floor_(build_id)
        st += timedelta(seconds = 1800)
    return res

########################################################################################################################################################################

# Нет страницы для этого
# function print_balance() {
    # try {
        # // let this_build = JSON.parse(localStorage.getItem("this_build"));
        # let result = Q_people() + Q_hws_cranes() + Q_hws_showers() + Q_electro() + Q_heat_pipes() + Q_hws_pipes();
        # let result2 = Q_all() + Q_wnd() + Q_wnd_inf() + Q_doors_() + Q_doors_inf() +Q_constructs() + Q_roof();
        # if (typeof (result) != "undefined") {
            # $('#teplopoteri').val(result2);
            # $('#teplopritoki').val(result);
        # }
        # else {
        # }
    # }
    # catch (err) {
        # alert(err);
        # $('#coeff_eff').html("Ошибка при попытке выполнения расчёта. Проверьте данные");
    # }
# }