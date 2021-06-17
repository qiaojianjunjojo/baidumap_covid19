#!/usr/bin/env python
# coding: utf-8
from flask import Flask,jsonify,request
from numpy.lib.function_base import append
from app.common.pyOracle import connectToOracle
from app.common.commFunc import nulToStr,getAllMonths
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
from app.common.flaskApp import app as configApp
from app import app
import pandas as pd
import math
from app.common.pySQLConnect import connectToSqlServer
class Covid19Info():
    def __init__(self):
        self.THSAPDA1 = connectToOracle(configApp.config["THSAPDA1"])
        self.THAPMAPSDA1 = connectToOracle(configApp.config["THAPMAPSDA1"])
        self.PHSAPDA1 = connectToOracle(configApp.config["PHSAPDA1"])
        self.SmoothHR = connectToSqlServer(configApp.config['SMOOTHHR'])

        

    #取得員工基本資料
    def getEmpLocation(self):
        try:

            #SQL
            datasql = """
                    select 
                    e.empno empno,
                    e.name name,
                    case
                    when o.level6 is not null then o.level6
                    when o.level5 is not null then o.level5
                    when o.level4 is not null then o.level4
                    when o.level7 is not null then o.level7
                    else null
                    end dept,
                    j.description job,
                    t.name title,
                    case e.indirect
                    when 'I' then '間接'
                    when 'D' then '直接'
                    end indirect,
                    e.address,
                    g.longitude,
                    g.latitude,
                    case g.precise
                    when 1 then '精確打點'
                    when 0 then '模糊打點'
                    end precise,
                    g.confidence,
                    g.comprehension,
                    i.Inoculationdate firstInoculationdate,
                    i2.InoculationDate secondInoculationdate
                    from 
                    corpemployee e
                    left join corporganization_bz_fact o on o.orgid = e.workorgid
                    left join corpjob j on j.id = e.jobid
                    left join corptitle t on t.id = e.titleid
                    left join Covid19_GPS g on g.empno = e.empno
                    left join InoculaitonLog i on e.empno = i.empno and i.Description = '第一劑'
                    left join InoculaitonLog i2 on e.empno = i2.empno and i2.Description = '第二劑'
                    where 
                    e.empstatus = 'E0F061BA-6C05-4019-81D1-5AFC295FAC15'
                    and e.corporation is not null
                    and e.empno not like 'X%'
                    and e.empno not like 'W%'
                    and e.empno not like 'C%'
                    and e.empno not like '4%'
                    and g.longitude is not null
					and g.latitude is not null
                
                    order by e.empno
            """
            dataDf = self.SmoothHR.sqlSelect(datasql,['empno','name','dept','job','title','indirect','address','longitude','latitude','precise','confidence','comprehension','firstInoculationdate','secondInoculationdate'])

            rsall = []
            for index, row in dataDf.iterrows():
                #本地調適出現亂碼 加入 .encode('latin1').decode('cp950')
                rs = {}
                rs['emp_no'] = nulToStr(row['empno'])
                rs['emp_name'] = nulToStr(row['name'])
                rs['dept'] = nulToStr(row['dept'])
                rs['job'] = nulToStr(row['job'])
                rs['title'] = nulToStr(row['title'])
                rs['indirect'] = nulToStr(row['indirect'])
                rs['address'] = nulToStr(row['address'])
                rs['longitude'] = nulToStr(float(row['longitude']))
                rs['latitude'] = nulToStr(float(row['latitude']))
                rs['precise'] = nulToStr(row['precise'])
                rs['confidence'] = nulToStr(row['confidence'])
                rs['comprehension'] = nulToStr(row['comprehension'])

                rs['firstInoculationdate'] = nulToStr(row['firstInoculationdate'])
                rs['secondInoculationdate'] = nulToStr(row['secondInoculationdate'])

                if rs['firstInoculationdate'] == "":
                    rs['vaccination'] = False
                else:
                    rs['vaccination'] = True     

                #透過經緯度，判斷人員是否在閉環區域

                #封閉區域座標
                closeAreapointList = [(113.146865, 23.078419),
                                    (113.148177, 23.106859),
                                    (113.138515, 23.150982),
                                    (113.153216, 23.138603),
                                    (113.172467, 23.136427),
                                    (113.166484, 23.151256),
                                    (113.18012, 23.184281),
                                    (113.184414, 23.220437),
                                    (113.173778, 23.235282),
                                    (113.187001, 23.238901),
                                    (113.199991, 23.211054),
                                    (113.21413, 23.197752),
                                    (113.216574, 23.182952),
                                    (113.188439, 23.15428),
                                    (113.194404, 23.147301),
                                    (113.217688, 23.147301),
                                    (113.215406, 23.131766),
                                    (113.223167, 23.095901),
                                    (113.216178, 23.089552),
                                    (113.182833, 23.083335),
                                    (113.184576, 23.072363),
                                    (113.217005, 23.049021),
                                    (113.256818, 23.04528),
                                    (113.273329, 23.03265),
                                    (113.255309, 22.984233),
                                    (113.222682, 23.012477),
                                    (113.180498, 22.997175),
                                    (113.145859, 23.033931),
                                    (113.122674, 23.072513)]

                isInclosearea =  self.IsPtInPoly(float(row['longitude']),float(row['latitude']),closeAreapointList) 
                rs["isInclosearea"] = isInclosearea

                #閉環區域驗證
                #isInclosearea =  self.IsPtInPoly(23.116196,113.179671,closeAreapointList) 
                #isInclosearea =  self.IsPtInPoly(23.081462,113.160123,closeAreapointList) 
                #isInclosearea =  self.IsPtInPoly(23.060332,113.148224,closeAreapointList) 
                

                

                #群創光電佛山廠區座標                
                #左上 右上 右下 左下
                pointList = [(112.983061,23.21487),(112.993006,23.214413),(112.99376,23.20596),(112.980932,23.207181)]
                #判斷是否座標是否在公司區域
                isInArea = self.IsPtInPoly(float(row['longitude']),float(row['latitude']),pointList) 
                rs['isINCompany'] = nulToStr(isInArea)

                if isInArea:
                    continue   

                #rs['CREATEDATE'] = row['CREATEDATE']
                #rs['TYPE'] = nulToStr(row['TYPE'])
                rsall.append(rs)


        except Exception as e:
            return str(e)
            app.logger.error(str(e))        

        return rsall


    #取得高風險區域資料
    def getHighRiskArea(self):
        try:
            #取得高風險區域資料
            locationSql = """ SELECT * FROM COVID19_RISKAREA"""
            locationdf = self.THAPMAPSDA1.sqlSelect(locationSql,['LOCATION','GSPLOCATION'])

            rsall = []
            for index, row in locationdf.iterrows():
                rs = {}
                rs['LOCATION'] = nulToStr(row['LOCATION'])
                splitrs = row['GSPLOCATION'].split(",")
                rs['LONGITUDE'] = nulToStr(float(splitrs[0]))
                rs['DIMENSIONS'] = nulToStr(float(splitrs[1]))
                rsall.append(rs)

        except Exception as e:
            return str(e)
            app.logger.error(str(e))        

        return rsall


    #判斷人員是否在高風險區域
    def getPeopleInRiskArea(self,riskDistance = 1):
        #取得高風險區域資料
        locationSql = """ SELECT * FROM COVID19_RISKAREA"""
        highRisklocationdf = self.THAPMAPSDA1.sqlSelect(locationSql,['LOCATION','GSPLOCATION'])


        #SQL
        datasql = """
                select 
                e.empno empno,
                e.name name,
                case
                when o.level6 is not null then o.level6
                when o.level5 is not null then o.level5
                when o.level4 is not null then o.level4
                when o.level7 is not null then o.level7
                else null
                end dept,
                j.description job,
                t.name title,
                case e.indirect
                when 'I' then '間接'
                when 'D' then '直接'
                end indirect,
                e.address,
                g.longitude,
                g.latitude,
                case g.precise
                when 1 then '精確打點'
                when 0 then '模糊打點'
                end precise,
                g.confidence,
                g.comprehension,
                i.Inoculationdate firstInoculationdate,
                i2.InoculationDate secondInoculationdate
                from 
                corpemployee e
                left join corporganization_bz_fact o on o.orgid = e.workorgid
                left join corpjob j on j.id = e.jobid
                left join corptitle t on t.id = e.titleid
                left join Covid19_GPS g on g.empno = e.empno
                left join InoculaitonLog i on e.empno = i.empno and i.Description = '第一劑'
                left join InoculaitonLog i2 on e.empno = i2.empno and i2.Description = '第二劑'
                where 
                e.empstatus = 'E0F061BA-6C05-4019-81D1-5AFC295FAC15'
                and e.corporation is not null
                and e.empno not like 'X%'
                and e.empno not like 'W%'
                and e.empno not like 'C%'
                and e.empno not like '4%'
                and g.longitude is not null
                and g.latitude is not null
            
                order by e.empno
        """
        dataDf = self.SmoothHR.sqlSelect(datasql,['empno','name','dept','job','title','indirect','address','longitude','latitude','precise','confidence','comprehension','firstInoculationdate','secondInoculationdate']) 

        rsall = []
        for _, row in dataDf.iterrows():
            for _,row2 in highRisklocationdf.iterrows():
                jd,wd = row2['GSPLOCATION'].split(',')
                #將bd09座標系轉成gcj02 因為健康中心目前使用高德地圖取經緯度
                pljd,plwd = self.bd09_to_gcj02(float(row['longitude']),float(row['latitude']))

                distance =  self.getDistance(plwd,pljd,float(jd),float(wd))
                if distance <= riskDistance:
                    rs = {}
                    rs['emp_no'] = nulToStr(row['empno'])
                    rs['emp_name'] = nulToStr(row['name'])
                    rs['emp_addr'] = nulToStr(row['address'])
                    rs['LONGITUDE'] = nulToStr(float(row['longitude']))
                    rs['DIMENSIONS'] = nulToStr(float(row['latitude']))
                    rs['precise'] = nulToStr(row['precise'])
                    rs['confidence'] = nulToStr(row['confidence'])
                    rs['riskarea'] = nulToStr(row2['LOCATION'])
                    rs['firstInoculationdate'] = nulToStr(row['firstInoculationdate'])
                    if rs['firstInoculationdate'] == "":
                        rs['vaccination'] = False
                    else:
                        rs['vaccination'] = True  
                    
                    rsall.append(rs)
                    break
        print(rsall)
        return rsall
 
        




    def IsPtInPoly(self,aLon, aLat, pointList):
        '''
        :param aLon: double 经度
        :param aLat: double 纬度
        :param pointList: list [(lon, lat)...] 多边形点的顺序需根据顺时针或逆时针，不能乱
        '''
        
        iSum = 0
        iCount = len(pointList)
        
        if(iCount < 3):
            return False
        
        
        for i in range(iCount):
            
            pLon1 = pointList[i][0]
            pLat1 = pointList[i][1]
            
            if(i == iCount - 1):
                
                pLon2 = pointList[0][0]
                pLat2 = pointList[0][1]
            else:
                pLon2 = pointList[i + 1][0]
                pLat2 = pointList[i + 1][1]
            
            if ((aLat >= pLat1) and (aLat < pLat2)) or ((aLat>=pLat2) and (aLat < pLat1)):
                
                if (abs(pLat1 - pLat2) > 0):
                    
                    pLon = pLon1 - ((pLon1 - pLon2) * (pLat1 - aLat)) / (pLat1 - pLat2);
                    
                    if(pLon < aLon):
                        iSum += 1
    
        if(iSum % 2 != 0):
            return True
        else:
            return False


    # 計算距離
    def getDistance(self,latA, lonA, latB, lonB):
        ra = 6378140  # 赤道半徑
        rb = 6356755  # 極半徑
        flatten = (ra - rb) / ra  # Partial rate of the earth
        # change angle to radians
        radLatA = math.radians(latA)
        radLonA = math.radians(lonA)
        radLatB = math.radians(latB)
        radLonB = math.radians(lonB)

        pA = math.atan(rb / ra * math.tan(radLatA))
        pB = math.atan(rb / ra * math.tan(radLatB))
        x = math.acos(math.sin(pA) * math.sin(pB) + math.cos(pA) * math.cos(pB) * math.cos(radLonA - radLonB))
        c1 = (math.sin(x) - x) * (math.sin(pA) + math.sin(pB)) ** 2 / math.cos(x / 2) ** 2
        c2 = (math.sin(x) + x) * (math.sin(pA) - math.sin(pB)) ** 2 / math.sin(x / 2) ** 2
        dr = flatten / 8 * (c1 - c2)
        distance = ra * (x + dr)
        distance = round(distance / 1000, 4)
        return distance


    def bd09_to_gcj02(self,bd_lon, bd_lat):
        """
        百度坐标系(BD-09)转火星坐标系(GCJ-02)
        百度——>谷歌、高德
        :param bd_lat:百度坐标纬度
        :param bd_lon:百度坐标经度
        :return:转换后的坐标列表形式
        """
        x_pi = 3.14159265358979324 * 3000.0 / 180.0

        x = bd_lon - 0.0065
        y = bd_lat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
        gg_lng = z * math.cos(theta)
        gg_lat = z * math.sin(theta)
        return [gg_lng, gg_lat]