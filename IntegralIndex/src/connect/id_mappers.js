
// id в номер блока (в массисве)
let input_mapper = {
    "general":                      0,
    "reliability:0":                1,
    "reliability:1":                2,
    "reliability:2":                3,
    "reliability:3":                4,
    "heat_los_win":                 5,
    "inf_win":                      6,
    "heat_los_inpgr":               7,
    "inf_inpgr":                    8,
    "heat_los_heatcond_benv":       9,
    "heat_los_heatcond_roof":       10,
    "heat_los_floor":               11,
    "heat_los_vent":                12,
    "add_heatcosts":                13,
    "add_heatcosts:0":              13,
    "add_heatcosts:1":              14,
    "add_heatcosts:2":              15,
    'heat_gains_people':            16,
    'heat_gains_washstands':        17,
    'heat_gains_showers':           18,
    'heat_gains_electriclighting':  19,
    'heat_gains_GVS':               20,
    'heat_gains_pipelines':         21,
    'reliability:4':                22,
}

let calc_map = {
    "general":                      "",
    "formula_calc":                 "/calc_efficiency",
    "reliability":                  "/calc_index",
    "tec":                          "/calc_tec_ctp",
}

let yearsMap = {
    "Тестовая дата - 01.09.2022": [new Date('2022-09-01 00:00:00'), new Date('2022-09-01 23:59:59')],
    "2014-15 - самая тёплая зима": [new Date('2014-09-01 00:00:00'), new Date('2015-05-31 23:59:59')],
    "2018-19": [new Date('2018-09-01 00:00:00'), new Date('2019-05-31 23:59:59')],
    "2019-20": [new Date('2019-09-01 00:00:00'), new Date('2020-05-31 23:59:59')],
    "2020-21 - самая холодная зима": [new Date('2020-09-01 00:00:00'), new Date('2021-05-31 23:59:59')],
    "2021-22": [new Date('2021-09-01 00:00:00'), new Date('2022-05-31 23:59:59')],
    "2022-23": [new Date('2022-09-01 00:00:00'), new Date('2023-05-31 23:59:59')]
}

let calc_name_map ={
    "formula_calc":                 "Расчет по СП 50.13330.2012",
    "reliability":                  "Расчёт надёжности",
    "tec":                          "Расчёт отпуска тепловой энергии ТЭЦ",
    "ctp":                          "Расчёт потребления тепловой энергии от ЦТП",
    "ins":                          "Расчёт искусственной нейронной сетью"
}

let id_mappers = {};
id_mappers.input_mapper = input_mapper
id_mappers.calc_map = calc_map
id_mappers.yearsMap = yearsMap
id_mappers.calc_name_map = calc_name_map
export default id_mappers