import numpy as np
import pandas as pd
import time
import os

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.python.keras.utils.generic_utils import get_custom_objects
from tensorflow.keras.metrics import MeanAbsolutePercentageError as mape
from tensorflow.keras.metrics import MeanAbsoluteError as mae

def ExcelToValidate(path):
    columns_to_indexes = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9, "K": 10, "L": 11, "M": 12, 
    "N": 13, "O": 14, "P": 15, "Q": 16, "R": 17, "S": 18, "T": 19, "U": 20, "V": 21, "W": 22, "X": 23, "Y": 24, "Z": 25, "AA": 26, 
    "AB": 27, "AC": 28, "AD": 29, "AE": 30, "AF": 31, "AG": 32, "AH": 33, "AI": 34, "AJ": 35, "AK": 36, "AL": 37, "AM": 38, "AN": 39, 
    "AO": 40, "AP": 41, "AQ": 42, "AR": 43, "AS": 44, "AT": 45, "AU": 46, "AV": 47, "AW": 48, "AX": 49, "AY": 50, "AZ": 51}

    x_predict = []
    res_index = 0
    prediction_index = 0

    dataset_validation_dataframe = pd.read_excel(path, 0)
    prediction_index = dataset_validation_dataframe.shape[1]
    dataset_validation_numpy = dataset_validation_dataframe.to_numpy()

    columns = dataset_validation_numpy.shape[1]
    print(dataset_validation_numpy.shape[0])
    for item in range(dataset_validation_numpy.shape[0]):
        new_entry_predict = []
        for j in range(0, columns):
            if j != res_index:
                new_entry_predict.append(dataset_validation_numpy[item][j])
        x_predict.append(new_entry_predict)

    return np.array(x_predict), prediction_index, dataset_validation_dataframe

def normalize(x, train_stats):
    new_data = x.copy()
    for row in new_data:
        for i in range(len(row)):
            row[i] = (row[i] - train_stats["mean"][i]) / train_stats["std"][i]
    return new_data

def Validate(model, filePath, mean, std):
    print("START2")
    input_validate_data, prediction_index, dataframe = ExcelToValidate(filePath)
    stats = {"mean": mean, "std": std}
    print("Downloaded")
    normed_predict_data = normalize(input_validate_data, stats)
    print("normalized")
    prediction = model.predict(normed_predict_data)
    print("calculated")
    return np.sum(prediction) * 10

def UseModel(modelPath, filePath, mean, std):
    print("Using model ", modelPath, " for dataset")
    model = keras.models.load_model(modelPath, custom_objects={'mape': mape, 'mae': mae})
    return Validate(model, filePath, mean, std)

get_custom_objects().update({"mape": mape, "mae": mae})