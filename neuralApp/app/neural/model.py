from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from ..database import db

class User(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    hashPw = Column(String(128))
    token = Column(String(128))
    directory = Column(String(128))

    def __init__(self, name, directory):
        self.name = name
        self.directory = directory
    
class Dataset(db.Model):
    __tablename__ = "dataset"

    id = Column(Integer, primary_key=True)
    id_user = Column(ForeignKey("user.id"), nullable=False, index=True)
    name = Column(String(128))
    filePath = Column(String(128))

    user = relationship(User)

    def __init__(self, id_user, name, filePath):
        self.id_user = id_user
        self.name = name
        self.filePath = filePath

    def __repr__(self):
        return self.name

class Model(db.Model):
    __tablename__ = "model"

    id = Column(Integer, primary_key=True)
    id_user = Column(ForeignKey("user.id"), nullable=False, index=True)
    id_dataset = Column(ForeignKey("dataset.id"), nullable=True, index=True)
    name = Column(String(128))
    filePath = Column(String(128))
    structure = Column(String(256))
    epochs = Column(Integer)
    loss_function = Column(String(16))
    loss = Column(Float)
    training_time_s = Column(Float)
    metrics_mae = Column(Float)
    metrics_mape = Column(Float)
    metrics_rmse = Column(Float)
    metrics_test_mae = Column(Float)
    metrics_test_mape = Column(Float)
    metrics_test_rmse = Column(Float)

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
        return self.name
    
class Prediction(db.Model):
    __tablename__ = "prediction"

    id = Column(Integer, primary_key=True)
    id_model = Column(ForeignKey("model.id"), nullable=False, index=True)
    name = Column(String(128))
    filePath = Column(String(128))

    model = relationship(Model)

    def __init__(self, id_model, name, filePath):
        self.id_model = id_model
        self.name = name
        self.filePath = filePath

    def __repr__(self):
        return self.name
