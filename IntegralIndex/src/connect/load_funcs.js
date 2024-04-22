import requests from '@/connect/server_requests'
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


function load_build(self, id_build, result_func){
    try {
        $.when(
            requests.async_json_promise_get('/data/build/' + id_build),
            requests.async_json_promise_get("/data/elements/shutoffvalve?" + $.param({name: '',id_shutoffvalve:''})),
            requests.async_json_promise_get("/data/elements/pipe?" + $.param({name: '',id_pipe:''})),
            requests.async_json_promise_get("/data/elements/radiator?" + $.param({name: '',id_radiator:''})),
            requests.async_json_promise_get("/data/elements/crane?" + $.param({name: '',id_crane:''})),
            requests.async_json_promise_get("/data/elements/heatexchanger?" + $.param({name: '',id_heatexchanger:''})),
            requests.async_json_promise_get("/data/elements/pump?" + $.param({name: '',id_pump:''})),
            requests.async_json_promise_get("/data/elements/window?" + $.param({name: '',id_window:''})),
            requests.async_json_promise_get("/data/elements/doors?" + $.param({name: '',id_door:''})),
            requests.async_json_promise_get("/data/elements/energoeff?" + $.param({name: '',id_energoeff:''})), 
            requests.async_json_promise_get("/data/elements/period?" + $.param({name: '',id_period:''})),
            requests.async_json_promise_get("/data/elements/material?" + $.param({name: '',id_material:''}))
        ).done(function (
            build_r 
        ) {
            try {
                let build = check_error(build_r, "build", self)       //, self)

                //ЗАГРУЗКА ПАРАМЕТРОВ ЗДАНИЯ (в меню настройки)
                self.parametrs_of_build.id_build                 = id_build
                self.parametrs_of_build.name_build               = build.name
                self.parametrs_of_build.floors                   = build.floors
                self.parametrs_of_build.length_build             = build.len_a      
                self.parametrs_of_build.width_build              = build.len_b      
                self.parametrs_of_build.length_wall              = build.len_sum        
                self.parametrs_of_build.height_wall              = build.height       
                self.parametrs_of_build.temp_inside              = build.temp_inside        
                self.parametrs_of_build.temp_outside             = build.temp_outside      
                self.parametrs_of_build.date_construction        = build.date_build
                self.parametrs_of_build.count_windows            = build.count_windows      
                self.parametrs_of_build.length_windows           = build.length_wnd    
                self.parametrs_of_build.height_windows           = build.height_wnd    
                self.parametrs_of_build.date_windows             = build.date_wnd       
                self.parametrs_of_build.type_windows             = build.id_window      
                self.parametrs_of_build.count_doors              = build.q_doors_count_doors       
                self.parametrs_of_build.length_doors             = build.length_door       
                self.parametrs_of_build.height_doors             = build.height_door       
                self.parametrs_of_build.type_doors               = build.id_door         
                self.parametrs_of_build.date_doors               = build.date_doors         
                self.parametrs_of_build.class_energoeff          = build.constructs_energoeff    
                self.parametrs_of_build.count_closet             = build.count_shkaf       
                self.parametrs_of_build.count_sofa               = build.count_divan         
                self.parametrs_of_build.count_table              = build.count_table        
                self.parametrs_of_build.count_small_closet       = build.count_shkafchik 
                self.parametrs_of_build.count_men                = build.mens          
                self.parametrs_of_build.count_women              = build.womens        
                // self.parametrs_of_build.count_children           =  build. children    
                self.parametrs_of_build.time_guests              =  build.time_average       
                self.parametrs_of_build.count_sink               =  build.count_crane        
                self.parametrs_of_build.height_basement          =  build.height_floor
                 
                self.parametrs_of_build.period_energosave        =  build.id_period     
                self.parametrs_of_build.walls_material           =  build.walls_material
                self.parametrs_of_build.floors_material          =  build.floors_materials
                self.parametrs_of_build.doors_material           =  build.doors_material 
                self.parametrs_of_build.furniture_material       =  build.mebel_material
                self.parametrs_of_build.sofa_material            =  build.divan_material
                self.parametrs_of_build.table_material           =  build.table_material
                self.parametrs_of_build.type_pipe                =  build.id_pipe          
               
                //ЗАГРУЗКА ПАРАМЕТРОВ ДЛЯ НАДЕЖНОСТИ
                self.parametrs_of_reliability.id_build            =  id_build
                self.parametrs_of_reliability.elev_itp            =  build.ihp 
                self.parametrs_of_reliability.ventsys             =  build.ventsys
                self.parametrs_of_reliability.count_installations =  build.ventsys? build.readings_vents.length : ''
                self.parametrs_of_reliability.length_pipe1        =  build.ventsys? build.readings_vents[0] : ''
                self.parametrs_of_reliability.length_pipe2        =  build.ventsys? build.readings_vents[1] : ''
                self.parametrs_of_reliability.count_up_hws        =  build.ascents_hws
                self.parametrs_of_reliability.count_down_hws      =  build.descents_hws
                self.parametrs_of_reliability.count_crane         =  build.count_crane
                self.parametrs_of_reliability.count_up_loft       =  build.ascents_heat
                self.parametrs_of_reliability.count_down_loft     =  build.descents_heat
                self.parametrs_of_reliability.count_radiator      =  build.count_radiator
                self.parametrs_of_reliability.type_armature       =  build.id_shutoffvalve   
                self.parametrs_of_reliability.type_radiator       =  build.id_radiator
                self.parametrs_of_reliability.type_crane          =  build.id_crane
                self.parametrs_of_reliability.type_pipe           =  build.id_pipe
                self.parametrs_of_reliability.type_pump           =  build.id_pump
                self.parametrs_of_reliability.type_heatexchanger  =  build.id_heatexchanger

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