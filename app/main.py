#!/usr/bin/env python
# coding: utf-8
from flask import Flask,jsonify,request,render_template,send_file,make_response
from app.common.pyOracle import connectToOracle
from app.common.commFunc import toList
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
from flask_cors import CORS
from app.common.flaskApp import app as configApp
from app import app
from flasgger import Swagger
from app.common.logs import Logger

from app.commonInfo import CommonInfo
from app.covid19Info import Covid19Info

import flask_monitoringdashboard as dashboard

dashboard.config.database_name = 'sqlite:///db/flask_monitoringdashboard.db'
#dashboard.bind(app) #api点击率监控

app.config['JSON_SORT_KEYS'] = False  #返回json格式時，取消自動按照字母排序
CORS(app)
Swagger(app)
log = Logger(app)


@app.route('/FSAP_Number_Of_Hits_Api/', methods=['POST'])
@log.writeLog()
def FSAP_Number_Of_Hits():
    """
    佛山MIS公用功能，將系統登入寫入到數據庫中
    ---
    tags:
      - 公用功能
    produces: application/json,
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - SysName
            - EmpName
            - EmpNo

          properties:
            SysName:
                type: string
                description: 系統名稱
                example: "INT-PORTAL"
            SysModule:
                type: string
                description: 系統模塊
                example: "登入功能"
            SysFunc:
                type: string
                description: 系統方程式
                example: "登入功能"
            EmpName:
                type: string
                description: 名稱
                example: "陳小明"
            EmpNo:
                type: string
                description: 工號
                example: "210007"
            HostName:
                type: string
                description: 電腦名稱
                example: "HA8969517"

    responses:
      200:
          description: success
      406:
          description: Unauthorized error

    """

    obj = CommonInfo()
    retMessage = obj.FSAP_Number_Of_Hits()
    resp = jsonify({"RetMsg": retMessage})
    return resp


@app.route('/getEmpLocationApi', methods=['GET'])  
@log.writeLog(detail=True)
def getEmpLocation():
  """
  data :　獲取人員居住地址/疫苗接種信息(資料來源 Smooth)
  ---
  tags:
    - 疫情防控功能 
  produces: application/json,

  responses:
    200:
        description: success
    406:
        description: Unauthorized error
  
  """
  #type = request.args.get('type')
  obj = Covid19Info()
  info = obj.getEmpLocation()
  return jsonify({"data": info})


@app.route('/getHighRiskAreaApi', methods=['GET'])  
@log.writeLog(detail=True)
def getHighRiskArea():
  """
  data : 獲取風險區域
  ---
  tags:
    - 疫情防控功能 
  produces: application/json,

  responses:
    200:
        description: success
    406:
        description: Unauthorized error
  
  """
  obj = Covid19Info()
  info = obj.getHighRiskArea()
  return jsonify({"data": info})


@app.route('/getPeopleInRiskAreaApi', methods=['GET'])  
@log.writeLog(detail=True)
def getPeopleInRiskArea():
  """
  data : 獲取人員居住地在風險區域範圍內
  ---
  tags:
    - 疫情防控功能
  produces: application/json,
  parameters:
        - name: dis
          in: query
          type: array
          description: 風險區域距離設定
          items:
            type: string
            enum: ['1','2','3'] 
  produces: application/json,
  responses:
    200:
        description: success
    406:
        description: Unauthorized error
  
  """
  dis = request.args.get('dis')
  obj = Covid19Info()
  info = obj.getPeopleInRiskArea(int(dis))
  return jsonify({"data": info})



