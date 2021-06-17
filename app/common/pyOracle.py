#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cx_Oracle
import pymssql
import pandas as pd
from app import app
# from app.common.flaskApp import app

# from app.common.flaskApp import flaskApp
"""
  connet to Oracle
  
  帶變量SQL例子：
  sql = "SELECT * from wip_code where code_cate='%s' and code='%s' "%(code_cate, condit)
"""


class connectToOracle():

    # def __init__(self, userName, password, IP, Port, DBname):
    def __init__(self, DBConfig):

        # fkApp = flaskApp()

        self.connectObj = ""
        self.connCnt = 0
        self.cursorCnt = 0
        self.sqlList = []


        self.usrName = DBConfig['usrName']
        self.password = DBConfig['password']
        self.IP = DBConfig['IP']
        self.port = DBConfig['port']
        self.dbName = DBConfig['dbName']
        # self.initOracleConnect()

    #  數據庫連接
    # encoding="UTF-8", nencoding="UTF-8" 解決中文亂碼問題
    def initOracleConnect(self):
        try:
            # oracle_tns = cx_Oracle.makedsn(self.IP, 1521, self.dbName)
            oracle_tns = self.IP + ":1521/" + self.dbName
            self.connectObj = cx_Oracle.connect(self.usrName, self.password, oracle_tns,encoding="UTF-8", nencoding="UTF-8")
            print(oracle_tns)
            print(self.usrName)
            print(self.password)
            # if self.connCnt <= 0:
            #     self.connectObj = cx_Oracle.connect(self.usrName, self.password, oracle_tns)
            #     self.connCnt += 1
        except:
            print('connect to DB fail')

    #  取得數據庫連接
    def getOracleConnect(self):
        # self.initOracleConnect()
        return self.connectObj

    # 斷開數據庫連接
    def closeOracleConnect(self, connectObj):
        connectObj.close()
        self.connCnt -= 1

    # 獲取光標
    def getOracleCursor(self):
        self.initOracleConnect()
        self.cursorCnt += 1
        return self.connectObj.cursor()

    # 關閉光標
    def closeOracleCursor(self, cursorObj):
        cursorObj.close()
        self.cursorCnt -= 1
        # if self.cursorCnt <= 0:
        #     self.closeOracleConnect(self.connectObj)
        self.closeOracleConnect(self.connectObj)
    # 1.方式一 搜索數據 返回dataframe
    # def sqlSelect(self, sql):
    #     selectCursor = self.getOracleCursor()
    #     selectCursor.execute(sql)
    #     rs = selectCursor.fetchall()
    #     result = pd.DataFrame(rs)
    #     self.closeOracleCursor(selectCursor)
    #     return result
    # columns可用訪問得到的dataframe 各欄位屬性
    def sqlSelect(self, sql, *columns):
        try:
            columns = list(columns)  
            selectCursor = self.getOracleCursor()
            selectCursor.execute(sql)
            rs = selectCursor.fetchall()
            if len(columns) == 0:
                result = pd.DataFrame(rs)
            else:
                result = pd.DataFrame(rs,columns=columns[0])
            self.closeOracleCursor(selectCursor)
            return result   
        except Exception as e:
            # print(str(e))
            self.closeOracleCursor(selectCursor)
            app.logger.error(str(e))
    #
    # 1.方式二 搜索數據  返回dataframe
    # def sqlPdSelect(self, sql):
    #     connectObj = self.getOracleConnect()
    #     result = pd.read_sql(sql, connectObj)
    #     self.closeOracleCursor(selectCursor)
    #     return result

    #  update insert delete 數據  并且commit
    def sqlExecute(self, sql):
        selectCursor = self.getOracleCursor()
        selectCursor.execute(sql)
        self.getOracleConnect().commit()
        self.closeOracleCursor(selectCursor)

    #  將要執行的sql到存到列表中
    def addExecuteSQL(self, sql):
        return self.sqlList.append(sql)

    # 執行sql列表中的sql，並一起commit
    def allSqlExecute(self):
        selectCursor = self.getOracleCursor()
        if len(self.sqlList) == 0:
            return print('No sql execute')

        for sql in self.sqlList:
            selectCursor.execute(sql)
        self.getOracleConnect().commit()
        self.sqlList = []
        self.closeOracleCursor(selectCursor)


class connectToSqlServer():
    def __init__(self, DBConfig):
        # fkApp = flaskApp()
        self.connectObj =""
        self.sqlList = []
        self.usrName = DBConfig['usrName']
        self.password = DBConfig['password']
        self.IP = DBConfig['IP']
        # self.port = DBConfig['port']
        self.dbName = DBConfig['dbName']
    
    def initSqlServerConnect(self):
        try:
            self.connectObj = pymssql.connect(self.IP ,self.usrName, self.password, self.dbName)
        except:
            print('connect to DB fail')

    #  取得數據庫連接
    def getSqlServerConnect(self):
        return self.connectObj

    # 斷開數據庫連接
    def closeSqlServerConnect(self, connectObj):
        connectObj.close()

    # 獲取光標
    def getSqlServerCursor(self):
        self.initSqlServerConnect()
        return self.connectObj.cursor()

    # 關閉光標
    def closeSqlServerCursor(self,selectCursor):
        selectCursor.close()
        self.closeSqlServerConnect(self.connectObj)
    # 1.方式一 搜索數據 返回dataframe
    def sqlSelect(self, sql, *columns):
        try:
            columns = list(columns)  
            selectCursor = self.getSqlServerCursor()
            selectCursor.execute(sql)
            rs = selectCursor.fetchall()
            if len(columns) == 0:
                result = pd.DataFrame(rs)
            else:
                result = pd.DataFrame(rs,columns=columns[0])
            self.closeSqlServerCursor(selectCursor)
            return result
        except Exception as e:
            print(str(e))
            print('Select sql error')
            return pd.DataFrame({})

    #
    # 1.方式二 搜索數據  返回dataframe
    # def sqlPdSelect(self, sql):
    #     connectObj = self.getSqlServerConnect()
    #     result = pd.read_sql(sql, connectObj)
    #     self.closeSqlServerCursor(selectCursor)
    #     return result

    #  update insert delete 數據  并且commit
    def sqlExecute(self, sql):
        selectCursor = self.getSqlServerCursor()
        selectCursor.execute(sql)
        self.getSqlServerConnect().commit()
        self.closeSqlServerCursor(selectCursor)

    #  將要執行的sql到存到列表中
    def addExecuteSQL(self, sql):
        return self.sqlList.append(sql)

    # 執行sql列表中的sql，並一起commit
    def allSqlExecute(self):
        selectCursor = self.getSqlServerCursor()
        if len(self.sqlList) == 0:
            return print('No sql execute')

        for sql in self.sqlList:
            selectCursor.execute(sql)
        self.getSqlServerConnect().commit()
        self.sqlList = []
        self.closeSqlServerCursor(selectCursor)