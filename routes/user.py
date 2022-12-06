from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
import hashlib
from datetime import datetime
from helpers.functions import createQuery, createQueryOne

loginRouter = APIRouter(prefix="/user")

class Login(BaseModel):
    username: str
    password: str

@loginRouter.post("/login")
async def login(login: Login):
    passhash = hashlib.md5(login.password.encode('utf-8')).hexdigest()

    user = createQueryOne("Select user_id, username, type From Users Where username=%s And password=%s", [login.username, passhash])

    if user == False:
        return {"status": False}

    token = hashlib.md5((login.password + login.username + datetime.now().strftime("%H:%M:%S")).encode('utf-8')).hexdigest()
    createQuery("Update Sessions Set end = %s Where user_id = %s And end Is NULL", [ datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user["user_id"] ])
    createQuery("Insert Into Sessions(user_id, token) Values(%s,%s)",[user["user_id"], token])
    
    return { "status": True, "user": user, 'token': token}