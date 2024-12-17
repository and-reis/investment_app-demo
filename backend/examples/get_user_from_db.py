# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 14:42:42 2024

@author: Derson
"""
from sqlalchemy import text
from app.dbconfig import Database
from app.services.user import UserService
from app.schemas.user import UserResponse

db = Database()
session = db.get_session()

v_userid = 2

userdata = UserService.get_user_by_id(v_userid, session)

if userdata:    
    print(UserResponse.model_validate(userdata) )
else:
    print("Usuário não encontrado!")