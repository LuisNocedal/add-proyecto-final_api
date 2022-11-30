from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
import json
app = FastAPI()

# conn = mysql.connector.connect(user='root', password='root', host='localhost', database='sakila', auth_plugin='mysql_native_password')
# cursor = conn.cursor()

@app.get('/')
async def root():
    return {'data': [
        ["Year", "Sales", "Expenses", "Profit"],
        ["2014", 1000, 400, 200],
        ["2015", 1170, 460, 250],
        ["2016", 660, 1120, 300],
        ["2017", 1030, 540, 350],
    ]}
