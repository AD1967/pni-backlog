import os
from .neural.model import User
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config, BASE_DIR, UPLOAD_FOLDER, PATH_TO_UPLOAD, ALLOWED_EXTENSIONS

def create_database(app, db):
    print("Creating database...")
    with app.app_context():
        db.create_all()
        if User.query.all() == []:
            user = User(name="Test User", directory="Test_user")
            db.session.add(user)
            db.session.commit()
    path_dir = os.path.join(BASE_DIR, UPLOAD_FOLDER, "Test_user")
    if not os.path.exists(path_dir):
        #print("Deleting directory")
        #shutil.rmtree(path_dir)
        print("Creating directory")
        os.mkdir(path_dir)
        os.mkdir(os.path.join(path_dir, "datasets"))
        os.mkdir(os.path.join(path_dir, "predictions"))
        os.mkdir(os.path.join(path_dir, "validations"))
        os.mkdir(os.path.join(path_dir, "models"))
    print("New database was created")
    print()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    #app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.sqlite3"

    # ???
    config[config_name].init_app(app)

    from .neural.views import neural
    app.register_blueprint(neural)

    # from .modules.blueprint import login_manager
    # login_manager.init_app(app)
    
    from .database import db
    db.init_app(app)
    create_database(app, db)

    return app