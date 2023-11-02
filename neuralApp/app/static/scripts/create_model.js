/* <div id="layer-1">
        <p><label for="choose-hidden-layer-1">Тип скрытого слоя 1:</label></p>
        <p>
            <select name="choose-hidden-layer-1" id="choose-hidden-layer-1">
                <option value="Dense">Dense</option>
             </select>
         </p>

        <p><label for="hidden-units-1">Число узлов в скрытом слое 1:</label></p>
        <p><input type="text" name="hidden-units-1" id="hidden-units-1" autocomplete="off"></p>

        <p><label for="choose-activation-1">Выберите функцию активации 1:</label></p>
        <p>
            <select name="choose-activation-1" id="choose-activation-1">
                <option value="linear">linear</option>
                <option value="relu">relu</option>
                <option value="sigmoid">sigmoid</option>
                <option value="tanh">tanh</option>
            </select>
         </p>
    </div>
*/
function ConstructLayer(number)
{
    let newLayer = layers.children.item(layers.children.length - 1).cloneNode(true);
    console.log(newLayer);
    newLayer.setAttribute("id", "layer-" + number);

    let labels = newLayer.getElementsByTagName("label");
    labels[0].setAttribute("for", "choose-hidden-layer-" + number);
    labels[0].textContent = "Тип скрытого слоя " + number + ":";
    labels[1].setAttribute("for", "choose-hidden-units-" + number);
    labels[1].textContent = "Число узлов в скрытом слое " + number + ":";
    labels[2].setAttribute("for", "choose-activation-" + number);
    labels[2].textContent = "Выберите функцию активации " + number + ":";

    let selects = newLayer.getElementsByTagName("select");
    let prev_selects = layers.children.item(layers.children.length - 1).getElementsByTagName("select")
    selects[0].setAttribute("name", "choose-hidden-layer-" + number);
    selects[0].setAttribute("id", "choose-hidden-layer-" + number);
    selects[0].value = prev_selects[0].value;
    selects[1].setAttribute("name", "choose-activation-" + number);
    selects[1].setAttribute("id", "choose-activation-" + number);
    selects[1].value = prev_selects[1].value;

    let inputs = newLayer.getElementsByTagName("input");
    inputs[0].setAttribute("name", "hidden-units-" + number);
    inputs[0].setAttribute("id", "hidden-units-" + number);

    console.log(newLayer);

    return newLayer;
    //newLayer.firstChild
}

function ConstructFactor(number)
{
    let newFactor = factors.children.item(factors.children.length - 1).cloneNode(true);
    console.log(newFactor);
    newFactor.setAttribute("id", "factor-" + number);

    let labels = newFactor.getElementsByTagName("label");
    labels[0].setAttribute("for", "choose-factor-" + number);
    labels[0].textContent = "Столбец фактора " + number + ":";

    let inputs = newFactor.getElementsByTagName("input");
    inputs[0].setAttribute("name", "choose-factor-" + number);
    inputs[0].setAttribute("id", "choose-factor-" + number);
    inputs[0].required = !document.getElementById("dataset-settings-default").checked;

    console.log(newFactor);

    return newFactor;
    //newLayer.firstChild
}

function AddFactor()
{
    console.log("Adding")
    factors.appendChild(ConstructFactor(factors.children.length + 1))
    factorsCount = document.getElementById("factor-number")
    factorsCount.setAttribute("value", parseInt(factorsCount.getAttribute("value"), 10) + 1) 
    //ConstructLayer(layers.children.length + 1)
}

function RemoveFactor()
{
    console.log("Removing")
    if (factors.children.length != 1)
    {
        document.getElementById("factor-" + factors.children.length).remove()
        factorsCount = document.getElementById("factor-number")
        factorsCount.setAttribute("value", parseInt(factorsCount.getAttribute("value"), 10) - 1)
    }
}

function AddLayer()
{
    layers.appendChild(ConstructLayer(layers.children.length + 1))
    layersCount = document.getElementById("layers-number")
    layersCount.setAttribute("value", parseInt(layersCount.getAttribute("value"), 10) + 1) 
}

function RemoveLayer()
{
    if (layers.children.length != 1)
    {
        //layers.removeChild(document.querySelector("#layer-" + layers[layers.children.length - 1]))
        console.log("layer-" + layers.children.length)
        document.getElementById("layer-" + layers.children.length).remove()
        layersCount = document.getElementById("layers-number")
        layersCount.setAttribute("value", parseInt(layersCount.getAttribute("value"), 10) - 1)
    }
}

function UpdateFactorInputs()
{
    for (i = 0; i < factors.children.length; i++)
    {
        var inputs = factors.children.item(i).getElementsByTagName("input");
        inputs[0].required = !document.getElementById("dataset-settings-default").checked;
    }
    document.getElementById("choose-result").required = !document.getElementById("dataset-settings-default").checked;
}

function ShowProgress()
{
    for (i = 0; i < 50000; i++)
    {

    }
    console.log("Showing progress")
    var divCreate = document.getElementById("div-create-model")
    console.log(divCreate)
    console.log(divCreate.style.display)
    if (divCreate.style.display != "none")
    {
        divCreate.style.display = "none"
    }
    var divProgress = document.getElementById("div-training-progress")
    console.log(divProgress.style.display)
    if (divProgress.style.display != "block")
    {
        divProgress.style.display = "block"
    }
    fetch("/progress", { method: 'GET' }).then(response => response.text()).then(text => 
        {
            console.log(text)
            if (text == "True")
            {
                console.log("In if")
                divProgress.textContent = "Обучение в процессе"
                setTimeout(ShowProgress, 1000)
            }
            else
            {
                console.log("In else")
                divCreate.style.display = "block";
                divProgress.style.display = "none";
            }
        })
}

function AnalyzeProgress(json_data)
{
    console.log(json_data)
    //var parsed_data = JSON.parse(json_data)
    parsed_data = json_data
    console.log(parsed_data)
    if (parsed_data.mode == "True")
    {
        console.log("Занят")
        //window.location.replace("/progress")
    }
    else
    {
        setTimeout(CheckProgress, 1000)
    }
}

function CheckProgress()
{
    fetch("/progress_info")
    .then(res => {console.log(res); var new_res = res.json(); console.log(new_res); return new_res})
    .then(out => {console.log(out); AnalyzeProgress(out)})
    .catch(err => {throw err})
}

var errorDataset = false
var errorModel = false

function AnalyzeDatasets(json_data)
{
    console.log("Checking datasets names")
    console.log(json_data);
    let current_dataset_name = document.getElementById("upload-dataset-file-name").value;
    if (json_data.datasets.includes(current_dataset_name) && document.getElementById("upload-dataset-file").value != "")
    {
        console.log("Dataset name already exists")
        document.getElementById("error-dataset").style.display = "inline";
        errorDataset = true
    }
    else
    {
        document.getElementById("error-dataset").style.display = "none";
        errorDataset = false
    }
}

function AnalyzeModels(json_data)
{
    console.log("Checking model names")
    console.log("Models:", json_data.models);
    let current_model_name = document.getElementById("ann-model-name").value;
    console.log("Current name:", current_model_name);
    if (json_data.models.includes(current_model_name))
    {
        console.log("Model name already exists")
        document.getElementById("error-model").style.display = "inline";
        errorModel = true
    }
    else if (current_model_name == "")
    {
        console.log("Empty model name")
        document.getElementById("error-model").style.display = "inline";
        errorModel = true
    }
    else
    {
        document.getElementById("error-model").style.display = "none";
        errorModel = false
    }
}

async function FetchDatasets()
{
    let response = await fetch('/datasets');
    let json_obj = await response.json();
    //let json_obj = JSON.stringify(json);
    console.log(json_obj);
    return json_obj;
}

async function FetchModels()
{
    let response = await fetch('/models');
    let json_obj = await response.json();
    //let json_obj = JSON.stringify(json);
    console.log(json_obj);
    return json_obj;
}

async function ValidateForm(event)
{
    console.log("Validating form")
    /*
    var possibleColumns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", 
    "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN", "AO", "AP", "AQ", "AR", "AS", "AT", "AU", 
    "AV", "AW", "AX", "AY", "AZ"]
    
    var result_col = document.getElementById("choose-result")
    console.log(result_col.value)
    
    var flag = true
    flag = possibleColumns.includes(result_col.value)
    if (!flag)
    {
        event.preventDefault();
        window.alert("Поле целевого значения для обучающего набора заполнено неверно! Получено: " + result_col.value)
        console.log("Поле целевого значения для обучающего набора заполнено неверно! Получено: " + result_col.value);
        return false
    }
    else
    {
        possibleColumns.pop(result_col.value)
        return true
    }
    */

    console.log("Fetching datasets");
    let dataset_json = await FetchDatasets();
    AnalyzeDatasets(dataset_json)
    console.log("Error dataset:", errorDataset)

    // let fetcher = await fetch("/datasets");
    // let dataset_json = await fetcher.json();
    // AnalyzeDatasets(dataset_json);
    // .then(res => {console.log(res); var new_res = res.json(); console.log(new_res); return new_res})
    // .then(out => {console.log(out); AnalyzeDatasets(out)})
    // .catch(err => {throw err})

    console.log("Fetching models");
    let model_json = await FetchModels();
    AnalyzeModels(model_json)
    console.log("Error model:", errorModel)
    // fetcher = await fetch("/models");
    // let model_json = await fetcher.json();
    // AnalyzeDatasets(model_json);
    // .then(res => {console.log(res); var new_res = res.json(); console.log(new_res); return new_res})
    // .then(out => {console.log(out); AnalyzeModels(out)})
    // .catch(err => {throw err})

    if (errorDataset || errorModel)
    {
        window.alert("Ошибка");
        console.log("Error: dataset and/or model's name already exists");
        event.preventDefault();
        return false;
    }
    else
    {
        console.log("Dataset and model's names are correct");
        console.log("Redirecting");
        window.location.replace("/progress");
        return true;
    }
}

function RedirectProgress(event)
{
    event.preventDefault()
    console.log("Error values:", errorDataset, errorModel);
    if (errorDataset || errorModel)
    {
        console.log("No redirect, error");
        errorDataset = false;
        errorModel = false;
    }
    else
    {
        console.log("Redirecting");
        window.location.replace("/progress");
    }
}

async function ValidateDatasetName(event)
{

    let datasetNameInput = document.getElementById("upload-dataset-file-name");
    console.log("Fetching datasets");
    let dataset_json = await FetchDatasets();
    AnalyzeDatasets(dataset_json);
    if (errorDataset)
    {
        datasetNameInput.setCustomValidity("Имя набора данных уже занято");
    }
    else
    {
        datasetNameInput.setCustomValidity("");
    }
    console.log("Error dataset:", errorDataset);

}

async function ValidateModelName(event)
{

    let modelNameInput = document.getElementById("ann-model-name");
    console.log("Fetching models");
    let model_json = await FetchModels();
    AnalyzeModels(model_json);
    if (errorModel)
    {
        modelNameInput.setCustomValidity("Имя модели уже занято");
    }
    else
    {
        modelNameInput.setCustomValidity("");
    }
    console.log("Error model:", errorModel);
}

function UpdateFormatSetting()
{
    // TODO:
    // Get all divs with formats (and result)
    // Iterate, checking for new value
    // If not-empty then set setting to Custom
}

function UpdateFormat()
{
    console.log("Change display for format")
    if (document.getElementById("dataset-settings-custom").checked)
    {
        document.getElementById("dataset-format").style.display = "inline";
    }
    else
    {
        document.getElementById("dataset-format").style.display = "none";
    }
}

var layers = document.getElementById("layers");
var factors = document.getElementById("factors")

document.getElementById("button-add-layer").addEventListener("click", AddLayer);
document.getElementById("button-remove-layer").addEventListener("click", RemoveLayer);
document.getElementById("button-add-factor").addEventListener("click", AddFactor);
document.getElementById("button-remove-factor").addEventListener("click", RemoveFactor);
document.getElementById("dataset-settings-default").addEventListener("click", UpdateFactorInputs);
document.getElementById("dataset-settings-custom").addEventListener("click", UpdateFactorInputs);
//document.getElementById("submit-ann-model-to-train").addEventListener("click", ShowProgress);
document.getElementById("form-create").addEventListener('submit', ValidateForm, false);
//document.getElementById("form-create").addEventListener('submit', RedirectProgress);

//document.getElementById("form-create").addEventListener('submit', CheckProgress);
document.getElementById("upload-dataset-file-name").addEventListener("input", ValidateDatasetName);
document.getElementById("ann-model-name").addEventListener("input", ValidateModelName);

document.getElementById("choose-result").addEventListener("input", UpdateFormatSetting);
document.getElementById("choose-factor-1").addEventListener("input", UpdateFormatSetting);
document.getElementById("dataset-settings-default").addEventListener("click", UpdateFormat);
document.getElementById("dataset-settings-custom").addEventListener("click", UpdateFormat);
