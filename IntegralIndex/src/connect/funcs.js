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
            alert("ошибка загрузки с сервера11")
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
    load_funcs.load_build(self, self.parametrs_of_build.id_build, load_result_func)
    localStorage.setItem("this_build_id", self.parametrs_of_build.id_build); 
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



function calc(id, self, selectedYear){       
    console.log("calc")
    let export_build_r = export_funcs.export_build(self)
    if (export_build_r.error){
        export_error_alert(self,export_build_r.text)
        //return "ошибка вычислений, проверьте наличие данных и их корректность"
        return [false, "error calc"]
    }
    else {
        export_error_alert(self,null)

        let result = requests.default_sput_request("/data/cur_build", export_build_r.result, self)
        if(result.fail){
            if(result.error == 'connect'){
                export_error_alert(self,"Ошибка подключения к серверу")
                return [false, "ошибка подключения к серверу"]
            }
            else{
                export_error_alert(self,"Ошибка выполнения операции")
                return [false, "error operation"]
            }
        }else{
            const startDate = id_mappers.yearsMap[selectedYear][0];
            const endDate = id_mappers.yearsMap[selectedYear][1];
            let currentDate = new Date(startDate);

            var res = {}
            while(currentDate <= endDate){
                let year = currentDate.getFullYear();
                let month = String(currentDate.getMonth() + 1).padStart(2, '0');
                let day = String(currentDate.getDate()).padStart(2, '0');
                let formattedDate = `${year}-${month}-${day}`;

                let result = requests.default_spost_request(id_mappers.calc_map[id], {"cur_date": formattedDate}, self)
                if(result['fail']){
                    if(result['error'] == 'connect'){
                        return [false, "ошибка подключения к серверу"]
                    }
                    else{
                        //return "ошибка вычислений, проверьте наличие данных и их корректность"
                        return [false, "error calc"]
                    }
                }
                else {
                    // console.log('from server ', result)
                    for (var key in result["result"]) {
                        if (key in res) {
                            res[key] += result["result"][key];
                        }
                        else {
                            res[key] = result["result"][key];
                        }
                    }
                    currentDate.setDate(currentDate.getDate() + 1);
                }
            }
        }
        console.log('Результат вычислений', res)
        return [true, res];
    }
}

function calc_reliability(parametrs_of_reliability) {
    let self = this
    let url = id_mappers.calc_map['reliability'];
    let result = requests.default_spost_request(url, parametrs_of_reliability, self)
    if(result['fail']){
        console.log('Результат запроса - надежность', result, " и" , result.error)
        return ["error", "error"]
    }
    else {
        console.log('Результат запроса - надежность', result, " и" , result.result)
        return [result.result, result.result];
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



function download_excel(){
    const fetch = require('node-fetch');
    let url = server_url + '/download'
    fetch(url, {
        method: 'POST',
        headers: {
            'Authorization': " Bearer " + localStorage.getItem("token")
        },
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        } else {
            throw new Error('Failed to download Excel file');
        }
    })
    .then(blob => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'formula_results.xlsx';
        document.body.appendChild(a);
        a.click();
        URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error(error);
    });
}

function save_cur(parametrs_of_build, results, dop_results){
    const fetch = require('node-fetch');

    let url = server_url + '/save_cur'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': " Bearer " + localStorage.getItem("token")
        },
        body: JSON.stringify({parametrs_of_build, results, dop_results })
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        } else {
            throw new Error('Failed to download Excel file');
        }
    })
    .then(blob => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'current_results.xlsx';
        document.body.appendChild(a);
        a.click();
        URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error(error);
    });
}

let funcs = {};
funcs.start = start
funcs.calc = calc
funcs.calc_reliability = calc_reliability
funcs.load = load
funcs.download_excel = download_excel
funcs.save_cur = save_cur
funcs.import = import_from_server
funcs.check_token_before_render = check_token_before_render
export default funcs

