import requests from '@/connect/server_requests'
import id_mappers from '@/connect/id_mappers'
import $ from 'jquery'

//ошибка == исключение
//нет ошибки == результат
function check_error(result, name, self){       //, self)
    let checked = requests.default_asget_promise_request_check(result, self)       //, self)
    if(checked.fail){
        throw "";
    }
    return result["result"]
}



function set_input(self, id, number, val){
    self.functions[id_mappers.input_mapper[id]].input[number][4] = true
    self.functions[id_mappers.input_mapper[id]].input[number][2] = val
}

function set_select_variants(self, id, number, lst, id_name){
    lst.forEach(function(item){
        self.functions[id_mappers.input_mapper[id]].select[number][1].push(item.name)
        self.functions[id_mappers.input_mapper[id]].select[number][2].push(item[id_name])
    })
}

function set_select(self, id, number, lst, id_name, val){
    self.functions[id_mappers.input_mapper[id]].select[number][1] = []
    self.functions[id_mappers.input_mapper[id]].select[number][2] = []
    self.functions[id_mappers.input_mapper[id]].select[number][3] = ''
    lst.forEach(function(item){
        self.functions[id_mappers.input_mapper[id]].select[number][1].push(item.name)
        self.functions[id_mappers.input_mapper[id]].select[number][2].push(item[id_name])
    })
    self.functions[id_mappers.input_mapper[id]].select[number][3] = val
}

function set_date(self, id, number, val){
    self.functions[id_mappers.input_mapper[id]].date[number][1] = val
}

function set_c_box(self, id, number, val){
    self.functions[id_mappers.input_mapper[id]].check_elem[number] = val
}

function set_r_btn(self, id, val){
    self.functions[id_mappers.input_mapper[id]].radio_elem[0] = val
}



// удаление ненужных полей, очистка

function clear_funcs(self){
    self.build_changes = new Set()
    self.results.forEach(function(item){
        item.val = ""
    })
    self.functions.forEach(function(item){
        if(item.select !== null){
            item.select.forEach(function(sel_item){
                sel_item[1] = []
                sel_item[2] = []
                sel_item[3] = ''
            })
        }
        if(item.check_elem !== null && item.check_elem !== undefined){
            console.log(item.check_elem)
            item.check_elem.forEach(function(item1, index){
                item.check_elem[index] = false
            })
        }
        if(item.input !== null){
            item.input.forEach(function(item1, index){
                item.input[index][2] = ''
            })
        }
    })
}

//поиск нужного эелемета по id

function find_elem_by_id(elems, id, id_name){
    let result = ''
    elems.forEach(function(item){
        if(item[id_name] == id){
            result = item
            return false
        }
    })
    return result
}

//установка select сразу со значением

function set_select_with_name(self, id, number, lst, id_name, val_id){
    set_select(self,id, number, lst, id_name, find_elem_by_id(lst,  val_id, id_name).name)
}

function load_build(self, id_build, result_func){
    try {
        $.when(
            requests.async_json_promise_get('/data/build/' + id_build),
            requests.async_json_promise_get('/data/builds?' + $.param({name: '',id_build:''})),
            requests.async_json_promise_get("/data/elements/shutoffvalve?" + $.param({name: '',id_shutoffvalve:''})),
            requests.async_json_promise_get("/data/elements/pipe?" + $.param({name: '',id_pipe:''})),
            requests.async_json_promise_get("/data/elements/radiator?" + $.param({name: '',id_radiator:''})),
            requests.async_json_promise_get("/data/elements/crane?" + $.param({name: '',id_crane:''})),
            requests.async_json_promise_get("/data/elements/heatexchanger?" + $.param({name: '',id_heatexchanger:''})),
            requests.async_json_promise_get("/data/elements/pump?" + $.param({name: '',id_pump:''})),
            requests.async_json_promise_get("/data/elements/window?" + $.param({name: '',id_window:''})),
            requests.async_json_promise_get("/data/elements/doors?" + $.param({name: '',id_door:''})),
            requests.async_json_promise_get("/data/elements/energoeff?" + $.param({name: '',id_energoeff:''})), ///!!!!!!!!!!!!!!!тут
            requests.async_json_promise_get("/data/elements/period?" + $.param({name: '',id_period:''})),
            requests.async_json_promise_get("/data/elements/material?" + $.param({name: '',id_material:''}))
        ).done(function (
            build_r,builds_r, shutoffvalves_r,pipes_r,radiators_r,cranes_r,heatexchangers_r,
            pumps_r,windows_r,doors_r,energoeffs_r,periods_r,materials_r 
        ) {
            try {
                let builds = check_error(builds_r, "builds", self)       //, self)
                let build = check_error(build_r, "build", self)       //, self)
                let shutoffvalves = check_error(shutoffvalves_r, "shutoffvalves", self)       //, self)
                let pipes = check_error(pipes_r, "pipes", self)       //, self)
                let radiators = check_error(radiators_r, "radiators", self)       //, self)
                let cranes = check_error(cranes_r, "cranes", self)       //, self)
                let heatexchangers = check_error(heatexchangers_r, "heatexchangers", self)       //, self)
                let pumps = check_error(pumps_r, "pumps", self)       //, self)
                let windows = check_error(windows_r, "windows", self)       //, self)
                let doors = check_error(doors_r, "doors", self)       //, self)
                let energoeffs = check_error(energoeffs_r, "energoeffs", self)       //, self)
                let periods = check_error(periods_r, "periods", self)       //, self)
                let materials = check_error(materials_r, "materials", self)       //, self)

                clear_funcs(self)

                self.load_pat.select.variants = []
                self.load_pat.select.ids = []
                self.load_pat.select.picked = ''
                builds.forEach(function (item) {
                    self.load_pat.select.variants.push(item.name)
                    self.load_pat.select.ids.push(item["id_build"])
                })
                self.load_pat.select.picked = build.name


                //settings
                self.parametrs_of_build.floors                  = build.floors
                self.parametrs_of_build.length_build            = build.len_a      
                self.parametrs_of_build.width_build             = build.len_b      
                self.parametrs_of_build.length_wall             = build.len_sum        
                self.parametrs_of_build.height_wall             = build.height       
                self.parametrs_of_build.temp_inside             = build.temp_inside        
                self.parametrs_of_build.temp_outside            = build.temp_outside      
                self.parametrs_of_build.date_build              = build.date_build
                self.parametrs_of_build.count_windows           = build.count_windows      
                self.parametrs_of_build.length_windows          = build.length_wnd    
                self.parametrs_of_build.height_windows          = build.height_wnd    
                self.parametrs_of_build.date_windows            = build.date_wnd       
                self.parametrs_of_build.type_windows            = build.id_window      
                self.parametrs_of_build.count_doors             = build.q_doors_count_doors       
                self.parametrs_of_build.length_doors            = build.length_door       
                self.parametrs_of_build.height_doors            = build.height_door       
                self.parametrs_of_build.type_doors              = build.id_door         
                self.parametrs_of_build.date_doors              = build.date_doors         
                self.parametrs_of_build.class_energoeff         = build.constructs_energoeff    
                self.parametrs_of_build.count_closet            = build.count_shkaf       
                self.parametrs_of_build.count_sofa              = build.count_divan         
                self.parametrs_of_build.count_table             = build.count_table        
                self.parametrs_of_build.count_small_closet      = build.count_shkafchik 
                self.parametrs_of_build.count_men               = build.mens          
                self.parametrs_of_build.count_women             = build.womens        
                // self.parametrs_of_build.count_children          =  build. children    
                self.parametrs_of_build.time_guests             =  build.time_average       
                self.parametrs_of_build.count_sink              =  build.count_crane        
                self.parametrs_of_build.height_basement         =  build.height_floor   

        
              
               
                    





                //general
                set_input(self, "general", 0, build.name)
                set_input(self, "general", 1, build.floors)
                set_input(self, "general", 2, build.len_a)
                set_input(self, "general", 3, build.len_b)
                set_input(self, "general", 4, build.len_sum)
                set_input(self, "general", 5, build.height)
                set_input(self, "general", 6, build.temp_inside)
                set_input(self, "general", 7, build.temp_outside)
                set_date(self, "general", 0, build.date_build)


                if ("id_reliability" in build) {
                    console.log("reliability")

                    let ihp = build.ihp == 0
                    if (build.ihp == 0) ihp = 'ИТП'
                    else ihp = 'Элеватор'

                    //reliability
                    set_r_btn(self, "reliability:0", ihp)
                    set_select_with_name(self, "reliability:0", 0, pumps, "id_pump", build.id_pump)
                    set_select_with_name(self, "reliability:0", 1, heatexchangers, "id_heatexchanger", build.id_heatexchanger)
                    set_c_box(self, "reliability:0", 0, "ventsys" in build && build.ventsys == 1)

                    if (build.ventsys) {
                        set_input(self, "reliability:1", 0, build.readings_vents.length)

                        // ждём обновления массива
                        self.$nextTick(function () {
                            build.readings_vents.forEach(function (item, index) {
                                set_input(self, "reliability:1", index + 1, item)
                            })
                        }
                        )
                    }
                    set_input(self, "reliability:2", 0, build.ascents_hws)
                    set_input(self, "reliability:2", 1, build.descents_hws)
                    set_input(self, "reliability:2", 2, build.count_crane)

                    set_input(self, "reliability:3", 0, build.ascents_heat)
                    set_input(self, "reliability:3", 1, build.descents_heat)
                    set_input(self, "reliability:3", 2, build.count_radiator)

                    set_select_with_name(self, "reliability:4", 0, shutoffvalves, "id_shutoffvalve", build.id_shutoffvalve)
                    set_select_with_name(self, "reliability:4", 1, pipes, "id_pipe", build.id_pipe)
                    set_select_with_name(self, "reliability:4", 2, radiators, "id_radiator", build.id_radiator)
                    set_select_with_name(self, "reliability:4", 3, cranes, "id_crane", build.id_crane)
                }
                else {
                    
                    set_select_variants(self, "reliability:0", 0, pumps, "id_pump")
                    set_select_variants(self, "reliability:0", 1, heatexchangers, "id_heatexchanger")

                    set_select_variants(self, "reliability:4", 0, shutoffvalves, "id_shutoffvalve")
                    set_select_variants(self, "reliability:4", 1, pipes, "id_pipe")
                    set_select_variants(self, "reliability:4", 2, radiators, "id_radiator")
                    set_select_variants(self, "reliability:4", 3, cranes, "id_crane")
                    console.log("skip reliability")
                }

                // Блок heat_los_win
                if ("id_q_wnd" in build) {
                    set_input(self, "heat_los_win", 0, build.count_windows)
                    set_input(self, "heat_los_win", 1, build.length_wnd)
                    set_input(self, "heat_los_win", 2, build.height_wnd)
                    set_input(self, "heat_los_win", 3, build.temp_inside)
                    set_input(self, "heat_los_win", 4, build.temp_outside)


                    set_select_with_name(self, "heat_los_win", 0, windows, "id_window", build.id_window) 
                    set_date(self, "heat_los_win", 0, build.date_wnd)
                } else {
                    set_select_variants(self, "heat_los_win", 0, windows, "id_window")
                }


                // Блок inf_win
                if ("id_q_wnd" in build) {
                     set_input(self, "inf_win", 0, build.count_windows)
                     set_input(self, "inf_win", 1, build.length_wnd)
                     set_input(self, "inf_win", 2, build.height_wnd)
                     set_input(self, "inf_win", 3, build.temp_inside)
                     set_input(self, "inf_win", 4, build.temp_outside)
                     
                     set_select_variants(self, "inf_win", 0, windows, "id_window")
                     set_select_with_name(self, "inf_win", 0, windows, "id_window", build.id_window)
                     set_date(self, "inf_win", 0, build.date_wnd)
                } else {
                    set_select_variants(self, "inf_win", 0, windows, "id_window")
                }

                // Блок heat_los_inpgr
                if ("id_q_floor" in build) {
                    set_input(self, "heat_los_inpgr", 0, build.q_doors_count_doors)
                    set_input(self, "heat_los_inpgr", 1, build.length_door)
                    set_input(self, "heat_los_inpgr", 2, build.height_door)
                    set_input(self, "heat_los_inpgr", 3, build.floors)
                    set_input(self, "heat_los_inpgr", 4, build.height)
                    set_input(self, "heat_los_inpgr", 5, build.temp_inside)
                    set_input(self, "heat_los_inpgr", 6, build.temp_outside)
                
                    set_select_with_name(self, "heat_los_inpgr", 0, doors, "id_door", build.id_door)
                    set_date(self, "heat_los_inpgr", 0, build.date_doors)
                } else {
                    set_select_variants(self, "heat_los_inpgr", 0, doors, "id_door")
                }

                // Блок inf_inpgr
                if ("id_q_floor" in build) {
                     set_input(self, "inf_inpgr", 0, build.count_doors)
                     set_input(self, "inf_inpgr", 1, build.length_door)
                     set_input(self, "inf_inpgr", 2, build.height_door)
                     set_input(self, "inf_inpgr", 3, build.floors)
                     set_input(self, "inf_inpgr", 4, build.height)
                     set_input(self, "inf_inpgr", 5, build.temp_inside)
                     set_input(self, "inf_inpgr", 6, build.temp_outside)

                     set_select_variants(self, "inf_inpgr", 0, doors, "id_door")
                     set_select_with_name(self, "inf_inpgr", 0, doors, "id_door", build.id_door)
                     set_date(self, "inf_inpgr", 0, build.date_doors)
                } else {
                    set_select_variants(self, "inf_inpgr", 0, doors, "id_door")
                }

                // Блок heat_los_heatcond_benv
                if ("id_q_construct_roof" in build) {
                    set_input(self, "heat_los_heatcond_benv", 0, build.temp_inside)
                    set_input(self, "heat_los_heatcond_benv", 1, build.temp_outside)
                    set_input(self, "heat_los_heatcond_benv", 2, build.len_a)
                    set_input(self, "heat_los_heatcond_benv", 3, build.len_b)
                    set_input(self, "heat_los_heatcond_benv", 4, build.floors)
                    set_input(self, "heat_los_heatcond_benv", 5, build.height)
                    set_input(self, "heat_los_heatcond_benv", 6, build.count_windows)
                    set_input(self, "heat_los_heatcond_benv", 7, build.length_wnd)
                    set_input(self, "heat_los_heatcond_benv", 8, build.height_wnd)
                    set_input(self, "heat_los_heatcond_benv", 9, build.q_doors_count_doors)
                    set_input(self, "heat_los_heatcond_benv", 10, build.length_door)
                    set_input(self, "heat_los_heatcond_benv", 11, build.height_door)
                    
                    set_select_with_name(self, "heat_los_heatcond_benv", 0, energoeffs, "id_energoeff", build.constructs_energoeff)
                } else {
                    set_select_variants(self, "heat_los_heatcond_benv", 0, energoeffs, "id_energoeff")
                }

                // Блок heat_los_heatcond_roof
                if ("id_q_construct_roof" in build) {
                    set_input(self, "heat_los_heatcond_roof", 0, build.temp_inside)
                    set_input(self, "heat_los_heatcond_roof", 1, build.temp_outside)
                    set_input(self, "heat_los_heatcond_roof", 2, build.len_a)
                    set_input(self, "heat_los_heatcond_roof", 3, build.len_b)
                    
                    set_select_with_name(self, "heat_los_heatcond_roof", 0, energoeffs, "id_energoeff", build.roof_energoeff)
                } else {
                    set_select_variants(self, "heat_los_heatcond_roof", 0, energoeffs, "id_energoeff")
                }

                // Блок heat_los_floor
                if ("id_q_floor" in build) {
                    console.log("Q_floor")
                    set_input(self, "heat_los_floor", 0, build.height_floor)
                    set_input(self, "heat_los_floor", 1, build.temp_inside)
                    set_input(self, "heat_los_floor", 2, build.temp_outside)
                    set_input(self, "heat_los_floor", 3, build.len_a)
                    set_input(self, "heat_los_floor", 4, build.len_b)
                    set_input(self, "heat_los_floor", 5, build.len_sum)
                }
                else {
                    console.log("skip Q_floor")
                }

                //ВРЕМЕННО????????
                let cond = true
                // Блок heat_los_vent
                if (cond) {
                    set_input(self, "heat_los_vent", 0, build.temp_inside)
                    set_input(self, "heat_los_vent", 1, build.temp_outside)
                    set_input(self, "heat_los_vent", 2, build.len_a)
                    set_input(self, "heat_los_vent", 3, build.len_b)
                    set_input(self, "heat_los_vent", 4, build.height)

                } else {
                    console.log("skip heat_los_vent")
                }


                // Блок add_heatcosts
                if ("id_q_reheat" in build) {
                    console.log("Q_reheating")

                    set_input(self, "add_heatcosts:0", 0, build.count_doors)
                    set_input(self, "add_heatcosts:0", 1, build.count_shkaf)
                    set_input(self, "add_heatcosts:0", 2, build.count_divan)
                    set_input(self, "add_heatcosts:0", 3, build.count_table)
                    set_input(self, "add_heatcosts:0", 4, build.count_shkafchik)
                    set_input(self, "add_heatcosts:0", 5, build.floors)
                    set_input(self, "add_heatcosts:0", 6, build.len_a)
                    set_input(self, "add_heatcosts:0", 7, build.len_b)
                    set_input(self, "add_heatcosts:0", 8, build.len_sum)
                    set_input(self, "add_heatcosts:0", 9, build.height)

                    set_select_with_name(self, "add_heatcosts:1", 0, periods, "id_period", build.id_period)

                    set_select_with_name(self, "add_heatcosts:2", 0, materials, "id_material", build.walls_material)
                    set_select_with_name(self, "add_heatcosts:2", 1, materials, "id_material", build.floors_materials)
                    set_select_with_name(self, "add_heatcosts:2", 2, materials, "id_material", build.doors_material)
                    set_select_with_name(self, "add_heatcosts:2", 3, materials, "id_material", build.mebel_material)
                    set_select_with_name(self, "add_heatcosts:2", 4, materials, "id_material", build.divan_material)

                    set_select_with_name(self, "add_heatcosts:2", 5, materials, "id_material", build.table_material)
                    set_select_with_name(self, "add_heatcosts:2", 6, materials, "id_material", build.shkafchik_material)

                }
                else {
                    console.log("skip Q_reheating")
                    set_select_variants(self, "add_heatcosts:1", 0, periods, "id_period")

                    set_select_variants(self, "add_heatcosts:2", 0, materials, "id_material")
                    set_select_variants(self, "add_heatcosts:2", 1, materials, "id_material")
                    set_select_variants(self, "add_heatcosts:2", 2, materials, "id_material")
                    set_select_variants(self, "add_heatcosts:2", 3, materials, "id_material")
                    set_select_variants(self, "add_heatcosts:2", 4, materials, "id_material")

                    set_select_variants(self, "add_heatcosts:2", 5, materials, "id_material")
                    set_select_variants(self, "add_heatcosts:2", 6, materials, "id_material")
                }

                // Блок heat_gains_people
                if ("id_q_peoples" in build) {
                    console.log("Q_people")
                    set_input(self, "heat_gains_people", 0, build.mens)
                    set_input(self, "heat_gains_people", 1, build.womens)
                    set_input(self, "heat_gains_people", 2, build.children)    //!!!!!!!!!!!!!!!!!!!!!
                    set_input(self, "heat_gains_people", 3, build.time_average)
                    set_input(self, "heat_gains_people", 4, build.temp_inside)
                } else {
                    console.log("skip Q_people")
                }

                // Блоки без проверок heat_gains_washstands heat_gains_showers VREMENNO!!!!!!!
                
                if (cond){
                    set_input(self, "heat_gains_washstands", 0, build.mens)
                    set_input(self, "heat_gains_washstands", 1, build.womens)
                    
                    set_input(self, "heat_gains_showers", 0, build.mens)
                    set_input(self, "heat_gains_showers", 1, build.womens)  

                    
                    set_input(self, "heat_gains_GVS", 0, build.temp_outside)
                    set_input(self, "heat_gains_GVS", 1, build.len_a)
                    set_input(self, "heat_gains_GVS", 2, build.len_b)
                    set_input(self, "heat_gains_GVS", 3, build.floors)
                    set_input(self, "heat_gains_GVS", 4, build.height)
                    set_input(self, "heat_gains_GVS", 5, build.count_crane)
                    //set_input(self, "heat_gains_GVS", 6, build.descents_hws)
                    set_select_with_name(self, "heat_gains_GVS", 0, pipes, "id_pipe", build.id_pipe)

                    set_input(self, "heat_gains_pipelines", 0, build.temp_outside)
                    set_input(self, "heat_gains_pipelines", 1, build.len_a)
                    set_input(self, "heat_gains_pipelines", 2, build.len_b)
                    set_input(self, "heat_gains_pipelines", 3, build.floors)
                    set_input(self, "heat_gains_pipelines", 4, build.height)
                    set_input(self, "heat_gains_pipelines", 5, build.count_windows)
                    //set_input(self, "heat_gains_pipelines", 6, build.descents_heat)  
                    set_select_with_name(self, "heat_gains_pipelines", 0, pipes, "id_pipe", build.id_pipe)
                }



                // Блок heat_gains_electriclighting
                if ("id_q_elec" in build) {
                    set_input(self, "heat_gains_electriclighting", 0, build.len_a)
                    set_input(self, "heat_gains_electriclighting", 1, build.len_b)
                    set_input(self, "heat_gains_electriclighting", 2, build.floors)
           
                    if (build.elec_consumption_by_period === null) {
                        set_c_box(self, "heat_gains_electriclighting", 0, true)
                    } else {
                        set_c_box(self, "heat_gains_electriclighting", 0, false)
                        set_input(self, "heat_gains_electriclighting", 3, build.elec_consumption_by_period)
                    }
                } else {
                    console.log("skip Q_elec")
                }
                return result_func(self, { "fail": false })
            }
            catch (error) {
                    return result_func(self, { "fail": true, text: "ошибка загрузки с сервера" })
            }
        })
        .fail(function() {
            return result_func(self, {"fail": true, text: "ошибка загрузки с сервера"})
        });
    } 
    catch (error) {
        return result_func(self, {"fail": true, text: "ошибка загрузки с сервера"})
    }
}




let load_funcs = {};
load_funcs.load_build = load_build


export default load_funcs