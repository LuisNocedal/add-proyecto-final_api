import mysql.connector
import psycopg2

def createQuery(query, data):
    connMysql = mysql.connector.connect(
        user='root', 
        password='$rdbaxolotech.0937.2022', 
        host='stack-rds-axolotech-e-comer-and-app-dev-rdsdb-nyfeg8ra2kys.cnmbtvnxnbpx.us-east-1.rds.amazonaws.com', 
        database='almacenes_de_datos', 
        auth_plugin='mysql_native_password'
    )
    cursorMysql = connMysql.cursor()

    cursorMysql.execute(query, data)
    connMysql.commit()

def createQueryOne(query, data):
    connMysql = mysql.connector.connect(
        user='root', 
        password='$rdbaxolotech.0937.2022', 
        host='stack-rds-axolotech-e-comer-and-app-dev-rdsdb-nyfeg8ra2kys.cnmbtvnxnbpx.us-east-1.rds.amazonaws.com', 
        database='almacenes_de_datos', 
        auth_plugin='mysql_native_password'
    )
    cursorMysql = connMysql.cursor()

    cursorMysql.execute(query, data)
    head = [i[0] for i in cursorMysql.description]
    res = cursorMysql.fetchone()
    # print(res)

    if res == None:
        return False

    return dict(zip(head, res))

def validateToken(token):
    token = createQueryOne("Select * From Sessions Where token = %s And End Is Null", [token])
    return token != False

def getAllTablesFromMysql(host, username, password, database):
    connMysql = mysql.connector.connect(
        user=username, 
        password=password, 
        host=host, 
        database=database, 
        auth_plugin='mysql_native_password'
    )
    cursorMysql = connMysql.cursor()

    cursorMysql.execute("SELECT table_name FROM information_schema.tables Where table_schema = %s", [ database ])
    headTables = [i[0] for i in cursorMysql.description]
    
    tables = []
    for row in cursorMysql.fetchall():
        tables.append(dict(zip(headTables, row)))

    totalInfo = []
    for table in tables:
        cursorMysql.execute("Select * From " + table["TABLE_NAME"] + " Limit 100")
        headInfo = [i[0] for i in cursorMysql.description]

        info = []
        for row in cursorMysql.fetchall():
            info.append(dict(zip(headInfo, row)))
        
        totalInfo.append({ "table_name": table['TABLE_NAME'], "data": info})

    return {"database": database, "data": totalInfo}

def getAllTablesFromPostgres(host, username, password, database):
    connMysql = psycopg2.connect('dbname=postgres user='+ username +' host=' +  host + ' password='+ password + '')
    cursorMysql = connMysql.cursor()

    cursorMysql.execute("SELECT table_name FROM information_schema.tables Where table_schema = %s", [ database ])
    headTables = [i[0] for i in cursorMysql.description]
    
    tables = []
    for row in cursorMysql.fetchall():
        tables.append(dict(zip(headTables, row)))

    # return tables

    totalInfo = []
    for table in tables:
        cursorMysql.execute('Select * From ' + database + '."' + table['table_name'] + '" Limit 100')
        headInfo = [i[0] for i in cursorMysql.description]

        info = []
        for row in cursorMysql.fetchall():
            info.append(dict(zip(headInfo, row)))
        
        totalInfo.append({ "table_name": table['table_name'], "data": info})

    return {"database": database, "data": totalInfo}
