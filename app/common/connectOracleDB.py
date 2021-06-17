from app.common.pyOracle import connectToOracle
from app.common.flaskApp import app

# def connectOracleDB():
#     usrName = app.config['DB']['usrName']
#     password = app.config['DB']['password']
#     IP = app.config['DB']['IP']
#     port = app.config['DB']['port']
#     dbName = app.config['DB']['dbName']
#     return connectToOracle(usrName, password, IP, port, dbName)

def connectOracleDB():
    usrName = app.config['DB']['usrName']
    password = app.config['DB']['password']
    IP = app.config['DB']['IP']
    port = app.config['DB']['port']
    dbName = app.config['DB']['dbName']
    return connectToOracle(usrName, password, IP, port, dbName)