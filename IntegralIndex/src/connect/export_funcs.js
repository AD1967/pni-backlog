//import requests from '@/connect/server_requests'
import id_mappers from '@/connect/id_mappers'
//import $ from 'jquery'

//функции получения значений полей 

function get_input(self, id, number){
    console.log(self.functions[id_mappers.input_mapper[id]].input)
    if(!self.functions[id_mappers.input_mapper[id]].input[number][4]){
        throw "Ошибка в выбранных блоках есть ошибочные поля"
    }
    return self.functions[id_mappers.input_mapper[id]].input[number][2]
}

function get_select(self, id, number){
    let result = null
    self.functions[id_mappers.input_mapper[id]].select[number][1].forEach(function(item, index){
        
        if (item == self.functions[id_mappers.input_mapper[id]].select[number][3]){
            result = self.functions[id_mappers.input_mapper[id]].select[number][2][index]
            return false
        }
    })
    if(result === null){
        throw ''
    }
    return result
}

function get_date(self, id, number){
    return self.functions[id_mappers.input_mapper[id]].date[number][1]
}

function get_c_box(self, id, number){
    return self.functions[id_mappers.input_mapper[id]].check_elem[number]
}

function get_r_btn(self, id){
    return self.functions[id_mappers.input_mapper[id]].radio_elem[0]
}

function is_block_checked(self, id){
    let result = false
    self.sections.forEach(function(item){
        if(item.name == id){
            result = item.check === 'true'
            return false
        }
    })

    return result
}

function export_b(self){
    console.log("export")
    let build = {}
    build.name = get_input(self, "general", 0)
    self.parametrs_of_build.forEach(function(d) {
        Object.assign(build, d);
    });

    return {"error": false, "result": build}
}

function export_build(self, full){
    console.log("export")
    let build = {}
    try {
        console.log("general")
        //general
        build.name =                    get_input(self, "general", 0)
        build.floors =                  get_input(self, "general", 1)
        build.len_a =                   get_input(self, "general", 2)
        build.len_b =                   get_input(self, "general", 3)
        build.len_sum =                 get_input(self, "general", 4)
        build.height =                  get_input(self, "general", 5)
        build.temp_inside =             get_input(self, "general", 6)
        build.temp_outside =            get_input(self, "general", 7)
        build.date_build =              get_date(self,   "general", 0)
        //если заполнена reliability
        if(full || is_block_checked(self, "reliability")){
            console.log("reliability")
            console.log( get_r_btn(self, "reliability:0"))
            build.ihp =                         get_r_btn(self, "reliability:0") == 'ИТП'
            build.id_pump =                     get_select(self, "reliability:0", 0)
            build.id_heatexchanger =            get_select(self, "reliability:0", 1)
            build.ventsys =                     get_c_box(self, "reliability:0", 0)

            if(build.ventsys) {
                build.readings_vents = []
                let length = get_input(self, "reliability:1", 0)
                
                // ждём обновления массива
                for (let i= 0; i != length; ++i){
                    build.readings_vents.push(get_input(self, "reliability:1", i+1))
                }
            }

            
            build.ascents_hws =                 get_input(self, "reliability:2", 0)
            build.descents_hws =                get_input(self, "reliability:2", 1)
            build.count_crane =                 get_input(self, "reliability:2", 2)

            build.ascents_heat =                get_input(self, "reliability:3", 0)
            build.descents_heat =               get_input(self, "reliability:3", 1)
            build.count_radiator =              get_input(self, "reliability:3", 2)

            build.id_shutoffvalve =         get_select(self, "reliability:4", 0)
            build.id_pipe =                 get_select(self, "reliability:4", 1)
            build.id_radiator =             get_select(self, "reliability:4", 2)
            build.id_crane =                get_select(self, "reliability:4", 3)
        }
        else{
            console.log("skip reliability")
        }
        // Блок heat_los_win
        if (full || is_block_checked(self, "heat_los_win")){
            build.count_windows=                    get_input(self, "heat_los_win", 0)
            // build.temp_inside=                    get_input(self, "heat_los_win", 1)
            // build.temp_outside=                    get_input(self, "heat_los_win", 2)
            build.length_wnd=                    get_input(self, "heat_los_win", 1)
            build.height_wnd=                    get_input(self, "heat_los_win", 2)

            build.id_window=                    get_select(self, "heat_los_win", 0)
            console.log(build.date_wnd)
            build.date_wnd=                    get_date(self, "heat_los_win", 0)
        }        
        else {
            console.log("skip id_q_wnd")
        }
        
        
        // Блок inf_win
        if (full || is_block_checked(self, "inf_win")){
             build.count_windows_inf=                    get_input(self, "inf_win", 0)
            // build.temp_inside=                    get_input(self, "inf_win", 1)
            // build.temp_outside=                    get_input(self, "inf_win", 2)
             build.length_wnd_inf=                    get_input(self, "inf_win", 1)
             build.height_wnd_inf=                    get_input(self, "inf_win", 2)

             build.id_window_inf=                    get_select(self, "inf_win", 0)
             build.date_wnd_inf=                    get_date(self, "inf_win", 0)
        } 
        else {
            console.log("skip inf_win")
        }

        // Блок heat_los_inpgr
        if (full || is_block_checked(self, "heat_los_inpgr")){
            build.q_doors_count_doors=                    get_input(self, "heat_los_inpgr", 0)
            // build.temp_inside=                    get_input(self, "heat_los_inpgr", 1)
            // build.temp_outside=                    get_input(self, "heat_los_inpgr", 2)
            build.length_door=                    get_input(self, "heat_los_inpgr", 1)
            build.height_door=                    get_input(self, "heat_los_inpgr", 2)

            build.id_door=                    get_select(self, "heat_los_inpgr", 0)
            build.date_doors=                    get_date(self, "heat_los_inpgr", 0)
        } else {
            console.log("skip heat_los_inpgr")
        }

        // Блок inf_inpgr
        if (full || is_block_checked(self, "inf_inpgr")){
             build.count_doors_inf=                    get_input(self, "inf_inpgr", 0)
            // build.temp_inside=                    get_input(self, "inf_inpgr", 1)
            // build.temp_outside=                    get_input(self, "inf_inpgr", 2)
             build.length_door_inf=                    get_input(self, "inf_inpgr", 1)
             build.height_door_inf=                    get_input(self, "inf_inpgr", 2)

             build.id_door_inf=                    get_select(self, "inf_inpgr", 0)
             build.date_doors_inf=                    get_date(self, "inf_inpgr", 0)
        } 
        else {
            console.log("skip inf_inpgr")
        }
        
        // Блок heat_los_heatcond_benv
        if (full || is_block_checked(self, "heat_los_heatcond_benv")) {
            build.constructs_energoeff=                    get_select(self, "heat_los_heatcond_benv", 0) 
            build.count_windows_c = get_input(self, "heat_los_heatcond_benv", 0)
            build.length_wnd_c=                    get_input(self, "heat_los_heatcond_benv", 1)
            build.height_wnd_c=                    get_input(self, "heat_los_heatcond_benv", 2)
            build.count_doors_c=                    get_input(self, "heat_los_heatcond_benv", 3)
            build.length_door_c=                    get_input(self, "heat_los_heatcond_benv", 4)
            build.height_door_c=                    get_input(self, "heat_los_heatcond_benv", 5)
        }
        else {
            console.log("skip heat_los_heatcond_benv")
        }
        
        // Блок heat_los_heatcond_roof
        if (full || is_block_checked(self, "heat_los_heatcond_roof")) {
            build.roof_energoeff=                    get_select(self, "heat_los_heatcond_roof", 0)
        } 
        else {
            console.log("skip heat_los_heatcond_roof")
        }

        // Блок heat_los_floor
        if(full || is_block_checked(self, "heat_los_floor")){
            console.log("Q_floor")
        
            build.height_floor=                    get_input(self, "heat_los_floor", 0)
            // build.temp_inside=                    get_input(self, "heat_los_floor", 1)
            // build.temp_outside=                    get_input(self, "heat_los_floor", 2)

        }
        else{
            console.log("skip Q_floor")
        }

        // Блок heat_los_vent
        if(full || is_block_checked(self, "heat_los_vent")){
            console.log("Q_floor")
        
            // build.temp_inside=                     get_input(self, "heat_los_vent", 0)
            // build.temp_outside=                    get_input(self, "heat_los_vent", 1)

        }
        else{
            console.log("skip Q_floor")
        }

        // Блок add_heatcosts
        if(full || is_block_checked(self, "add_heatcosts")){
            console.log("Q_reheating")

            build.count_doors=                    get_input(self, "add_heatcosts:0", 0)
            build.count_shkaf=                    get_input(self, "add_heatcosts:0", 1)
            build.count_divan=                    get_input(self, "add_heatcosts:0", 2)
            build.count_table=                    get_input(self, "add_heatcosts:0", 3)
            build.count_shkafchik=                    get_input(self, "add_heatcosts:0", 4)

            build.id_period=                    get_select(self, "add_heatcosts:1", 0)

            build.walls_material=                    get_select(self, "add_heatcosts:2", 0)
            build.floors_materials=                    get_select(self, "add_heatcosts:2", 1)
            build.doors_material=                    get_select(self, "add_heatcosts:2", 2)
            build.mebel_material=                    get_select(self, "add_heatcosts:2", 3)
            build.divan_material=                    get_select(self, "add_heatcosts:2", 4)

            build.table_material=                    get_select(self, "add_heatcosts:2", 5)
            build.shkafchik_material=                get_select(self, "add_heatcosts:2", 6)

        }
        else{
            console.log("skip Q_reheating")
        }





        // Блок heat_gains_people
        if (full || is_block_checked(self, "heat_gains_people")) {
            console.log("Q_people")
            build.mens = get_input(self, "heat_gains_people", 0)
            build.womens = get_input(self, "heat_gains_people", 1)
            build.children = get_input(self, "heat_gains_people", 2)//!!!!!!!!!!
            build.time_average = get_input(self, "heat_gains_people", 3)//!!!!!!!!!!
        } else {
            console.log("skip heat_gains_people")
        }
        // heat_gains_washstands
        if (full || is_block_checked(self, "heat_gains_washstands")) {
            console.log("Q_people")
            build.mens_w = get_input(self, "heat_gains_washstands", 0)
            build.womens_w = get_input(self, "heat_gains_washstands", 1)
            //build.time_average = get_input(self, "heat_gains_washstands", 2)
        } else {
            console.log("skip heat_gains_washstands")
        }
        // heat_gains_showers
        if (full || is_block_checked(self, "heat_gains_showers")) {
            console.log("Q_people")
            build.mens_s = get_input(self, "heat_gains_showers", 0)
            build.womens_s = get_input(self, "heat_gains_showers", 1)
            //build.time_average = get_input(self, "heat_gains_washstands", 2)
        } else {
            console.log("skip heat_gains_showers")
        }
        // Блок heat_gains_electriclighting
        if (full || is_block_checked(self, "heat_gains_electriclighting")) {
            let tmp = get_c_box(self, "heat_gains_electriclighting", 0)
            if(tmp){
                build.elec_consumption_by_period = null
            }
            else{
                build.elec_consumption_by_period = get_input(self, "heat_gains_electriclighting", 3)
            }
        } else {
            console.log("skip heat_gains_electriclighting")
        }

        //heat_gains_GVS
        if (full || is_block_checked(self, "heat_gains_GVS")) {
            console.log("heat_gains_GVS")
            build.count_crane = get_input(self, "heat_gains_GVS", 5)
            build.hws_type = get_select(self, "heat_gains_GVS", 0)
        } else {
            console.log("skip heat_gains_GVS")
        }

        //heat_gains_pipelines
        if (full || is_block_checked(self, "heat_gains_pipelines")) {
            console.log("heat_gains_pipelines")
            build.count_windows_pip = get_input(self, "heat_gains_pipelines", 5)
            build.pip_type = get_select(self, "heat_gains_pipelines", 0)
        } else {
            console.log("skip heat_gains_pipelines")
        }

        return {"error": false, "result": build}
    } 
    catch (error) {
        return {"error": true, "text": error}
    }
}


let export_funcs = {};
export_funcs.export_build = export_build
export_funcs.export_b = export_b


export default export_funcs