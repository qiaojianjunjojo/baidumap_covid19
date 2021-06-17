#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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