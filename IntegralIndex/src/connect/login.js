import requests from '@/connect/server_requests'
import $ from 'jquery'

let server_url = "http://127.0.0.1:5000"

function enter(self) {
    let user_login = self.login_
    let user_psw = self.psw

    if (user_login == "" || user_psw == ""){
        self.Flag = true
        self.login_ = ""
        self.psw = "" 
    } else {
        self.Flag = false
    }


    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: server_url + "/tokens",
        async: false,
        // До отправки отсылаем логин и пароль для verify_password
        // Это делается только один раз при входе, затем для аутентификации бедт посылаться только токен
        beforeSend: function (xhr) {
            xhr.setRequestHeader ("Authorization", "Basic " + btoa(user_login + ":" + user_psw));
        },

    })
    .done(function(response) {
        if (!response.success) {
            console.log("Некорректные данные при входе")
            if (!self.Flag){
                self.Flag2 = true
            } else {
                self.Flag2 = false
            }
        } else {
            self.Flag2 = false
            // После успешной авторизации сервер выдает токен, который мы сохраняем в лок хранилище
            // для дальнейшей отправке с запросами
            localStorage.setItem("token", response["result"])
            window.location.href = "/"
            self.hide_dialog()
        }
    }).fail(function() {
        alert("ошибка подключения к серверу")
    });

}

function logout() {
    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: "/logout",
        async: false,
        data: JSON.stringify({token : localStorage.getItem("token")}),
        dataType: "json"
    })
    // .done(function(response) {

    // }).fail(function() {

    // });

}

function registr(self) {
    let user_login = self.login_
    let user_psw = self.psw
    let user_psw_2 = self.psw2

    if (user_login == "" || user_psw == "" || user_psw_2 == ""){
        self.Flag = true
        self.login_ = ""
        self.psw = "" 
        self.psw2 = ""
    } else {
        self.Flag = false
    }

    if (user_psw != user_psw_2 && !self.Flag){
        self.Flag3 = true
        self.login_ = ""
        self.psw = "" 
        self.psw2 = ""
    } else {
        self.Flag3 = false
    }

    let result = requests.default_spost_request_auth_free( "/registration", {name: user_login, psw: user_psw, psw2: user_psw_2}, self)

    if(result['fail']){
        if(result['error'] == 'connect'){
            alert("registr: fail connect")
        }
        else{
            //alert("registr: Некорректные данные")
            console.log("Некорректные данные при регистрации")
            if (!self.Flag && !self.Flag3){
                self.Flag2 = true
            } else {
                self.Flag2 = false
            }
        }
    }
    else {
        //alert("registr: Вы успешно зарегистрировались")
        self.hide_dialog();
        self.$emit('update:show', [true, false])
    }
}

let login_funcs = {};
login_funcs.enter = enter
login_funcs.logout = logout
login_funcs.registr = registr

export default login_funcs