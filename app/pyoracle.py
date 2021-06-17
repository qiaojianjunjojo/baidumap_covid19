#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cx_Oracle
import pandas as pd
from app.common.flaskApp import app


# from app.common.flaskApp import flaskApp
"""
  connet to Oracle
  
  帶變量SQL例子：
  sql = "SELECT * from wip_code where code_cate='%s' and code='%s' "%(code_cate, condit)
"""


class connectToOracle():

    def __init__(self, DBconfig):
        try:
            self.config = DBconfig
            self.conn = cx_Oracle.connect(DBconfig["usrName"], DBconfig["password"], DBconfig["IP"] + ":1521/" + DBconfig["dbName"],encoding ="UTF-8", nencoding="UTF-8",threaded=True)
            #self.conn = cx_Oracle.connect("%s/%s@%s/%s" % (DBconfig["userName"],DBconfig["password"],DBconfig["IP"],DBconfig["DBname"]))
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(e)
            print(f'{DBconfig["dbName"]}-{DBconfig["usrName"]}:DB连接失败')

    #  數據庫連接
    # encoding="UTF-8", nencoding="UTF-8" 解決中文亂碼問題
    def initOracleConnect(self):
        try:
            # oracle_tns = cx_Oracle.makedsn(self.IP, 1521, self.dbName)
            oracle_tns = self.IP + ":1521/" + self.dbName
            self.connectObj = cx_Oracle.connect(self.usrName, self.password, oracle_tns,encoding ="UTF-8", nencoding="UTF-8")
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
    """
    container异常crash后，改用sqlSelect2;此方法暂时停用 add by qjj20200723
    """
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
            print(str(e))
            print('Select sql error')
            self.closeOracleCursor(selectCursor)
            return pd.DataFrame({})

    def sqlSelect2(self, sql, *columns):
        try:
            columns = list(columns)  
            self.cursor.execute(sql)
            rs = self.cursor.fetchall()
            if len(columns) == 0:
                result = pd.DataFrame(rs)
            else:
                result = pd.DataFrame(rs,columns=columns[0])
            return result
        except Exception as e:
            print(str(e))
            print(f'{self.config["DBname"]}:sql执行报错!')
            return pd.DataFrame({})

    def __del__(self):
        if hasattr(self,"cursor"):
            self.cursor.close()
            #print('python解析器自動關閉cursor')
        if hasattr(self,"conn"):
            self.conn.close()
            #print('python解析器自動關閉conn')

    #
    # 1.方式二 搜索數據  返回dataframe
    # def sqlPdSelect(self, sql):
    #     connectObj = self.getOracleConnect()
    #     result = pd.read_sql(sql, connectObj)
    #     self.closeOracleCursor(selectCursor)
    #     return result

    #  update insert delete 數據  并且commit
    def sqlExecute(self, sql):
        try:
            selectCursor = self.getOracleCursor()
            selectCursor.execute(sql)
            self.getOracleConnect().commit()
            self.closeOracleCursor(selectCursor)
        except:
            print('Execute sql error')

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
