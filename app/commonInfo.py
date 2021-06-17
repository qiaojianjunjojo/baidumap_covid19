#!/usr/bin/env python
# coding: utf-8
from flask import Flask,jsonify,request
from app.common.pyOracle import connectToOracle
from app.common.commFunc import nulToStr,getAllMonths
from datetime import date,datetime
from dateutil.relativedelta import relativedelta

from app.common.flaskApp import app as configApp
from app import app

class CommonInfo():
    def __init__(self):
        self.THSAPDA1 = connectToOracle(configApp.config["THSAPDA1"])
        self.THAPMAPSDA1 = connectToOracle(configApp.config["THAPMAPSDA1"])
    # 人員登入計數

    def insertLoginLog(self):
        try:
            inputInfo = request.get_json()
            LoginLogSql = """
                insert into qpt_login_log(emp_id, emp_name, write_date)values('{0}', '{1}', sysdate)
                """.format(inputInfo['EmpID'], inputInfo['EmpName'])
            # print(LoginLogSql)
            self.THSAPDA1.sqlExecute(LoginLogSql)
            return 'Insert success'
        except Exception as e:
            return str(e)
            app.logger.error(str(e))

    def getLoginLog(self, EmpID):
        try:
            if EmpID != 'ALL':
                condition = f"where emp_id = '{EmpID}'"
            else:
                condition = ''
            LoginLogSql = """
            select emp_id, emp_name,count(*) cnt From qpt_login_log {0} group by emp_id, emp_name
            """.format(condition)
            LoginLogDf = self.THSAPDA1.sqlSelect(LoginLogSql)
            LoginLogList = []
            for index, row in LoginLogDf.iterrows():
                LoginLogDict = {}
                LoginLogDict['EMPID'] = nulToStr(row[0])
                LoginLogDict['EMPNAME'] = nulToStr(row[1])
                LoginLogDict['CNT'] = nulToStr(row[2])
                LoginLogList.append(LoginLogDict)

            return LoginLogList
        except Exception as e:
            app.logger.error(str(e))



    # 將備註信息寫入到數據庫 白血球, AERB, IMP, BOASorting
    def insertLeucocyteMommentInfo(self):
        try:
            inputInfo = request.get_json()
            MommentInfoCntSql = """
            select count(*) cnt from QPT_COMMENT_RECORD where BOARD_CATE ='{0}' and KEY1='{1}' and KEY2='{2}' and  KEY3='{3}'
            """.format(inputInfo['BOARD_CATE'], inputInfo['KEY1'], inputInfo['KEY2'],
             inputInfo['KEY3'])
            MommentInfoCntDf = self.THSAPDA1.sqlSelect(MommentInfoCntSql)
            if int(MommentInfoCntDf[0][0]) > 0 :
                MommentInfoSql = """
                update QPT_COMMENT_RECORD set COMMENT_INFO1='{4}', COMMENT_INFO2='{5}' 
                where  BOARD_CATE ='{0}' and KEY1='{1}' and KEY2='{2}' and  KEY3='{3}'
                """.format(inputInfo['BOARD_CATE'], inputInfo['KEY1'], inputInfo['KEY2'],
                inputInfo['KEY3'], inputInfo['COMMENT_INFO1'], inputInfo['COMMENT_INFO2'])
            else:
                MommentInfoSql = """
                insert into QPT_COMMENT_RECORD(board_cate, key1, key2, key3, comment_info1, comment_info2, update_time) 
                values('{0}','{1}','{2}','{3}','{4}','{5}',sysdate)
                """.format(inputInfo['BOARD_CATE'], inputInfo['KEY1'], inputInfo['KEY2'],
                inputInfo['KEY3'], inputInfo['COMMENT_INFO1'], inputInfo['COMMENT_INFO2'])
            self.THSAPDA1.sqlExecute(MommentInfoSql)
            return 'Insert success'
        except Exception as e:
            return str(e)
            app.logger.error(str(e))


    def FSAP_Number_Of_Hits(self):
        try:
            inputInfo = request.get_json()
            requestip = request.remote_addr


            LoginLogSql = """
                insert into FSMIS_NUMBER_OF_HIT(sysname,sysmodule,sysfun,empname, empno,ip,pcname, time)values('{0}','{1}','{2}','{3}','{4}','{5}','{6}', sysdate)
                """.format(inputInfo['SysName'],inputInfo['SysModule'],inputInfo['SysFunc'], inputInfo['EmpName'],inputInfo['EmpNo'],requestip,inputInfo['HostName'])
            #print(LoginLogSql)
            self.THAPMAPSDA1.sqlExecute(LoginLogSql)
            return 'Insert success'
        except Exception as e:
            return str(e)
            app.logger.error(str(e))

