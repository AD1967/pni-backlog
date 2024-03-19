
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





//api:
//calc_efficiency
//calc_index
//calc_efficiency_wnd
//calc_efficiency_wnd_inf
//calc_efficiency_doors
//calc_efficiency_doors_inf
//calc_efficiency_constructs
//calc_efficiency_roof
//calc_efficiency_hws_pipes
//calc_efficiency_heat_pipes
//calc_efficiency_people
//calc_efficiency_hws_cranes
//calc_efficiency_hws_showers
//calc_efficiency_electro
//calc_efficiency_vent
//calc_efficiency_floor


// api to block_id
let calc_map = {
    "general":                      "",
    "reliability":                  "/calc_index",
    "heat_los_win":                 "/calc_efficiency_wnd",
    "inf_win":                      "/calc_efficiency_wnd_inf",
    "heat_los_inpgr":               "/calc_efficiency_doors",
    "inf_inpgr":                    "/calc_efficiency_doors_inf",
    "heat_los_heatcond_benv":       "/calc_efficiency_constructs",
    "heat_los_heatcond_roof":       "/calc_efficiency_roof",
    "heat_los_floor":               "/calc_efficiency_floor",
    "heat_los_vent":                "/calc_efficiency_vent",
    "add_heatcosts":                "/calc_efficiency",
    "heat_gains_people":            "/calc_efficiency_people",
    "heat_gains_washstands":        "/calc_efficiency_hws_cranes",
    "heat_gains_showers":           "/calc_efficiency_hws_showers",
    "heat_gains_electriclighting":  "/calc_efficiency_electro",
    "heat_gains_GVS":               "/calc_efficiency_hws_pipes",
    "heat_gains_pipelines":         "/calc_efficiency_heat_pipes",
    "tec":                          "/calc_tec",
    "cpt":                          "/calc_cpt" 
}

let calc_result_map = {
    "general":                      function(result){return result},
    "reliability":                  function(result){
        return "ИТС<sub>надёжность</sub> = " + result.toFixed(5)},
    "heat_los_win":                 function(result){
        return "Тепловые потери через окна<br>Q<sub>окон</sub> = " + result},
    "inf_win":                      function(result){
        return "Инфильтрация через окна<br>Q<sub>рез окон</sub> = " + result},
    "heat_los_inpgr":               function(result){
        return "Тепловые потери через входную группу<br>Q<sub>двери</sub> = " + result},
    "inf_inpgr":                    function(result){
        return "Инфильтрация через входную группу<br>Q<sub>рез двери</sub> = " + result},
    "heat_los_heatcond_benv":       function(result){
        return "Теплопотери посредством теплопроводности через ограждающие конструкции<br>Q<sub>стен</sub> = " + result},
    "heat_los_heatcond_roof":       function(result){
        return "Теплопотери посредством теплопроводности через кровлю<br>Q<sub>стен инфильтр</sub> = " + result},
    "heat_los_floor":               function(result){
        return "Тепловые потери через пол<br>Q<sub>пол</sub> = " + result},
    "heat_los_vent":                function(result){
        return "Тепловые потери от вентиляции<br>Q<sub>вент</sub> = " + result},
    "add_heatcosts":                function(result){
        return "Потребление тепловой энергии за отопительный период<br>Q<sub>∑</sub> = " + result[0] + 
        "<br><br>Q<sub>стены</sub> = " + result[1] + "<br>Q<sub>пол</sub> = " + result[2]  + 
        "<br>Q<sub>дверь</sub> = " + result[3] + "<br>Q<sub>шкаф</sub> = " + result[4] + "<br>Q<sub>диван</sub> = " + result[5] + 
        "<br>Q<sub>стол</sub> = " + result[6]  + "<br>Q<sub>нав. шкафчик</sub> = " + result[7]},
    "heat_gains_people":            function(result){
        return "Теплоприток от людей<br>Q<sub>персонал</sub> = " + result},
    "heat_gains_washstands":        function(result){
        return "Затраты тепловой энергии на ГВС для рукомойников<br>Q<sub>рук</sub> = " + result},
    "heat_gains_showers":           function(result){
        return "Затраты тепловой энергии на ГВС для душевых<br>Q<sub>душ</sub> = " + result},
    "heat_gains_electriclighting":  function(result){
        return "Теплоприток от от системы электроосвещения и силового электроснабжения<br>Q<sub>ЭЭ ОТОП ПЕРИОД</sub> = " + result},
    "heat_gains_GVS":               function(result){
    return "Теплоприток от неизолированных трубопроводов ГВС<br>Q<sub>труб. ГВС</sub> = " + result},
    "heat_gains_pipelines":         function(result){
        return "Теплоприток от неизолированных трубопроводов отопления<br>Q<sub>труб. отопл.</sub> = " + result}
}
let calc_dec_result_map = {
    "general":                  function(result){return result.toFixed(3)},
    "reliability":              function(result){return result.toFixed(3)},
    "heat_los_win":             function(result){return result.toFixed(3)},
    "inf_win":                  function(result){return result.toFixed(3)},
    "heat_los_inpgr":           function(result){return result.toFixed(3)},
    "inf_inpgr":                function(result){return result.toFixed(3)},
    "heat_los_heatcond_benv":   function(result){return result.toFixed(3)},
    "heat_los_heatcond_roof":   function(result){return result.toFixed(3)},
    "heat_los_floor":           function(result){return result.toFixed(3)},
    "heat_los_vent":            function(result){return result.toFixed(3)},
    "add_heatcosts":            function(result){return result.toFixed(3)},
    
    "heat_gains_people":            function(result){return result.toFixed(3)},
    "heat_gains_washstands":        function(result){return result.toFixed(3)},
    "heat_gains_showers":           function(result){return result.toFixed(3)},
    "heat_gains_electriclighting":  function(result){return result.toFixed(3)},
    "heat_gains_GVS":               function(result){return result.toFixed(3)},
    "heat_gains_pipelines":         function(result){return result.toFixed(3)},
    "tec":                          function(result){return result.toFixed(3)},
    "cpt":                          function(result){return result.toFixed(3)}
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
let id_mappers = {};
id_mappers.input_mapper = input_mapper
id_mappers.calc_map = calc_map
id_mappers.calc_result_map = calc_result_map
id_mappers.calc_dec_result_map = calc_dec_result_map
id_mappers.yearsMap = yearsMap

export default id_mappers