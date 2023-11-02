from .model import User
from . import db

import base64
from datetime import datetime, timedelta
import os

# функция добавления нового пользователя в бд
def addUser(name, hpsw):
    try:
        res = User.query.filter(User.name.like(name)).count()
        if res > 0:
            print(f"Пользователь с таким login уже существует: login = {name}")
            return False
        db.session.add(User({'name': name, 'password':  hpsw, 'token': "default_token", 'token_expiration': datetime.utcnow() - timedelta(seconds=1) }))
        db.session.commit()
    except:
        print("addUser, Ошибка добавления пользователя в БД ")
        return False
    return True

# функция для получения пользователя из бд по login
def getUserByLogin(login):
    try:
        res = User.query.filter_by(name = login).first()
        if not res:
            print(f"Пользователь не найден: logic = {login}")
            return None
        
        return res
    except:
        print("getUserByLogin, Ошибка получения данных из БД ")
    
    return None