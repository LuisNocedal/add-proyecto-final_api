from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
import hashlib
from datetime import datetime
import mysql.connector
from fastapi import Request
from middlewares.verify_token_route import VerifyTokenRoute
from helpers.functions import getAllTablesFromMysql, getAllTablesFromPostgres

dataRouter = APIRouter(prefix="/data", route_class=VerifyTokenRoute)

class Data(BaseModel):
    test: str

@dataRouter.post("/get-databases")
async def test(request: Request):
    data = await request.json()
    instances = data["instances"]

    instancesData = []

    for instance in instances:
        if(instance["type"] == "MySql"):
            tablesData = getAllTablesFromMysql(instance["host"], instance["username"], instance["password"], instance["database"])
            instancesData.append(tablesData)
            # for tableData in tablesData:
            #     instancesData.append(tableData)
        if(instance["type"] == "Postgres"):
            tablesData = getAllTablesFromPostgres(instance["host"], instance["username"], instance["password"], instance["database"])
            instancesData.append(tablesData)
            # for tableData in tablesData:
            #     instancesData.append(tableData)

    return { "status": True, "instancesData": instancesData }
