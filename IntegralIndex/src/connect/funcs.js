import requests from '@/connect/server_requests'
import id_mappers from '@/connect/id_mappers'
import load_funcs from '@/connect/load_funcs'
import export_funcs from './export_funcs'

import $ from 'jquery'
let server_url = "http://127.0.0.1:5000"

function start(self){       // ,self)
    if (localStorage.getItem("this_build_id") === null) {
        let result = requests.default_sget_request("/data/build/test?" + $.param({id_build:''}), self)       // ,self)
        if(result['fail']){
            if(result['error'] == 'connect'){
                alert("get_from_server: fail connect")
            }
            else{
                alert("get_from_server: error: " + result['error'])
            }
            throw "";
        }
        else {
            localStorage.setItem("this_build_id",  result["result"]["id_build"])
        }
    }
}

function load_result_func(self, result) {
    if(result.fail){
        if(self.check_loadpat){
            self.loadpat_error.text = 'Ошибка загрузки с сервера'
            self.loadpat_error.show = true
        }
        else{
            alert("ошибка загрузки с сервера")
        }
    }
    else{
        //успех
        if(self.check_loadpat){
            self.check_loadpat = false
            self.loadpat_error.text = ''
            self.loadpat_error.show = false
        }
    }
}

function load(self){
    let id_build = localStorage.getItem("this_build_id");
    load_funcs.load_build(self, id_build, load_result_func)
}

function import_from_server(self){
    let id_build = ''
    self.load_pat.select.variants.forEach(function(item, index){
        if(item == self.load_pat.select.picked){
            id_build = self.load_pat.select.ids[index]
            return false
        }
    })
    if(id_build === ''){
        console.log('import picked error')
    }
    else{
        console.log('import')
        console.log(id_build)
        console.log(self.load_pat.select.picked)
        load_funcs.load_build(self, id_build, load_result_func)
        localStorage.setItem("this_build_id", id_build);
    }
}

function export_error_alert(self, error = null){
    if(error === null){
        self.savepat_error.text = ''
        self.savepat_error.show = false
    }
    else{
        self.savepat_error.text = error
        self.savepat_error.show = true
    }
}

function exportf(self, full, to_server, f){
    let export_build_r = export_funcs.export_build(self, full)
    if(export_build_r.error){
        export_error_alert(self,export_build_r.text)
    }
    else {
        export_error_alert(self,null)
        if(to_server){
            console.log("to_server")
            let result = requests.default_sput_request("/data/build", export_build_r.result, self)       // ,self)
            if(result.fail){
                if(result.error == 'connect'){
                    export_error_alert(self,"Ошибка подключения к серверу")
                }
                else{
                    export_error_alert(self,"Ошибка выполнения операции")
                }
            }
            else {
                //успех
                load_funcs.load_build(self,  result.result.id_build, function(self,result1){
                    if(result1.fail){
                        export_error_alert(self,"ошибка выгрузки загруженного шаблона")
                    }
                    else{
                        //успех
                        localStorage.setItem("this_build_id", result.result.id_build);
                        self.check_savepat = false
                        self.dialog_buttons_check = false
                        if (f !== undefined){
                            f(self)
                        }
                    }
                })
            }
        }
        else{
            console.log("export deb")
            console.log(export_build_r.result)
            self.check_savepat = false
            // let blob = new Blob([JSON.stringify(build)], {type: "text/plain"});
            // let link = document.createElement("a");
            // link.setAttribute("href", URL.createObjectURL(blob));
            // link.setAttribute("download", "build.json");
            // link.click();
        }
    }
}




function calc(id, self){       
    console.log("calc")
    console.log(self)
    let export_build_r = export_funcs.export_build(self, false);
    if(export_build_r.error){
        
        export_error_alert(self,export_build_r.text)
        return "ошибка вычислений, проверьте наличие данных и их корректность"
    }
    else {
        export_error_alert(self,null)
        console.log("to_server")
            let result = requests.default_sput_request("/data/cur_build", export_build_r.result, self)       // ,self)
            if(result.fail){
                if(result.error == 'connect'){
                    export_error_alert(self,"Ошибка подключения к серверу")
                }
                else{
                    export_error_alert(self,"Ошибка выполнения операции")
                }
            }else{
                let id_build = localStorage.getItem("this_build_id");
                let result = requests.default_spost_request(id_mappers.calc_map[id],{"id":id_build}, self)       // ,self)
                if(result['fail']){
                    if(result['error'] == 'connect'){
                        return "ошибка подключения к серверу"
                    }
                    else{
                        console.log(result)
                        return "ошибка вычислений, проверьте наличие данных и их корректность"
                    }
                }
                else {
                    return id_mappers.calc_result_map[id](result["result"])
                }
            }
    }    
}

//
function check_token_before_render(data){
    let flag = true
    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: server_url + "/check_token_for_server",
        async: false,
        data: JSON.stringify(data),
        dataType: "json"
    })
    .done(function(response) {      // если пришел валидный токен
        if (response.success) {
            flag = true
        } else {
            flag = false
            //alert("Кажется вы не авторизовались, мы перенаправим вас на страницу входа")
        }
    }).fail(function() {
        alert("ошибка подключения к серверу")
    });

    return flag
}



let funcs = {};
funcs.start = start
funcs.calc = calc
funcs.export = exportf
funcs.load = load
funcs.import = import_from_server
funcs.check_token_before_render = check_token_before_render

export default funcs