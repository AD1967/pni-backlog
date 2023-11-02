from datetime import date, datetime
import os
from os.path import join as path_join
import json

from config import config

import flask
from app.modules.db import db, init_module
from app.modules.db.model import Build, User, Q_wnd, Q_door, get_elem_class_by_str, first_char_to_upper

app = flask.Flask(__name__, instance_relative_config=True)
app.config.from_object(config['default'])
init_module(app)


#для переменования параметров lambda в lambd
def lambda_corrector(v):
    if(v.get('lambda') != None):
        v['lambd'] = v.pop('lambda')
    return v

#удалить ВСЕ ТАБЛИЦЫ и создать ВСЕ таблицы из db.model (классов) 
def sqlalch_create():
    with app.app_context():
        try:
            for table in reversed(db.metadata.sorted_tables):
                if(table.name != 'weather'):
                    table.delete()
            db.create_all()
            db.session.commit()
        except:
            print("sqlalch_create ошибка создания БД")

#перезаполнить таблицы из json
def sqlalch_refill():
    c = config['default']
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_object(c)
    db.init_app(app)
    with app.app_context():
        try:
            print("sqlalch_refill")
            db_jsons =  c.DATABASE_JSONS
            for f in  filter(lambda x: x.endswith('.json'), os.listdir(db_jsons)):
                data = list(json.load(open(path_join(db_jsons, f), encoding='utf-8')))
                id = f[0:len(f)-5]
                klass = get_elem_class_by_str(first_char_to_upper(id))
                print(id)
                klass.__table__.drop(db.engine)
                klass.__table__.create(db.engine)
                for v in data:
                    d = lambda_corrector(dict(v))
                    if(klass == Build):
                        d[ 'date_build'] = datetime.fromisoformat(d[ 'date_build'])
                    elif(klass == User):
                        d[ 'token_expiration'] = datetime.fromisoformat(d[ 'token_expiration'])
                    elif(klass == Q_wnd):
                        d[ 'date_wnd'] = datetime.fromisoformat(d[ 'date_wnd'])
                    elif(klass == Q_door):
                        d[ 'date_doors'] = datetime.fromisoformat(d[ 'date_doors'])
                    db.session.add(klass(d))
            db.session.commit()
        except:
           db.session.rollback()
           print("sqlalch_refill ошибка заполнения БД")

sqlalch_create()
sqlalch_refill()