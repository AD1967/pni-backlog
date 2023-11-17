import datetime
import math
from ..db.common_gets import *
from ..db.model import *

# ДОПОЛНИТЕЛЬНЫЕ ЗАТРАТЫ НА ПРОГРЕВ

countOfPoint = 8 #Количество выводимых знаков после запятой
dt = 1 # Единичный временной промежуток
#function toGCal (x) {

#    return (x * 2.3884e-10).toFixed(5) + " Гкал";
#}

def toGCal(value):
    new_value = value * 2.3884e-10
    return f"{new_value:.{countOfPoint}f} Гкал"

#function convertGCal (x) {
#    return (x * 4230.7e-6).toFixed((5)) + " Гкал";
#}

def convertGCal(value):
    new_value = value * 4230.7e-6
    return f"{new_value:.{countOfPoint}f} Гкал"

#function printGCal (x) {
#    return x.toFixed(5) + " Гкал";
#}

def printGCal(value):
    return f"{value:.{countOfPoint}f}"



#######################################################################################################################################################################
test_temp = -20
n_men  = 10
n_women = 35
n_children = 200
coun_room_with_sinks = 4
air_humidity = 0.7
P0 = 101325
cur_info = ""
########################################################################################################################################################################

#function Q_walls() {
#    let this_build = JSON.parse(localStorage.getItem("this_build"));
#    return (this_build['height'] * this_build['len_sum'] * this_build['floors']) * (materials[walls[this_build['walls_material']]['material']]['capacity'] * thickness['kirpich'] * materials[walls[this_build['walls_material']]['material']]['density'] +  materials['rotband']['capacity'] * thickness['rotband'] * materials['rotband']['density'] +  materials['shtukaturka']['capacity'] * thickness['shtukaturka'] * materials['shtukaturka']['density']) * (temp['heat'] - temp['dezh']);
#}
def update_cur_info(data):
    global cur_info
    cur_info = data
    return ""
def Q_walls(build_id):
    heat = 20
    dezh = 12

    q_reheat = get_one_by_id_build(Q_reheating, build_id)
    period = get_one_from_table(Period, q_reheat.id_period)
    build = q_reheat.build
    
    brick = get_one_from_table(Material, 1)
    rotband = get_one_from_table(Material, 8)
    shtukaturka = get_one_from_table(Material, 9)

    return (build.height * build.len_sum * build.floors) * (q_reheat.walls_material_val.capacity * brick.thickness * \
    q_reheat.walls_material_val.density + rotband.capacity * rotband.thickness * rotband.density + shtukaturka.capacity * \
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
    q_reheat = get_one_by_id_build(Q_reheating, build_id)
    period = get_one_from_table(Period, q_reheat.id_period)
    build = q_reheat.build

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

    Q = (build.len_a * build.len_b - (build.len_sum * build.floors * \
        (brick.thickness + rotband.thickness + shtukaturka.thickness))) * (heat - dezh)

    # Вместо умножения на период в конце
    Q = Q * period.T

    # В оригинале тут === и сравнение с '0' и '1' соответсвенно
    # Но как я понял, имеется в виду, что '0' – это линолеум, а '1' – плиточный клей + плитка
    # Если что – исправим

    if q_reheat.floors_materials == 17:
        return Q * (q_reheat.floors_materials_val.capacity * linoleum.thickness * q_reheat.floors_materials_val.density)
    elif q_reheat.floors_materials == 12:
        return Q * ((q_reheat.floors_materials_val.capacity * plitka.thickness * q_reheat.floors_materials_val.density) + \
            rotband.capacity * glue.thickness * rotband.density)
    else:
        return Q * ((q_reheat.floors_materials_val.capacity * parket.thickness * q_reheat.floors_materials_val.density) + \
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
    q_reheat = get_one_by_id_build(Q_reheating, build_id)
    period = get_one_from_table(Period, q_reheat.id_period)

    return q_reheat.doors_material_val.capacity * q_reheat.count_doors * V * q_reheat.doors_material_val.density * (heat - dezh) * \
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
    q_reheat = get_one_by_id_build(Q_reheating, build_id)
    period = get_one_from_table(Period, q_reheat.id_period)

    return q_reheat.mebel_material_val.capacity * q_reheat.count_shkaf * V * q_reheat.mebel_material_val.density * (heat - dezh) * \
        period.T

########################################################################################################################################################################

#function Q_divan() {
#    let this_build = JSON.parse(localStorage.getItem("this_build"));
#    return materials[materials_select[this_build['divan_material']]['material']]['capacity'] * this_build['divan'] * V['divan'] * materials[materials_select[this_build['divan_material']]['material']]['density'] * (temp['heat'] - temp['dezh']);
#}

def Q_divan(build_id):
    V = get_one_from_table(Volume, 3).value
    q_reheat = get_one_by_id_build(Q_reheating, build_id)
    period = get_one_from_table(Period, q_reheat.id_period)
    heat = 20
    dezh = 12

    return q_reheat.divan_material_val.capacity * q_reheat.count_divan * V * q_reheat.divan_material_val.density * (heat - dezh) * \
        period.T
########################################################################################################################################################################

#function Q_table() {
#    let this_build = JSON.parse(localStorage.getItem("this_build"));
#    return materials[materials_select[this_build['table_material']]['material']]['capacity'] * this_build['table'] * V['table'] * materials[materials_select[this_build['table_material']]['material']]['density'] * (temp['heat'] - temp['dezh']);
#}

def Q_table(build_id):    
    V = get_one_from_table(Volume, 5).value
    q_reheat = get_one_by_id_build(Q_reheating, build_id)
    period = get_one_from_table(Period, q_reheat.id_period)
    heat = 20
    dezh = 12

    return q_reheat.table_material_val.capacity * q_reheat.count_table * V * q_reheat.table_material_val.density * (heat - dezh) * \
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
    q_reheat = get_one_by_id_build(Q_reheating, build_id)
    period = get_one_from_table(Period, q_reheat.id_period)
    count = q_reheat.count_shkafchik
    material_capacity = q_reheat.shkafchik_material_val.capacity
    material_density = q_reheat.shkafchik_material_val.density

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
    q_walls = Q_walls(build_id)
    q_floors = Q_floors(build_id)
    q_shkaf = Q_shkaf(build_id)
    q_shkafchik = Q_shkafchik(build_id)
    q_divan = Q_divan(build_id)
    q_table = Q_table(build_id)
    q_doors = Q_doors(build_id)
    q_all = q_walls + q_floors + q_shkaf + q_shkafchik + q_divan + q_table + q_doors
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
    q_wnd = get_one_by_id_build(Q_wnd, build_id)
    build = q_wnd.build
    this_date = datetime.now()

    weather = get_weather_by_time(datetime.strptime('2022-01-31 22:45:00', "%Y-%m-%d %H:%M:%S"))
    #msYears = 1000 * 60 * 60 * 24 * 365
    #t = math.floor((this_date - datetime.strptime(q_wnd.date_wnd.strftime('%Y-%m-%d'), '%Y-%m-%d')).total_seconds()) * 1000 / msYears
    #tBuild = math.floor((this_date - datetime.strptime(build.date_build.strftime('%Y-%m-%d'), '%Y-%m-%d')).total_seconds()) * 1000 / msYears

    dYears = 365 
    t = math.floor((this_date - datetime.strptime(q_wnd.date_wnd.strftime('%Y-%m-%d'), '%Y-%m-%d')).days)/ dYears
    tBuild = math.floor((this_date - datetime.strptime(build.date_build.strftime('%Y-%m-%d'), '%Y-%m-%d')).days)/ dYears
    window_type = get_one_from_table(Window, int(cur_info['id_window']))
    k = 1
    if tBuild >= 40:
        k = 1.68
    elif tBuild > 1:
        k = 1 + 0.0169 * tBuild
    return (int(cur_info['temp_inside']) - weather.T) * 1.1 * int(cur_info['count_windows']) * int(cur_info['length_wnd'])* int(cur_info['height_wnd']) * \
        k * 8.5984e-7 * dt / window_type.R

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
    q_wnd = get_one_by_id_build(Q_wnd, build_id)
    build = q_wnd.build
    print(cur_info)
    return 1.005 * dt * 2.388458966275e-7 * (build.temp_inside - test_temp) * q_wnd.count_windows * \
        (2 * q_wnd.length_wnd + 2 * q_wnd.height_wnd) * q_wnd.window.q * q_wnd.window.a

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
    return Q_wnd_(build_id)

def calc_eff_wnd_inf(build_id):
    return Q_wnd_inf(build_id)

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
    q_doors = get_one_by_id_build(Q_door, build_id)
    build = q_doors.build
    this_date = datetime.now()

    #msYears = 1000 * 60 * 60 * 24 * 365
    #t = math.floor((this_date - datetime.strptime(q_doors.date_doors.strftime('%Y-%m-%d'), '%Y-%m-%d')).total_seconds()) * 1000 / msYears
    #tBuild = math.floor((this_date - datetime.strptime(build.date_build.strftime('%Y-%m-%d'), '%Y-%m-%d')).total_seconds()) * 1000 / msYears

    dYears = 365
    t = math.floor((this_date - datetime.strptime(q_doors.date_doors.strftime('%Y-%m-%d'), '%Y-%m-%d')).days) / dYears
    tBuild = math.floor((this_date - datetime.strptime(build.date_build.strftime('%Y-%m-%d'), '%Y-%m-%d')).days) / dYears


    k = 1
    if tBuild >= 40:
        k = 1.68
    elif tBuild > 1:
        k = 1 + 0.0169 * tBuild
    
    return (build.temp_inside - test_temp) * (1.1 + q_doors.door.beta * build.height * build.floors) * \
        q_doors.count_doors * q_doors.length_door * q_doors.height_door * k * 8.5984e-7 * dt  / q_doors.door.R

########################################################################################################################################################################

# function Q_doors_inf() {
    # let this_build = JSON.parse(localStorage.getItem("this_build"));
    # return 1.005 * 4000 * 2.388458966275e-7 * (this_build['temp_doors_inside'] - this_build['temp_doors_outside']) *
        # this_build['doors_count'] * (2 * this_build['len_doors'] + 2 * this_build['height_doors']) *
        # doors[this_build['type_windows']].q * doors[this_build['type_windows']].a;
# }

def Q_doors_inf(build_id):
    q_doors = get_one_by_id_build(Q_door, build_id)
    build = q_doors.build
    print(cur_info)
    return 1.005 * dt * 2.388458966275e-7 * (build.temp_inside - test_temp) * q_doors.count_doors * \
        (2 * q_doors.length_door + 2 * q_doors.height_door) * q_doors.door.q * q_doors.door.a

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
    return Q_doors_(build_id)

def calc_eff_doors_inf(build_id):
    return Q_doors_inf(build_id)

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
    build = get_one_by_id_build(Build, build_id)
    q_wnd = get_one_by_id_build(Q_wnd, build_id)
    q_doors = get_one_by_id_build(Q_door, build_id)
    construct = get_one_by_id_build(Q_construct_roof, build_id)
    energoeff = get_one_from_table(Energoeff, construct.constructs_energoeff)

    this_date = datetime.now()
    #msYears = 1000 * 60 * 60 * 24 * 365
    dYears = 365
    #tBuild = math.floor((this_date - datetime.strptime(build.date_build.strftime('%Y-%m-%d'), '%Y-%m-%d')).total_seconds()) * 1000 / msYears
    tBuild = math.floor((this_date - datetime.strptime(build.date_build.strftime('%Y-%m-%d'), '%Y-%m-%d')).days) / dYears


    k = 1
    if tBuild >= 40:
        k = 1.68
    elif tBuild > 1:
        k = 1 + 0.0169 * tBuild
    return (build.temp_inside - test_temp) * \
         (1 + 0.1) * (2 * build.len_a * build.height * build.floors + \
         2 * build.len_b * build.height * build.floors - \
         q_wnd.count_windows * q_wnd.length_wnd * q_wnd.height_wnd - \
         q_doors.count_doors * q_doors.length_door * q_doors.height_door) * \
         k * 8.5984e-7  * dt/  energoeff.R 

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
    roof = get_one_by_id_build(Q_construct_roof, build_id)
    build = roof.build
    energoeff = get_one_from_table(Energoeff, roof.roof_energoeff)

    return build.len_a * build.len_b * (build.temp_inside - test_temp) * \
        8.5984e-7 * dt / energoeff.R

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
    return Q_constructs_(build_id)

def calc_eff_roof(build_id):
    return Q_roof_(build_id)

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
    build = get_one_by_id_build(Build, build_id)
    reliability = get_one_by_id_build(Reliability, build_id)

    k = 5
    if reliability.id_pipe <= 2:
       k = 12

    h = build.height * (build.floors - 1)
    l = 2 * h * coun_room_with_sinks + \
        2 * (build.len_a + build.len_b)

    return k * 3.14 * 0.028 * l * 0.3 * (60 - build.temp_inside) * \
         8.5984e-7 * dt

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
    build = get_one_by_id_build(Build, build_id)
    reliability = get_one_by_id_build(Reliability, build_id)
    q_wnd = get_one_by_id_build(Q_wnd, build_id)
    k = 5
    if reliability.id_pipe <= 2:
       k = 12

    h = build.height
    l = 2 * (build.len_a + build.len_b) + h * q_wnd.count_windows / 2.0

    # Заменили 60 на 90
    # См. файл с диска
    return k * 3.14 * 0.028 * l * 0.3 * (90 - build.temp_inside) * \
         8.5984e-7 * dt

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
    return Q_hws_pipes(build_id)

def calc_eff_heat_pipes(build_id):
    return Q_heat_pipes(build_id)

########################################################################################################################################################################

# // ТЕПЛОПРИТОК ОТ ЛЮДЕЙ
# function Q_people() {
    # let this_build = JSON.parse(localStorage.getItem("this_build"));

    # return  (this_build['mens'] * (220 - 5 * this_build['temp_windows_inside']) +
            # 0.85 * this_build['womens'] * (220 - 5 * this_build['temp_windows_inside'])) *
            # (this_build['time'] / 24) * (8.5984e-7 * 24 * 205);
# }

def Q_people(build_id):
    q_people = get_one_by_id_build(Q_person, build_id)
    build = q_people.build

    return  (n_men * (220 - 5 * build.temp_inside) + \
            0.85 * n_women * (220 - 5 * build.temp_inside) + 0.75 * n_children * (220 - 5 * build.temp_inside)) * \
            8.5984e-7 * dt

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
    return Q_people(build_id)

########################################################################################################################################################################

# // ЗАТРАТЫ РУКОМОЙНИКИ
# function Q_hws_cranes() {
    # let this_build = JSON.parse(localStorage.getItem("this_build"));

    # return  0.00009 * 1000 * 4190 * (this_build['mens'] + this_build['womens']) *
        # 180 * (60 - 15) / 86400 * (8.5984e-7 * 24 * 205);
# }

def Q_hws_cranes(build_id):
    q_people = get_one_by_id_build(Q_person, build_id)

    return  0.00009 * 1000 * 4190 * (n_men + n_women + n_children) * \
        (180.0 * (60 - 15) / 84600.0) * 8.5984e-7 * dt

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
    return Q_hws_cranes(build_id)

########################################################################################################################################################################

# // ЗАТРАТЫ ДУШЕВЫЕ
# function Q_hws_showers() {
    # let this_build = JSON.parse(localStorage.getItem("this_build"));

    # return  0.00018 * 1000 * 4190 * (this_build['mens'] + this_build['womens']) *
        # 500 * (60 - 15) / 86400 * (8.5984e-7 * 24 * 205);
# }

def Q_hws_showers(build_id):
    q_people = get_one_by_id_build(Q_person, build_id)

    return  0.00018 * 1000 * 4190 * (n_men + n_women + n_children) * \
        500 * (60 - 15) / 84600 * 8.5984e-7 * dt

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
    return Q_hws_showers(build_id)

########################################################################################################################################################################

# function Q_electro() {
    # let this_build = JSON.parse(localStorage.getItem("this_build"));
    # if ($('input[name="W_ee_checkbox"]').is(':checked'))
        # return 0.95 * this_build['len_a'] * this_build['len_b'] * this_build['floors'] * 0.0008598/4000;
    # else
        # return 0.95 * $('#W_ee').val() * 0.0008598/4000;
# }

def Q_electro(build_id):
    q_electro = get_one_by_id_build(Q_elec, build_id)
    
    if q_electro.elec_consumption_by_period is None:
        build = q_electro.build
        return 0.95 * build.len_a * build.len_b * build.floors * 8.5984e-7 * dt
    return 0.95 * q_electro.elec_consumption_by_period * 8.5984e-7 * dt
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
    return Q_electro(build_id)

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
    build = get_one_by_id_build(Build, build_id)

    t_in = build.temp_inside
    t_out = test_temp

    n = 1.25
    if build.name.find('Офис') != -1:
       n = 3
    if build.name.find('Школа') != -1: 
       n = 2.5
    A = build.len_a * build.len_b
    h = build.height

    ####### Расчет плотности воздуха #########
    Ps = 133.3 * math.exp(18.6 - 3992/(t_out + 233.8))
    d = 622 * (air_humidity * Ps)/(P0 - air_humidity * Ps)
    P_vp = (d * P0)/(622 + d)
    P_sv = P0 - P_vp
    p_air = (P_sv * 0.029 + P_vp * 0.018)/(8.314 * (t_out + 273.15))
    #######################################
    return 0.28 * 1005 * 8.5984e-7 * p_air * build.len_a * build.len_b * build.floors * build.height * n * (t_in - t_out) * dt

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
    return Q_vent(build_id)

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
    build = get_one_by_id_build(Build, build_id)
    q_floor = get_one_by_id_build(Q_floor, build_id)

    t_in = build.temp_inside
    t_out = test_temp
    a = build.len_a
    b = build.len_b
    h = q_floor.height_floor
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
    return (0.476 * f1 + 0.233 * f2 + 0.116 * f3 + 0.07 * f4) * (t_in - t_out) * 8.5984e-7 * dt

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
    return Q_floor_(build_id)

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