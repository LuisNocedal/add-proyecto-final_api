from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
import hashlib
from datetime import datetime
import mysql.connector
from fastapi import Request
from middlewares.verify_token_route import VerifyTokenRoute
from helpers.functions import getAllTablesFromMysql, getAllTablesFromPostgres
from fastapi.responses import JSONResponse

dataRouter = APIRouter(prefix="/data", route_class=VerifyTokenRoute)

class Data(BaseModel):
    test: str

@dataRouter.post("/get-databases")
async def test(request: Request):
    try:
        data = await request.json()
        instances = data["instances"]

        instancesData = []

        try:
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
        except:
            return JSONResponse(content={"message": "No se ha podido conectar a alguna de las instancias"}, status_code=404)

        return { "status": True, "instancesData": instancesData }
    except:
        return JSONResponse(content={"message": "Ha habido un error en el servidor"}, status_code=500)
