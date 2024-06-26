import datetime
import math
from ..db.common_gets import *
from ..db.model import *



def P(lambd, tau) :
    return math.exp(-lambd * tau)

def PL(lambd, tau, length) :
    return math.exp(-lambd * tau * length)

def Q(x) :
    return 1 - x

def g_ventilation_system(reliability, t):
    ##?????????????????????????????
    l_air_heater = get_one_from_table(Airheater, 1).lambd

    l_pipe = get_one_from_table(Pipe, reliability['type_pipe']).lambd
    l_crane = get_one_from_table(Crane, reliability['type_crane']).lambd

    readings_vent = get_readings_vents(int(reliability['id_build']))
    result = 1
    for i in range(0, len(readings_vent)):
        result *= Q(PL(l_pipe, t, readings_vent[i].value) * P(l_air_heater, t) * PL(l_pipe, t, readings_vent[i].value))

    print("вентиляция", Q(result))
    return Q(result)

def g_hws_system(reliability, t):
    l_crane = get_one_from_table(Crane, reliability['type_crane']).lambd
    l_pump = get_one_from_table(Pump, reliability['type_pump']).lambd
    build = get_one_from_table(Build, int(reliability['id_build']))

    cranes_on_floor = math.pow(P(l_crane, t), reliability['count_crane'])
    floors_on_descent = math.pow(cranes_on_floor, build.floors)
    descent_on_ascent = 1
    for i in range(0,  int(reliability['count_up_hws'])):
        descent_on_ascent *= Q(floors_on_descent)

    descent_on_ascent = Q(descent_on_ascent)
    result = 1
    for i in range(0,  int(reliability['count_down_hws'])):
        result *= Q(descent_on_ascent)
    
    print("гвс", Q(result) * P(l_pump, t))
    return Q(result) * P(l_pump, t)

def g_heat_system(reliability, t):
    l_pipe = get_one_from_table(Pipe, reliability['type_pipe']).lambd
    l_radiator = get_one_from_table(Radiator, reliability['type_radiator']).lambd
    l_shutoff = get_one_from_table(Shutoffvalve, reliability['type_armature']).lambd
    build = get_one_from_table(Build, int(reliability['id_build']))

    P_radiator = PL(l_pipe, t, 1.5) * P(l_shutoff, t) * P(l_radiator, t) * P(l_shutoff, t) * PL(l_pipe, t, 1.5)
    radiators_on_floor = 1
    for i in range(0,  int(reliability['count_radiator'])):
        radiators_on_floor *= Q(P_radiator)

    radiators_on_floor = Q(radiators_on_floor)
    floors_on_descent = math.pow(radiators_on_floor, build.floors)
    descents_on_ascent = 1
    for i in range(0,  int(reliability['count_down_loft'])):
        descents_on_ascent *= Q(floors_on_descent)
    
    descents_on_ascent = Q(descents_on_ascent)
    result = 1
    for i in range(0,  int(reliability['count_up_loft'])):
        result *= Q(descents_on_ascent)
    
    print("отопление", Q(result))
    return Q(result)


# класс для вычисления
class IndexCalcError(Exception):
    pass

def calc_index(parametrs_of_reliability):
    reliability = parametrs_of_reliability
    # reliability = get_one_by_id_build(Reliability, build_id)
    # if(reliability == None): return None
    build = get_one_from_table(Build, int(reliability['id_build']))

    this_date = datetime.now()
    #msHours = 60 * 60
    ventilation_system = lambda t: g_ventilation_system(reliability, t)
    hws_system = lambda t: g_hws_system(reliability, t)
    heat_system = lambda t: g_heat_system(reliability, t)

    #t = math.floor(
    #    (this_date - datetime.strptime(build.date_build.strftime('%Y-%m-%d'), '%Y-%m-%d')
    #).total_seconds()) / msHours
    print(this_date - datetime.strptime(build.date_build.strftime('%Y-%m-%d'), '%Y-%m-%d'))
    t = math.floor((
        (this_date - datetime.strptime(build.date_build.strftime('%Y-%m-%d'), '%Y-%m-%d')).seconds)/3600)
    l_shutoff = get_one_from_table(Shutoffvalve, reliability['type_armature']).lambd
    l_pump = get_one_from_table(Pump, reliability['type_pump']).lambd
    l_heat_exchanger = get_one_from_table(Heatexchanger, reliability['type_heatexchanger']).lambd
    if (int(reliability['elev_itp'])):
        if(int(reliability['ventsys'])):
            if (int(reliability['count_up_hws']) != 0):
                if (int(reliability['count_up_loft']) != 0):
                    return  Q(Q(P(l_shutoff, t) * Q( Q(P(l_heat_exchanger, t)) * Q(ventilation_system(t))) * P(l_shutoff, t)) *
                            Q(P(l_shutoff, t) * Q( Q(P(l_heat_exchanger, t)) * Q(hws_system(t))) * P(l_shutoff, t)) *
                            Q(P(l_shutoff, t) * Q( Q(P(l_heat_exchanger, t)) * Q(heat_system(t))) * P(l_shutoff, t)) ) * P(l_pump, t)
                else:
                    return Q( Q(P(l_shutoff, t) * Q( Q(P(l_heat_exchanger, t)) * Q(ventilation_system(t))) * P(l_shutoff, t)) *
                                Q(P(l_shutoff, t) * Q( Q(P(l_heat_exchanger, t)) * Q(hws_system(t))) * P(l_shutoff, t)) ) * P(l_pump, t)
            else:
                if (int(reliability['count_up_loft']) != 0) :
                    return Q( Q(P(l_shutoff, t) * Q( Q(P(l_heat_exchanger, t)) * Q(ventilation_system(t))) * P(l_shutoff, t)) *
                        Q(P(l_shutoff, t) * Q( Q(P(l_heat_exchanger, t)) * Q(heat_system(t))) * P(l_shutoff, t)) ) * P(l_pump, t)
                else:
                    return P(l_shutoff, t) * Q( Q(P(l_heat_exchanger, t)) * Q(ventilation_system(t))) * P(l_shutoff, t) * P(l_pump, t)
        else:
            if (int(reliability['count_up_hws']) != 0) :
                if (int(reliability['count_up_loft']) != 0) :
                    return Q( Q(P(l_shutoff, t) * Q( Q(P(l_heat_exchanger, t)) * Q(hws_system(t))) * P(l_shutoff, t)) *
                        Q(P(l_shutoff, t) * Q( Q(P(l_heat_exchanger, t)) * Q(heat_system(t))) * P(l_shutoff, t)) ) * P(l_pump, t)
                else:
                    return P(l_shutoff, t) * Q( Q(P(l_heat_exchanger, t)) * Q(hws_system(t))) * P(l_shutoff, t) * P(l_pump, t)
            else:
                if (int(reliability['count_up_loft']) != 0) :
                    return P(l_shutoff, t) * Q( Q(P(l_heat_exchanger, t)) * Q(heat_system(t))) * P(l_shutoff, t) * P(l_pump, t)
                else:
                    raise IndexCalcError('undefined')
    else:
        if(int(reliability['ventsys'])) :
            if (int(reliability['count_up_hws']) != 0) :
                if (int(reliability['count_up_loft']) != 0):
                    return Q( Q(P(l_shutoff, t) * ventilation_system(t) * P(l_shutoff, t)) *
                                Q(P(l_shutoff, t) * hws_system(t) * P(l_shutoff, t)) *
                                Q(P(l_shutoff, t) * heat_system(t) * P(l_shutoff, t)))
                else:
                    return Q( Q(P(l_shutoff, t) * ventilation_system(t) * P(l_shutoff, t)) *
                        Q(P(l_shutoff, t) * hws_system(t) * P(l_shutoff, t)))
            else:
                if (int(reliability['count_up_loft'])  != 0) :
                    return Q( Q(P(l_shutoff, t) * ventilation_system(t) * P(l_shutoff, t)) *
                        Q(P(l_shutoff, t) * heat_system(t) * P(l_shutoff, t)))
                else:
                    return P(l_shutoff, t) * ventilation_system(t) * P(l_shutoff, t)
        else:
            if (int(reliability['count_up_hws']) != 0) :
                if (int(reliability['count_up_loft'])  != 0) :
                    return Q(Q(P(l_shutoff, t) * hws_system(t) * P(l_shutoff, t)) *
                        Q(P(l_shutoff, t) * heat_system(t) * P(l_shutoff, t)))
                else:
                    return P(l_shutoff, t) * hws_system(t) * P(l_shutoff, t)
            else:
                if (int(reliability['count_up_loft'])  != 0) :
                    return P(l_shutoff, t) * heat_system(t) * P(l_shutoff, t)
                else:
                    raise IndexCalcError('undefined')