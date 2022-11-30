from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
import json
app = FastAPI()

# conn = mysql.connector.connect(user='root', password='root', host='localhost', database='sakila', auth_plugin='mysql_native_password')
# cursor = conn.cursor()

@app.get('/')
async def root():
    return {'message': "Hello, world"}
