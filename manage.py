import os
from flask_cors import CORS
from sqlalchemy import false
from app import create_app

# создание приложения
# можно задать в окружении черз FLASK_CONFIG
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# enable CORS
CORS(app)

# запуск
if __name__ == "__main__":
    print("Все пути: ",app.url_map)
    app.run(threaded=True)
