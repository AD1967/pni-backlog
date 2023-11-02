import base64                                           #
from datetime import datetime, timedelta                #
import os                                               #
from .db.model import User                              #
from werkzeug.security import generate_password_hash, check_password_hash   #
from .db import db


class UserLogin():
    # ТОКЕНЫ
    # Метод get_token() возвращает токен для пользователя. 
    # Токен генерируется как случайная строка. 
    # Перед созданием нового токена этот метод проверяет, есть ли 
    # у назначенного токена по крайней мере минута до истечения срока действия, 
    # и в этом случае возвращается существующий токен.
    @staticmethod
    def get_token(user, expires_in=86400):
        print(user.token)
        now = datetime.utcnow()
        if user.token_expiration > now + timedelta(seconds=60):
            return user.token
        user.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        user.token_expiration = now + timedelta(seconds=expires_in)
        db.session.commit()
        print(user.token)
        return user.token

    # Метод revoke_token() делает маркер, назначенный пользователю, недействительным, 
    # просто установив дату истечения срока действия на одну секунду до текущего времени.
    @staticmethod
    def revoke_token(user):
        user.token_expiration = datetime.utcnow() - timedelta(seconds=1)
    
    # Метод check_token() является статическим методом, 
    # который принимает токен в качестве входных данных и возвращает пользователя, 
    # которому этот токен принадлежит в качестве ответа. 
    # Если токен недействителен или истек, метод возвращает None.
    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    @staticmethod
    def check_password(user, password):
        return check_password_hash(user.password, password)