import requests from '@/connect/server_requests'
import {isProd} from '@/connect/server_requests'
import id_mappers from '@/connect/id_mappers'
import load_funcs from '@/connect/load_funcs'
import export_funcs from './export_funcs'

import $ from 'jquery'
var server_url
if (isProd){
    server_url = window.location.href + "api"
}
else {
    server_url = "http://127.0.0.1:5000"
}

function start(self) {
    if (localStorage.getItem("this_build_id") === null) {
        let result = requests.default_sget_request("/data/build/test?" + $.param({ id_build: '' }), self)       // ,self)
        if (result['fail']) {
            if (result['error'] == 'connect') {
                alert("get_from_server: fail connect")
            }
            else {
                alert("get_from_server: error: " + result['error'])
            }
            throw "";
        }
        else {
            localStorage.setItem("this_build_id", result["result"]["id_build"])
        }
    }
}

function load_result_func(self, result) {
    if (result.fail) {
        if (self.check_loadpat) {
            self.loadpat_error.text = 'Ошибка загрузки с сервера'
            self.loadpat_error.show = true
        }
        else {
            alert("ошибка загрузки с сервера11")
        }
    }
    else {
        //успех
        if (self.check_loadpat) {
            self.check_loadpat = false
            self.loadpat_error.text = ''
            self.loadpat_error.show = false
        }
    }
}

function load(self) {
    let id_build = localStorage.getItem("this_build_id");
    load_funcs.load_build(self, id_build, load_result_func)
}

function import_from_server(self) {
    load_funcs.load_build(self, self.parametrs_of_build.id_build, load_result_func)
    localStorage.setItem("this_build_id", self.parametrs_of_build.id_build);
}

function calc(id, self, selectedYear) {
    self.showProgress = true;
    //основные расчеты
    let export_build_r = export_funcs.export_build(self)
    var result = requests.default_sput_request("/data/cur_build", export_build_r.result, self)

    if (!result.fail) {
        const startDate = id_mappers.yearsMap[selectedYear][0];
        const endDate = id_mappers.yearsMap[selectedYear][1];
        let currentDate = new Date(startDate);
        var mul = (startDate.getDate() ==  endDate.getDate()) ? 100 : 0.3663
        var res = {}
        var progress = 0;
        for (var index = currentDate; index <= endDate;  index.setDate(currentDate.getDate() + 1)) {
            progress +=1;
            let formattedDate = `${index.getFullYear()}-${String(index.getMonth() + 1).padStart(2, '0')}-${String(index.getDate()).padStart(2, '0')}`
            setTimeout(function(id,  self, progress, formattedDate){
                document.getElementById('loading_name').innerHTML = id_mappers.calc_name_map[id];
                document.getElementById('loading_calc').innerHTML = ((progress*mul).toFixed(3)!= 100)? "Прогресс расчета: " + (progress * mul).toFixed(3).toString() + " %" : "";
                self.showProgress = ((progress*mul).toFixed(3)!= 100)
                let result = requests.default_spost_request(id_mappers.calc_map[id], { "cur_date": formattedDate }, self);
                if (!result['fail']) {
                    for (var key1 in result["result"]) { 
                        res[key1] = (key1 in res)? res[key1] + result["result"][key1] : result["result"][key1]   
                    }      
                }    
            }, 10, id, self, progress, formattedDate)
        }
    }
    setTimeout(function(res, self){
        //сохранение
        for (var key2 in res) {
            self.results[key2] = res[key2];
        }
        //доп вычисления
        self.calc_dop_results();
        self.showResults = true;
    }, 10, res, self)
    
}

function calc_reliability(parametrs_of_reliability) {
    let self = this
    let url = id_mappers.calc_map['reliability'];
    let result = requests.default_spost_request(url, parametrs_of_reliability, self)
    if (result['fail']) {
        console.log('Результат запроса - надежность', result, " и", result.error)
        return ["error", "error"]
    }
    else {
        console.log('Результат запроса - надежность', result, " и", result.result)
        return [result.result, result.result];
    }
}

function calc_ner(model) {
    let self = this
    let result = requests.default_spost_request("/calc_ner", {"model": model}, self)
    console.log(result)
    return result.result
}

//
function check_token_before_render(data) {
    let flag = true
    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: server_url + "/check_token_for_server",
        async: false,
        data: JSON.stringify(data),
        dataType: "json"
    })
        .done(function (response) {      // если пришел валидный токен
            if (response.success) {
                flag = true
            } else {
                flag = false
                //alert("Кажется вы не авторизовались, мы перенаправим вас на страницу входа")
            }
        }).fail(function () {
            alert("ошибка подключения к серверу")
        });

    return flag
}



function download_excel() {
    const fetch = require('node-fetch');
    let url = server_url + '/download'
    console.log('url download', url)

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

function save_cur(parametrs_of_build, results, dop_results) {
    const fetch = require('node-fetch');

    let url = server_url + '/save_cur'
    console.log('url save cur', url)

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': " Bearer " + localStorage.getItem("token")
        },
        body: JSON.stringify({ parametrs_of_build, results, dop_results })
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
funcs.calc_ner = calc_ner
export default funcs

