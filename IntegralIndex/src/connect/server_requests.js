import $ from 'jquery'

//let server_url = "http://127.0.0.1:5000"
let server_url = window.location.href + "api"
//дефотная проверка результата запроса
//возвращает {"fail": true, "error": "connect"} - ошибка соединения/код 500
//возвращает {"fail": true, "error": "server", "response": ответ сервера} - ответ "succsess" false сервера
//возвращает {"fail": false, "response": ответ сервера} - "succsess" true сервера
function default_check(result/*, self*/){     // , self)
    if(result.fail){
        return {"fail": true, "error": "connect"}
    }
    else if(!result.response.success){
        // Ошибка авторизации
        if (result.response.error == "401") {
            window.location.href = "/"
            throw ""
        } else {
            return {"fail": true, "error": "server", "response": result.response.result}
        }
    }
    return {"fail": false, "result": result.response.result}
}

//type - тип запроса
//url - url
//json_flag - данные json/нет
//auth_flag - с аутентификацией/без
//async_flag - синхронно/асинзронно
//data - данные, null - без них
function gen_ajax(type, url, json_flag, auth_flag, async_flag, data = null){
    let params 
    if(url =="") {
        params = {
            type: type,
            url: server_url,
            async: async_flag
        }
    }
    else {
        params = {
            type: type,
            url: server_url + "api" + url,
            async: async_flag
        }
    }
    if(auth_flag){
        params.headers = {Authorization: " Bearer " + localStorage.getItem("token")}
    }
    if(json_flag){
        params.contentType =  "application/json"
        params.dataType = "json"
    }
    if(data !== null){
        if(params.contentType ==  "application/json")
        {
            //console.log( JSON.stringify(data))
            params.data = JSON.stringify(data)
        }
        else{
            params.data = data
        }
    }
    return $.ajax(params)
}

//синхронный default запрос
//type - тип запроса
//url - url
//json_flag - данные json/нет
//auth_flag - с аутентификацией/без
//data - данные, null - без них
//возвращает {"fail": true} - ошибка соединения/код 500
//возвращает {"fail": false, "response": ответ сервера} - ответ сервера
function default_sync_ajax_request(type, url, json_flag, auth_flag, data = null){
    let result = ""
    gen_ajax(type, url, json_flag, auth_flag, false, data)
    .done(function(response) {
        result = {"fail": false, "response": response}
    }).fail(function() {
        result = {"fail": true}
    });
    return result
}

//СИНХРОННЫЙ default запрос POST к серверу по url с json data на входе и json на выходе,  ***без авторизации через токен
function sync_json_post_auth_free(url, data){
    return default_sync_ajax_request("POST", url, true, false, data)
}

//СИНХРОННЫЙ default запрос POST к серверу по url с json data на входе и json на выходе, с доп обработкой ***без авторизации через токен
function default_spost_request_auth_free(url, data, self){        // , self)
    return default_check(sync_json_post_auth_free(url, data), self)       // , self)
}

//СИНХРОННЫЙ default запрос POST к серверу по url с json data на входе и json на выходе,
function sync_json_post(url, data){
    return default_sync_ajax_request("POST", url, true, true, data)
}

//СИНХРОННЫЙ default запрос POST к серверу по url с json data на входе и json на выходе, с доп обработкой
function default_spost_request(url, data, self){       // , self)
    return default_check(sync_json_post(url, data), self)       // , self)
}

//СИНХРОННЫЙ default запрос GET к серверу по url с json на выходе,
function sync_json_get(url){
    return default_sync_ajax_request("GET", url, false, true, null)
}

//СИНХРОННЫЙ default запрос GET к серверу по url с json на выходе, с доп обработкой
function default_sget_request(url, self){       // , self)
    return default_check(sync_json_get(url), self)       // , self)
}

//СИНХРОННЫЙ default запрос PUT к серверу по url с json data на входе и json на выходе,
function sync_json_put(url, data){
    return default_sync_ajax_request("PUT", url, true, true, data)
}

//СИНХРОННЫЙ default запрос PUT к серверу по url с json data на входе и json на выходе, с доп обработкой
function default_sput_request(url, data, self){       // , self)
    return default_check(sync_json_put(url, data), self)       // , self)
}

//АСИНХРОННЫЙ PROMISE запрос GET к серверу по url  на входе и json на выходе (промис),
async function async_json_promise_get(url){
    if (url == "") {
        return $.ajax({
            type: "GET",
            url: server_url,
            headers: {Authorization: " Bearer " + localStorage.getItem("token")},
            async: true
        })
    } else {
        return $.ajax({
            type: "GET",
            url: server_url + "api" + url,
            headers: {Authorization: " Bearer " + localStorage.getItem("token")},
            async: true
        })
    }
}

//функция проверки для результата async_json_promise_get (доп обработка)
function default_asget_promise_request_check(result, self){       // , self)
    return default_check({fail:false, response: result}, self)       // , self)
}


let requests = {};

requests.sync_json_post = sync_json_post
requests.sync_json_post_auth_free = sync_json_post_auth_free
requests.default_sget_request = default_sget_request
requests.sync_json_get = sync_json_get
requests.default_spost_request = default_spost_request
requests.default_spost_request_auth_free = default_spost_request_auth_free

requests.sync_json_put = sync_json_put
requests.default_sput_request = default_sput_request

requests.async_json_promise_get = async_json_promise_get
requests.default_asget_promise_request_check = default_asget_promise_request_check


export default requests