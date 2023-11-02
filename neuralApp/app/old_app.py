from flask import Flask, redirect, url_for, render_template, request, flash, send_from_directory, send_file, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql import null
from sqlalchemy.orm import relationship
from neural.neural_module import CreateModel, UseModel, Validate
from werkzeug.utils import secure_filename
import os
import pandas as pd
import numpy as np
import shutil
import io

UPLOAD_FOLDER = 'static/files'
ALLOWED_EXTENSIONS = {'txt', 'csv', 'xls', 'xlsx', 'pkl'}
HIDDEN_LAYER_OPTIONS = ["Dense"]
ACTIVATION_OPTIONS = ["relu", "linear", "sigmoid", "tanh", "leakyrelu"]
COLUMNS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", 
"Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN", "AO", "AP", "AQ", "AR", "AS", "AT", "AU", 
"AV", "AW", "AX", "AY", "AZ"]
PATH_TO_UPLOAD = os.path.join(os.path.abspath(os.path.dirname(__file__)), UPLOAD_FOLDER)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.sqlite3"

print("Path to upload:", PATH_TO_UPLOAD)
print("Allowed extensions for datasets:", ALLOWED_EXTENSIONS)
print()

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "user"

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(128))
    hashPw = Column(db.String(128))
    token = Column(db.String(128))
    directory = Column(db.String(128))

    def __init__(self, name, directory):
        self.name = name
        self.directory = directory
    
class Dataset(db.Model):
    __tablename__ = "dataset"

    id = Column(db.Integer, primary_key=True)
    id_user = Column(ForeignKey("user.id"), nullable=False, index=True)
    name = Column(db.String(128))
    filePath = Column(db.String(128))

    user = relationship(User)

    def __init__(self, id_user, name, filePath):
        self.id_user = id_user
        self.name = name
        self.filePath = filePath

    def __repr__(self):
        return self.name

class Model(db.Model):
    __tablename__ = "model"

    id = Column(db.Integer, primary_key=True)
    id_user = Column(ForeignKey("user.id"), nullable=False, index=True)
    id_dataset = Column(ForeignKey("dataset.id"), nullable=True, index=True)
    name = Column(db.String(128))
    filePath = Column(db.String(128))
    structure = Column(db.String(256))
    epochs = Column(db.Integer)
    loss_function = Column(db.String(16))
    loss = Column(db.Float)
    training_time_s = Column(db.Float)
    metrics_mae = Column(db.Float)
    metrics_mape = Column(db.Float)
    metrics_rmse = Column(db.Float)
    metrics_test_mae = Column(db.Float)
    metrics_test_mape = Column(db.Float)
    metrics_test_rmse = Column(db.Float)

    user = relationship(User)
    dataset = relationship(Dataset)

    def __init__(self, id_user, id_dataset, name, filePath, structure, epochs, loss_function, loss, training_time_s, 
    metrics_mae, metrics_mape, metrics_rmse, metrics_test_mae, metrics_test_mape, metrics_test_rmse):
        self.id_user = id_user
        self.id_dataset = id_dataset
        self.name = name
        self.filePath = filePath
        self.structure = structure
        self.epochs = epochs
        self.loss_function = loss_function
        self.loss = loss
        self.training_time_s = training_time_s
        self.metrics_mae = metrics_mae
        self.metrics_mape = metrics_mape
        self.metrics_rmse = metrics_rmse
        self.metrics_test_mae = metrics_test_mae
        self.metrics_test_mape = metrics_test_mape
        self.metrics_test_rmse = metrics_test_rmse
    
    def __repr__(self):
        #return "[" + self.name + ":" + self.structure + "]"
        return self.name

def create_database():
    print("Creating database...")
    with app.app_context():
        db.create_all()
        if User.query.all() == []:
            user = User(name="Test User", directory="Test_user")
            db.session.add(user)
            db.session.commit()
    path_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], "Test_user")
    if not os.path.exists(path_dir):
        print("Creating directory")
        os.mkdir(path_dir)
        os.mkdir(os.path.join(path_dir, "datasets"))
        os.mkdir(os.path.join(path_dir, "predictions"))
        os.mkdir(os.path.join(path_dir, "validations"))
        os.mkdir(os.path.join(path_dir, "models"))
    print("New database was created")
    print()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# all_str = 0 - input, 1 - layer node, 2 - layer type, 3 - layer func, 4 - ..., 5 - ..., 6 - ..., ..., 
# 3n + 1 - nodes, 3n + 2 - type, 3n + 3 - func
def ParseModelStructure(str):
    all_str = str.split("-")
    result = "Число входных узлов: " + all_str[0]
    limit = int((len(all_str) - 1) / 3)
    for i in range(0, limit):
        layer_number = i + 1
        result += f"\nСлой {layer_number}: слой {all_str[3 * i + 1]} с числом узлов {all_str[3 * i + 2]} и функцией {all_str[3 * i + 3]}"
    return result

def GetModelReportStr(model_db):
    report_text = "Название модели: " + model_db.name + "\nСтруктура модели:\n" + \
        ParseModelStructure(model_db.structure) + \
            "\nЧисло эпох обучения: " + str(model_db.epochs) + "\nПродолжительность обучения (с): " + \
                str(model_db.training_time_s) + "\nЗначение функции потерь после последней эпохи: " + \
                    str(model_db.loss) + \
                    "\nЗначение MAE (средняя абсолютная ошибка) для обучающего набора после последней эпохи: " + \
                        str(model_db.metrics_mae) + \
                        "\nЗначение MAPE (средняя абсолютная процентная ошибка) для обучающего набора после последней эпохи: " + \
                            str(model_db.metrics_mape) + \
                            "\nЗначение RMSE (среднеквадратичная ошибка) для обучающего набора после последней эпохи: " + \
                                str(model_db.metrics_rmse) + \
                                "\nЗначение MAE (средняя абсолютная ошибка) для тестового набора: " + \
                                    str(model_db.metrics_test_mae) + \
                                        "\nЗначение MAPE (средняя абсолютная процентная ошибка) для тестового набора: " + \
                                            str(model_db.metrics_test_mape) + \
                                                "\nЗначение RMSE (средневадратичная ошибка) для тестового набора: " + \
                                                    str(model_db.metrics_test_rmse)
    return report_text

@app.route("/home", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def home_page():
    current_user = User.query.filter_by(id=1).first()
    error = False
    message = ""
    if request.method == "POST":
        print(request.form)
        if "delete-dataset" in request.form and "all-dataset-file" in request.form:
            dataset_to_delete = Dataset.query.filter_by(name=request.form["all-dataset-file"]).first()
            model_to_edit = Model.query.filter_by(id_dataset=dataset_to_delete.id).all()
            shutil.rmtree(os.path.join(PATH_TO_UPLOAD, current_user.directory, "datasets", dataset_to_delete.name))
            db.session.delete(dataset_to_delete)
            for model in model_to_edit:
                model.id_dataset = None
        if "edit-dataset" in request.form and "all-dataset-file" in request.form:
            dataset_to_edit = Dataset.query.filter_by(name=request.form["all-dataset-file"]).first()
            dataset_to_edit.name = request.form["edit-dataset-name"]
        if "download-dataset" in request.form and "all-dataset-file" in request.form:
            dataset_to_download = Dataset.query.filter_by(name=request.form["all-dataset-file"]).first()
            return send_file(os.path.join(PATH_TO_UPLOAD, current_user.directory, "datasets", dataset_to_download.name, 
                                          dataset_to_download.filePath), as_attachment=True, 
                                          download_name='Dataset_' + dataset_to_download.name + ".xlsx")
        if "download-ann-model-report" in request.form and "all-ann-models" in request.form:
            model_to_report = Model.query.filter_by(name=request.form["all-ann-models"]).first()
            report_text = GetModelReportStr(model_to_report)
            buffer = io.BytesIO()
            buffer.write(report_text.encode('utf-8'))
            buffer.seek(0)
            return send_file(buffer, as_attachment=True, download_name='ANN_report_file_' + model_to_report.name + ".txt", 
            mimetype='text/csv')
        if "delete-ann-model" in request.form and "all-ann-models" in request.form:
            model_to_delete = Model.query.filter_by(name=request.form["all-ann-models"]).first()
            shutil.rmtree(os.path.join(PATH_TO_UPLOAD, current_user.directory, "models", model_to_delete.filePath))
            #os.remove(os.path.join(PATH_TO_UPLOAD, current_user.directory, "models", model_to_delete.filePath + ".h5"))
            db.session.delete(model_to_delete)
        if "edit-ann-model" in request.form and "all-ann-models" in request.form:
            model_to_edit = Model.query.filter_by(name=request.form["all-ann-models"]).first()
            model_to_edit.name = request.form["edit-ann-model-name"]

            os.rename(os.path.join(PATH_TO_UPLOAD, current_user.directory, "models", model_to_edit.filePath), 
            os.path.join(PATH_TO_UPLOAD, current_user.directory, "models", model_to_edit.name))

            os.rename(os.path.join(PATH_TO_UPLOAD, current_user.directory, "models", model_to_edit.name, model_to_edit.filePath + ".h5"), 
            os.path.join(PATH_TO_UPLOAD, current_user.directory, "models", model_to_edit.name, model_to_edit.name + ".h5"))

            os.rename(os.path.join(PATH_TO_UPLOAD, current_user.directory, "models", model_to_edit.name, model_to_edit.filePath + \
                "Stat.xlsx"), 
            os.path.join(PATH_TO_UPLOAD, current_user.directory, "models", model_to_edit.name, model_to_edit.name + "Stat.xlsx"))

            if (os.path.exists(os.path.join(PATH_TO_UPLOAD, current_user.directory, "validations", model_to_edit.filePath + \
                ".xlsx"))):

                print("change validation name")
                os.rename(os.path.join(PATH_TO_UPLOAD, current_user.directory, "validations", model_to_edit.filePath + ".xlsx"), 
                          os.path.join(PATH_TO_UPLOAD, current_user.directory, "validations", model_to_edit.name + ".xlsx"))

            model_to_edit.filePath = model_to_edit.name
        if "download-last-prediction" in request.form and "all-ann-models" in request.form:
            predictPath = os.path.join(PATH_TO_UPLOAD, current_user.directory, "validations", 
            Model.query.filter_by(name=request.form["all-ann-models"]).first().name + ".xlsx")
            if (os.path.exists(predictPath)):
                return send_file(predictPath, as_attachment=True)
            else:
                error = True
                message = "Отсутствует файл с прогнозом, выполненным выбранной моделью '" + request.form["all-ann-models"] + "'"
        db.session.commit()
    list_datasets = Dataset.query.filter_by(id_user=current_user.id).all()
    list_models = Model.query.filter_by(id_user=current_user.id).all()
    print(list_datasets)
    print(list_models)
    if error:
        return render_template("index.html", user=current_user.name, list_datasets=list_datasets, list_models=list_models, 
        error=error, message=message)
    return render_template("index.html", user=current_user.name, list_datasets=list_datasets, list_models=list_models)

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

# Only positive!
def represents_int(s):
    try: 
        int(s)
    except ValueError:
        return False
    else:
        return True and int(s) > 0

model_training = False
gl_model_name = ""
@app.route("/create_model", methods = ["GET", "POST"])
def create_model():
    global model_training
    global gl_model_name
    if request.method == "POST" and not model_training:
        current_user = User.query.filter_by(id=1).first()
        print()
        print("POST data for create_model")
        print(request.form)
        dataset_status = None
        model_name = request.form["ann-model-name"]
        gl_model_name = model_name
        if 'upload-dataset-file' not in request.files:
            print('No file part')
            dataset_status = "No file part"
        else:
            file = request.files['upload-dataset-file']
            if file.filename == '':
                print('No selected file')
                if (request.form["choose-dataset-file"] != ""):
                    dataset_status = "Chosen"
            elif file and allowed_file(file.filename):
                dataset_status = "Uploaded"
                filename = secure_filename(file.filename)

                dataset_name = request.form["upload-dataset-file-name"]
                if request.form["upload-dataset-file-name"] == "":
                    dataset_name = filename

                os.mkdir(os.path.join(PATH_TO_UPLOAD, current_user.directory, "datasets", dataset_name))
                
                save_path = os.path.join(PATH_TO_UPLOAD, current_user.directory, "datasets", dataset_name, filename)
                print("Saving dataset to:", save_path)
                file.save(save_path)

                dataset = Dataset(current_user.id, dataset_name, filename)
                db.session.add(dataset)
                db.session.commit()
        
        dataset_to_train = None
        if dataset_status == "Chosen":
            dataset_to_train = Dataset.query.filter_by(name=request.form["choose-dataset-file"]).first()
            print("Chosen dataset id:", dataset_to_train.id)
        if dataset_status == "Uploaded":
            dataset_to_train = Dataset.query.filter_by(name=dataset_name).first()
            print("File uploaded by id:", dataset_to_train.id)
            print("File saved as:", request.form["upload-dataset-file-name"])

        if dataset_status == "Chosen" or dataset_status == "Uploaded":
            #print("Input units:", request.form["input_units"])

            hidden_layers = []
            hidden_units = []
            activation_functions = []
            i = 1
            correct_fields = True
            #model_struct = request.form["input_units"]
            model_struct = ""
            number_layers = int(request.form["layers-number"]) + 1
            while i < number_layers and correct_fields:
                hidden_layer = request.form[f"choose-hidden-layer-{i}"]
                hidden_unit = request.form[f"hidden-units-{i}"]
                activation_function = request.form[f"choose-activation-{i}"]
                if (hidden_layer in HIDDEN_LAYER_OPTIONS) and (activation_function in ACTIVATION_OPTIONS) \
                and represents_int(hidden_unit):
                    hidden_layers.append(hidden_layer)
                    hidden_units.append(int(hidden_unit))
                    activation_functions.append(activation_function)
                    model_struct += "-" + hidden_layer + "-" + hidden_unit + "-" + activation_function
                else:
                    print("NO DATA IN FIELD:", i)
                    if (i == 1):
                        print("NO CORRECT LAYERS")
                        return redirect(url_for("home_page"))
                    else:
                        correct_fields = False
                i += 1
            print("Chosen hidden layers:", hidden_layers)
            print("Hidden units:", hidden_units)
            print("Chosen activation:", activation_functions)
            print()
            model_training = True
            dataset_settings = {"mode": request.form["dataset-settings"]}
            list_factors = []
            if dataset_settings["mode"] == "Custom":
                for i in range(1, int(request.form["factor-number"]) + 1):
                    list_factors.append(request.form[f"choose-factor-{i}"])
                dataset_settings["result_column"] = request.form["choose-result"]
            print("Settings:", dataset_settings)
            print("Factors:", list_factors)

            loss_function = request.form["choose-loss"]
            to_predict = (request.form["dataset-settings-2"] == "Yes")

            try:
                model, input_units, model_history, test_scores, time, mean, std = \
                CreateModel(os.path.join(PATH_TO_UPLOAD, current_user.directory, "datasets", dataset_to_train.name, dataset_to_train.filePath), dataset_settings, list_factors, hidden_layers, hidden_units, activation_functions,
                int(request.form["epoch-number"]), loss_function, to_predict, os.path.join(PATH_TO_UPLOAD, current_user.directory, "validations", 
                model_name + ".xlsx"))
            except Exception as ex:
                model_training = False
                gl_model_name = ""
                error_message = ex.args[0]
                print(error_message)
                return error_message

            epochs = 0
            last_train_loss = 0
            metrics_mae = 0
            metrics_mape = 0
            metrics_rmse = 0
            metrics_test_mae = 0
            metrics_test_mape = 0
            metrics_test_rmse = 0
            if ("epochs" in model_history.params):
                epochs = model_history.params["epochs"]
                last_train_loss = model_history.history["loss"][epochs - 1]
                metrics_mae = model_history.history["mean_absolute_error"][epochs - 1]
                metrics_mape = model_history.history["mean_absolute_percentage_error"][epochs - 1]
                metrics_rmse = model_history.history["root_mean_squared_error"][epochs - 1]
                metrics_test_mae = test_scores[1]
                metrics_test_mape = test_scores[2]
                metrics_test_rmse = test_scores[3]


            # ПОПРАВИТЬ В БУДУЩЕМ model_name на имя файла
            # Path to model dicrectory
            save_model_path = os.path.join(PATH_TO_UPLOAD, current_user.directory, "models", model_name)
            os.mkdir(save_model_path)
            #model.save(save_model_path)
            # TEMP: in directory save as {model_name}.h5
            model.save(os.path.join(save_model_path, model_name + ".h5"))
            stats = []
            stats.append(mean.to_numpy())
            stats.append(std.to_numpy())
            np_stats = np.array(stats)
            np_stats = np.transpose(np_stats)
            #stats.transpose()
            df_stat = pd.DataFrame(np_stats)
            # TEMP: in directory save as {model_name}Stat.xlsx
            df_stat.to_excel(os.path.join(save_model_path, model_name + "Stat.xlsx"), index=False)
            print(save_model_path)
            model_struct = f"{input_units}" + model_struct
            model_db = Model(current_user.id, dataset_to_train.id, model_name, model_name, model_struct, epochs, loss_function, 
            last_train_loss, time, metrics_mae, metrics_mape, metrics_rmse, metrics_test_mae, metrics_test_mape, metrics_test_rmse)
            db.session.add(model_db)
            db.session.commit()

            if (to_predict):
                report_text = GetModelReportStr(model_db)
                df_model = pd.DataFrame()
                df_model.insert(loc=0, column="Структура модели ИНС", value=report_text.split("\n"))
                df_prediction = pd.read_excel(os.path.join(PATH_TO_UPLOAD, current_user.directory, "validations", 
                model_name + ".xlsx"), sheet_name=0)
                writer = pd.ExcelWriter(os.path.join(PATH_TO_UPLOAD, current_user.directory, "validations", 
                model_name + ".xlsx"), engine='openpyxl')
                df_prediction.to_excel(writer, sheet_name='Прогноз модели', index=False)
                df_model.to_excel(writer, sheet_name='Структура модели', index=False)
                writer.close()
        model_training = False
        gl_model_name = ""
        return redirect(url_for("create_model"))
    elif request.method == "POST":
        return "Training is being performed for another user. Try again later."
    elif request.method == "GET" and model_training:
        return redirect(url_for("progress_page"))
    else:
        current_user = User.query.filter_by(id=1).first()
        list_datasets = Dataset.query.filter_by(id_user=current_user.id).all()
        print(list_datasets)
        list_column = []
        print(COLUMNS)
        return render_template("create_model.html", list_datasets=list_datasets, list_columns=COLUMNS)

@app.route("/use_model", methods = ["GET", "POST"])
def use_model():
    global model_training
    if request.method == "POST" and not model_training:
        current_user = User.query.filter_by(id=1).first()
        print()
        print("POST data for use_model")
        dataset_status = None
        print(request.files)
        if 'upload-dataset-file' not in request.files:
            print('No file part')
            dataset_status = "No file part"
        else:
            file = request.files['upload-dataset-file']
            if file.filename == '':
                print('No selected file')
                if (request.form["choose-dataset-file"] != ""):
                    dataset_status = "Chosen"
            elif file and allowed_file(file.filename):
                dataset_status = "Uploaded"
                filename = secure_filename(file.filename)
                save_path = os.path.join(PATH_TO_UPLOAD, current_user.directory, "datasets", filename)
                print("Saving dataset to:", save_path)
                file.save(save_path)

                dataset_name = request.form["upload-dataset-file-name"]
                if request.form["upload-dataset-file-name"] == "":
                    dataset_name = filename
                dataset = Dataset(current_user.id, dataset_name, save_path)
                db.session.add(dataset)
                db.session.commit()
        dataset_to_predict = None
        if dataset_status == "Chosen":
            dataset_to_predict = Dataset.query.filter_by(name=request.form["choose-dataset-file"]).first()
            print("Chosen dataset id:", dataset_to_predict.id)
        if dataset_status == "Uploaded":
            dataset_to_predict = Dataset.query.filter_by(name=dataset_name).first()
            print("File uploaded by id:", dataset_to_predict.id)
            print("File saved as:", request.form["upload-dataset-file-name"])

        if dataset_status == "Chosen" or dataset_status == "Uploaded":
            print("Проверка существования модели")
            print(request.form["choose-ann-model"])
            print(Model.query.filter_by(id_user=current_user.id).all())
            model_name = request.form["choose-ann-model"]
            all_models = [m.name for m in Model.query.filter_by(id_user=current_user.id).all()]
            if model_name in all_models:
                print("Модель в наличии")
                #model_training = True
                dataset_settings = {"mode": request.form["dataset-settings"], "sheet": 0}
                list_factors = []
                if dataset_settings["mode"] == "Custom":
                    for i in range(1, int(request.form["factor-number"]) + 1):
                        list_factors.append(request.form[f"choose-factor-{i}"])
                    dataset_settings["result_column"] = request.form["choose-result"]
                    # TO DO: исправить взятие столбца для прогноза, и его определение
                    #dataset_settings["prediction_column"] = request.form["choose-prediction"]
                    dataset_settings["prediction_column"] = "A"
                print("Settings:", dataset_settings)
                print("Factors:", list_factors)
                #predictPath = os.path.join(PATH_TO_UPLOAD, current_user.directory, "predictions", 
                #Model.query.filter_by(name=request.form["choose-ann-model"]).first().name + ".xlsx")
                model_db = Model.query.filter_by(name=request.form["choose-ann-model"]).first()
                
                df_stat = pd.read_excel(os.path.join(PATH_TO_UPLOAD, current_user.directory, "models", model_name, model_name + "Stat.xlsx"))
                print(df_stat)
                np_mean = [row[0] for row in df_stat.to_numpy()]
                np_std = [row[1] for row in df_stat.to_numpy()]
                predictPath = os.path.join(PATH_TO_UPLOAD, current_user.directory, "validations", 
                model_db.name + ".xlsx")
                print("Путь сохранения результата:", predictPath)
                try:                   
                    UseModel(
                        os.path.join(PATH_TO_UPLOAD, current_user.directory, "models", model_db.name, model_db.name + ".h5"), 
                    os.path.join(PATH_TO_UPLOAD, current_user.directory, "datasets", dataset_to_predict.name, dataset_to_predict.filePath), 
                    predictPath, dataset_settings, list_factors, np_mean, np_std)
                except Exception as ex:
                    return ex.args[0]
                #model_training = False
                return send_file(predictPath, as_attachment=True)
            else:
                print("Модели нет")
        #model_training = False
        return render_template("use_model.html")
    elif request.method == "POST":
        #return "Training is being performed for another user. Try again later."
        return redirect(url_for("progress_page"))
    else:
        current_user = User.query.filter_by(id=1).first()
        list_datasets = Dataset.query.filter_by(id_user=current_user.id).all()
        list_models = Model.query.filter_by(id_user=current_user.id).all()
        print(list_datasets)
        print(list_models)
        return render_template("use_model.html", list_datasets=list_datasets, list_models=list_models, list_columns=COLUMNS)

@app.route("/datasets")
def datasets_info():
    current_user = User.query.filter_by(id=1).first()
    list_datasets = Dataset.query.filter_by(id_user=current_user.id).all()
    print(list_datasets)
    json = {"datasets": [dataset.name for dataset in list_datasets]}
    print(json)
    return json

@app.route("/models")
def models_info():
    current_user = User.query.filter_by(id=1).first()
    list_models = Model.query.filter_by(id_user=current_user.id).all()
    print(list_models)
    json = {"models": [model.name for model in list_models]}
    return json

@app.route("/progress_info")
def progress_info():
    global model_training
    global gl_model_name
    json = {"mode": f"{model_training}"}
    if (model_training):
        json["name"] = gl_model_name
    print(json)
    return json

@app.route("/progress")
def progress_page():
    global gl_model_name
    global model_training
    return render_template("progress.html", model_training=model_training, model_name=gl_model_name)

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/page_not_found")
def page_not_found():
    return "<h1>Ошибка: данной страницы не существует</h1>"

@app.errorhandler(404)
def wrong_page(page):
    return redirect(url_for("page_not_found"))

if __name__ == "__main__":
    print("Launching app...")
    print("Все пути:", app.url_map)
    print()
    create_database()
    app.run(debug = True)