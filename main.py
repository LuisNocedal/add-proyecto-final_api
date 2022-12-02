from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
import psycopg2

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# conn = mysql.connector.connect(user='root', password='root', host='localhost', database='sakila', auth_plugin='mysql_native_password')
# cursor = conn.cursor()

con = psycopg2.connect('dbname=postgres user=postgres host=database-postgres.cnmbtvnxnbpx.us-east-1.rds.amazonaws.com password=12345678')
cur = con.cursor()

@app.get('/')
async def root():
    cur.execute("SELECT * FROM almacenes_de_datos.users")
    user = cur.fetchall()
    return user
    # return {'data': [
    #     ["Year", "Sales", "Expenses", "Profit"],
    #     ["2014", 1000, 400, 200],
    #     ["2015", 1170, 460, 250],
    #     ["2016", 660, 1120, 300],
    #     ["2017", 1030, 540, 350],
    # ]}

class Login(BaseModel):
    username: str
    password: str

@app.post('/login')
async def login(login: Login):
    if login.username == "user1" and login.password == "1234":
        return {"status": True, "token": "12345678"}
    else:
        return {"status": False}
