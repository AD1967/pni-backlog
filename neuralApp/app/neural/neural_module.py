import numpy as np
import pandas as pd
import time
import os

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# FOR FUTURE?
def DivideDataset(dataset_numpy, part_to_train=0.7):
    x_train = []
    y_train = []
    x_test = []
    y_test = []

    print(dataset_numpy.shape)
    first_test_item_number = int(dataset_numpy.shape[0] * part_to_train)
    print("Number of first item to test:", first_test_item_number)
    i = 0
    for array in dataset_numpy:
        new_entry = []
        for j in range(1, array.size):
            new_entry.append(array[j])
        if i < first_test_item_number:
            x_train.append(new_entry)
            y_train.append(array[0])
        else:
            x_test.append(new_entry)
            y_test.append(array[0])
        i += 1
    return np.array(x_train), np.array(y_train), np.array(x_test), np.array(y_test)

def GetColumnIndexes(columns):
    columns_to_indexes = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9, "K": 10, "L": 11, "M": 12, 
    "N": 13, "O": 14, "P": 15, "Q": 16, "R": 17, "S": 18, "T": 19, "U": 20, "V": 21, "W": 22, "X": 23, "Y": 24, "Z": 25, "AA": 26, 
    "AB": 27, "AC": 28, "AD": 29, "AE": 30, "AF": 31, "AG": 32, "AH": 33, "AI": 34, "AJ": 35, "AK": 36, "AL": 37, "AM": 38, "AN": 39, 
    "AO": 40, "AP": 41, "AQ": 42, "AR": 43, "AS": 44, "AT": 45, "AU": 46, "AV": 47, "AW": 48, "AX": 49, "AY": 50, "AZ": 51}

    list_indexes = []
    for item in columns:
        list_indexes.append(columns_to_indexes[item])
    list_indexes.sort()
    return list_indexes

def GetRelativeIndex(target, indexes):
    flag = True
    local_indexes = indexes.copy()
    local_indexes.sort()
    i = 0
    while flag and i < len(local_indexes):
        if target < local_indexes[i]:
            flag = False
        else:
            i += 1
    return i

def UseExcelDataset(filePath, settings, factors):
    columns_to_indexes = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9, "K": 10, "L": 11, "M": 12, 
    "N": 13, "O": 14, "P": 15, "Q": 16, "R": 17, "S": 18, "T": 19, "U": 20, "V": 21, "W": 22, "X": 23, "Y": 24, "Z": 25, "AA": 26, 
    "AB": 27, "AC": 28, "AD": 29, "AE": 30, "AF": 31, "AG": 32, "AH": 33, "AI": 34, "AJ": 35, "AK": 36, "AL": 37, "AM": 38, "AN": 39, 
    "AO": 40, "AP": 41, "AQ": 42, "AR": 43, "AS": 44, "AT": 45, "AU": 46, "AV": 47, "AW": 48, "AX": 49, "AY": 50, "AZ": 51}

    x_train = []
    y_train = []
    x_test = []
    y_test = []

    res_index = 0

    if (settings["mode"] == "Default"):
        dataset_train_dataframe = pd.read_excel(filePath, sheet_name=0)
        dataset_test_dataframe = pd.read_excel(filePath, sheet_name=1)
    elif (settings["mode"] == "Custom"):
        list_factors = GetColumnIndexes(factors)
        res_col_index = columns_to_indexes[settings["result_column"]]
        all_indexes = list_factors.copy()
        all_indexes.append(res_col_index)
        dataset_train_dataframe = pd.read_excel(filePath, sheet_name=0, usecols=all_indexes)
        dataset_test_dataframe = pd.read_excel(filePath, sheet_name=1, usecols=all_indexes)

        res_index = GetRelativeIndex(res_col_index, list_factors)
        print("Factors:", factors)
        print("Result:", settings["result_column"])
        print("Column indexes:", list_factors)
        print("All indexes:", all_indexes)
        print("Index for res:", res_index)
    else:
        print("Undefined behavior in UseExcelDataset")
    dataset_train_numpy = dataset_train_dataframe.to_numpy()
    dataset_test_numpy = dataset_test_dataframe.to_numpy()

    print("Train data", dataset_train_dataframe)
    print("Train numpy", dataset_train_numpy)
    print("Test data", dataset_test_dataframe)
    print("Test numpy", dataset_test_numpy)
    columns = dataset_train_numpy.shape[1]
    print("Columns number:", columns)
    limit = max(dataset_test_numpy.shape[0], dataset_train_numpy.shape[0])
    print("limit:", limit)
    for item in range(limit):
        new_entry_train = []
        new_entry_test = []
        for j in range(0, columns):
            if (item < dataset_train_numpy.shape[0]) and j != res_index:
                new_entry_train.append(dataset_train_numpy[item][j])
            if (item < dataset_test_numpy.shape[0]) and j != res_index:
                new_entry_test.append(dataset_test_numpy[item][j])
        if (item < dataset_train_numpy.shape[0]):
            x_train.append(new_entry_train)
            y_train.append(dataset_train_numpy[item][res_index])
        if (item < dataset_test_numpy.shape[0]):
            x_test.append(new_entry_test)
            y_test.append(dataset_test_numpy[item][res_index])
    print("Factors number:", len(x_train[0]))
    return np.array(x_train), np.array(y_train), np.array(x_test), np.array(y_test), len(x_train[0]), dataset_train_dataframe, dataset_test_dataframe

def ExcelToValidate(path, settings, factors):
    columns_to_indexes = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9, "K": 10, "L": 11, "M": 12, 
    "N": 13, "O": 14, "P": 15, "Q": 16, "R": 17, "S": 18, "T": 19, "U": 20, "V": 21, "W": 22, "X": 23, "Y": 24, "Z": 25, "AA": 26, 
    "AB": 27, "AC": 28, "AD": 29, "AE": 30, "AF": 31, "AG": 32, "AH": 33, "AI": 34, "AJ": 35, "AK": 36, "AL": 37, "AM": 38, "AN": 39, 
    "AO": 40, "AP": 41, "AQ": 42, "AR": 43, "AS": 44, "AT": 45, "AU": 46, "AV": 47, "AW": 48, "AX": 49, "AY": 50, "AZ": 51}

    x_predict = []
    res_index = 0
    prediction_index = 0

    if (settings["mode"] == "Default"):
        dataset_validation_dataframe = pd.read_excel(path, sheet_name=settings["sheet"])
        prediction_index = dataset_validation_dataframe.shape[1]
        print("Factors (validation):", factors)
        print("Result (validation): A")
        print("Index for res (validation):", res_index)
        print("Index for prediction (validation):", prediction_index)
    elif (settings["mode"] == "Custom"):
        list_factors = GetColumnIndexes(factors)
        res_col_index = columns_to_indexes[settings["result_column"]]
        predict_col_index = columns_to_indexes[settings["prediction_column"]]
        all_indexes = list_factors.copy()
        all_indexes.append(res_col_index)

        dataset_validation_dataframe = pd.read_excel(path, sheet_name=settings["sheet"], usecols=all_indexes)

        res_index = GetRelativeIndex(res_col_index, list_factors)
        prediction_index = GetRelativeIndex(predict_col_index, all_indexes)

        print("Factors (validation):", factors)
        print("Result (validation):", settings["result_column"])
        print("Column indexes (validation):", list_factors)
        print("All indexes (validation):", all_indexes)
        print("Index for res (validation):", res_index)
        print("Index for prediction (validation):", prediction_index)

    dataset_validation_numpy = dataset_validation_dataframe.to_numpy()

    print("Validation data", dataset_validation_dataframe)
    print("Validation numpy", dataset_validation_numpy)

    columns = dataset_validation_numpy.shape[1]
    print("Columns (validation):", columns)

    for item in range(dataset_validation_numpy.shape[0]):
        new_entry_predict = []
        for j in range(0, columns):
            if j != res_index:
                new_entry_predict.append(dataset_validation_numpy[item][j])
        x_predict.append(new_entry_predict)
    print("Factors number (validation):", len(x_predict[0]))

    return np.array(x_predict), prediction_index, dataset_validation_dataframe

def SetModel(input_units, hidden_layers, hidden_units, activation_functions, loss_function):
    print("Setting ANN Model")
    print()
    error_msg = ""
    error = False
    model = keras.Sequential()
    model.add(layers.InputLayer(input_shape = (input_units, )))
    for i in range(0, len(hidden_layers)):
        if hidden_layers[i] == "Dense":
            if (activation_functions[i] != "leakyrelu"):
                model.add(layers.Dense(units = hidden_units[i], activation = activation_functions[i]))
            else:
                model.add(layers.Dense(units = hidden_units[i]))
                model.add(layers.LeakyReLU())
        elif hidden_layers[i] == "LSTM":
            error = True
            error_msg = "LSTM is not supported yet"
            print(error_msg)
        else:
            error = True
            error_msg = "Error: this type of layer is not supported:" + hidden_layers[i]
            print(error_msg)
    model.add(layers.Dense(units = 1))
    if not error:
        model.compile(loss = loss_function, 
        metrics = ["mean_absolute_error", "mean_absolute_percentage_error", tf.keras.metrics.RootMeanSquaredError()], optimizer = "adam")
        model.summary()
    print()
    return model

def TrainModel(model, epoch_number, model_data, x_train, y_train, x_test, y_test):
    print("Launching training for model", model_data)
    imitate = False
    history = []
    start_time = 0
    finish_time = 0
    scores = []
    if imitate:
        print("Imitating training for model", model_data)
        i = 0
        while i < 500000000:
            i += 1
    else:
        start_time = time.time()
        # batch size? prev 100
        history=model.fit(x_train, y_train, epochs=epoch_number, batch_size=32,validation_split=0.1)
        
        print(history)
        print(history.history)
        print(history.params)

        finish_time = time.time()
        print("--- %s seconds ---" % (finish_time - start_time))

        print((finish_time - start_time)/60,'minutes')
        scores = model.evaluate(x_test, y_test)
        print("TEST MAPE :",scores)
    print("Finish training for model", model_data)
    return history, scores, (finish_time - start_time)

def normalize(x, train_stats):
    new_data = x.copy()
    for row in new_data:
        for i in range(len(row)):
            row[i] = (row[i] - train_stats["mean"][i]) / train_stats["std"][i]
    return new_data

def CreateModel(filePath, settings, factors, hidden_layers, hidden_units, activation_functions, epochs, loss, to_predict, validate_path):
    print("Launching model creation...")

    # Пока без предобработки, считаем, что датасет обработан и сохранён через эксель
    #dataset = ProcessDatasetToTrain(dataset_id)
    #dataset = Dataset.query.filter_by(id=dataset_id).first()
    #current_user = User.query.filter_by(id=1).first()
    #dataset_file = pd.read_excel(os.path.join(PATH_TO_UPLOAD, current_user.directory, "datasets", dataset.filePath))
    # dataset_numpy, dataframe = UseExcelDataset(filePath, settings)
    # model = SetModel(input_units, hidden_layers, hidden_units, activation_functions)
    # model_data = [input_units, hidden_layers, hidden_units, activation_functions]
    # model_history, test_scores, duration = TrainModel(model, dataset_numpy, model_data)
    
    x_train, y_train, x_test, y_test, input_units, data1, data2 = UseExcelDataset(filePath, settings, factors)

    print("x_train:", x_train)
    print("y_train:", y_train)
    print("x_test:", x_test)
    print("y_test:", y_test)

    if (x_train.shape[1] != x_test.shape[1]):
        raise Exception(f"Обучающий и тестовый наборы имеют разные формы: {x_train.shape[1]} и {x_test.shape[1]}")

    df_x_train = pd.DataFrame(x_train)
    df_train_stats = df_x_train.describe()
    train_stats = df_train_stats.transpose()
    print(train_stats)

    normed_train_regressors = normalize(x_train, train_stats)
    normed_test_regressors = normalize(x_test, train_stats)

    print("normed x_train:", normed_train_regressors)
    print("normed x_test:", normed_test_regressors)

    model = SetModel(input_units, hidden_layers, hidden_units, activation_functions, loss)
    model_data = [input_units, hidden_layers, hidden_units, activation_functions]
    model_history, test_scores, duration = TrainModel(model, epochs, model_data, normed_train_regressors, y_train, normed_test_regressors, y_test)
    if to_predict:
        prediction = model.predict(normed_test_regressors)
        data2.insert(len(data2.columns), "Прогноз", prediction, True)
        print("Inserted to dataframe for prediction")
        print(data2.head())
        data2.to_excel(validate_path, index=False)
        print("Saved to .xlsx")
    return model, input_units, model_history, test_scores, duration, train_stats["mean"], train_stats["std"]

def BuildPredictData(predict, input):
    result = []
    for i in range(0, len(predict)):
        new_entry = [predict[i]]
        new_entry.extend(input[i])
        result.append(new_entry)
    return np.array(result)

def Validate(model, input, filePath, validatePath, settings, list_factors, mean, std):
    print("Using model to validate")
    input_validate_data, prediction_index, dataframe = ExcelToValidate(filePath, settings, list_factors)
    if (input_validate_data.shape[1] != input):
        raise Exception(f"Набор для прогноза имеет форму, отличную от входного слоя ИНС: {input_validate_data.shape[1]} и {input}")
    print("Validation dataset was received")
    stats = {"mean": mean, "std": std}
    print(stats)
    normed_predict_data = normalize(input_validate_data, stats)
    print("Normed precit data:", normed_predict_data)
    prediction = model.predict(normed_predict_data)
    print("Prediction done")
    dataframe.insert(prediction_index, "Прогноз", prediction, True)
    print("Inserted to dataframe for validation")
    print(dataframe.head())
    dataframe.to_excel(validatePath, index=False)
    print("Saved to .xlsx")

def UseModel(modelPath, filePath, predictPath, settings, list_factors, mean, std):
    print("Using model ", modelPath, " for dataset")
    model = keras.models.load_model(modelPath)
    input = model.layers[0].input_shape[1]
    print("Model was loaded")
    Validate(model, input, filePath, predictPath, settings, list_factors, mean, std)
