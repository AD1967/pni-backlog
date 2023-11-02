import os
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == "__main__":
    print("All endpoints:", app.url_map)
    app.run(threaded=True)
