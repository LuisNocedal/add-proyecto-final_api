from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import hashlib
from datetime import datetime

from routes.user import loginRouter
from routes.data import dataRouter

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

con = psycopg2.connect('dbname=postgres user=postgres host=database-postgres.cnmbtvnxnbpx.us-east-1.rds.amazonaws.com password=12345678')
cur = con.cursor()

@app.get('/')
async def root():
    # return {
    #     "status": True
    # }
    cur.execute("SELECT * FROM almacenes_de_datos.users")

    head = [i[0] for i in cur.description]
    
    user = []
    for row in cur.fetchall():
        user.append(dict(zip(head, row)))

    return user
    # return {'data': [
    #     ["Year", "Sales", "Expenses", "Profit"],
    #     ["2014", 1000, 400, 200],
    #     ["2015", 1170, 460, 250],
    #     ["2016", 660, 1120, 300],
    #     ["2017", 1030, 540, 350],
    # ]}

app.include_router(loginRouter)
app.include_router(dataRouter)
