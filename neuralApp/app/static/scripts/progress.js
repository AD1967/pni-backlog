function AnalyzeProgress(json_data)
{
    console.log(json_data)
    //var parsed_data = JSON.parse(json_data)
    parsed_data = json_data
    console.log(parsed_data)
    if (parsed_data.mode == "True")
    {
        console.log("Занят")
        div.textContent = "В данный момент сервер ЗАНЯТ обучением модели " + parsed_data.name
        setTimeout(CheckProgress, 1000)
    }
    else
    {
        console.log("Не занят")
        div.textContent = "В данный момент сервер НЕ ЗАНЯТ обучением модели"
        window.alert("Обучение завершено")
        window.location.replace("/")
    }
}

function CheckProgress()
{
    var url = "127.0.0.1:5000/progress_info"
    fetch("/progress_info").then(res => {console.log(res); var new_res = res.json(); console.log(new_res); return new_res}).then(out => {console.log(out); AnalyzeProgress(out)}).catch(err => {throw err})
}

var div = document.getElementById("progress-screen");
setTimeout(CheckProgress, 1000);