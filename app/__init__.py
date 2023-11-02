from flask import Flask
from config import config


# создание приложения, инициализация компонентов, модулей
def create_app(config_name):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])

    # ???
    config[config_name].init_app(app)

    from .modules.blueprint import main as bp
    app.register_blueprint(bp)

    # from .modules.blueprint import login_manager
    # login_manager.init_app(app)
    
    from .modules.db import init_module
    init_module(app)

    return app