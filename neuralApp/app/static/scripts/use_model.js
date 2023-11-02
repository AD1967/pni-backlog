function ConstructFactor(number)
{
    var newFactor = factors.children.item(0).cloneNode(true);
    console.log(newFactor);
    newFactor.setAttribute("id", "factor-" + number);

    var labels = newFactor.getElementsByTagName("label");
    labels[0].setAttribute("for", "choose-factor-" + number);
    labels[0].textContent = "Столбец фактора " + number + ":";

    var inputs = newFactor.getElementsByTagName("input");
    inputs[0].setAttribute("name", "choose-factor-" + number);
    inputs[0].setAttribute("id", "choose-factor-" + number);
    inputs[0].required = !document.getElementById("dataset-settings-default").checked;

    console.log(newFactor);

    return newFactor;
}

function AddFactor()
{
    console.log("Adding")
    factors.appendChild(ConstructFactor(factors.children.length + 1))
    factorsCount = document.getElementById("factor-number")
    factorsCount.setAttribute("value", parseInt(factorsCount.getAttribute("value"), 10) + 1) 
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

function UpdateFactorInputs()
{
    for (i = 0; i < factors.children.length; i++)
    {
        var inputs = factors.children.item(i).getElementsByTagName("input");
        inputs[0].required = !document.getElementById("dataset-settings-default").checked;
    }
    document.getElementById("choose-result").required = !document.getElementById("dataset-settings-default").checked;
}

var factors = document.getElementById("factors")

document.getElementById("button-add-factor").addEventListener("click", AddFactor);
document.getElementById("button-remove-factor").addEventListener("click", RemoveFactor);
document.getElementById("dataset-settings-default").addEventListener("click", UpdateFactorInputs);
document.getElementById("dataset-settings-custom").addEventListener("click", UpdateFactorInputs);
