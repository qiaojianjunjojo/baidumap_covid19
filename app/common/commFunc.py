#!/usr/bin/env python
# coding: utf-8
from app.common.pyOracle import connectToOracle
import pandas as pd
from datetime import date,datetime,timedelta
from dateutil.relativedelta import relativedelta
import time

# 將None 轉化為空
def nulToStr(arg):
    if arg == None or pd.isnull(arg):
        arg=''
    return arg

# 將None 轉化為0
def nulToZero(arg):
    if arg == None or pd.isnull(arg):
        arg = 0
    return arg

# columnNameList顯示的欄位名稱，順序要與sql 中的欄位順序對應
def toList(data, columnNameList):
    subContentList = []
    for index,row in data.iterrows():
        subContentDict = {}
        i = 0
        for i in range(data.columns.size):
            subContentDict[columnNameList[i]] = nulToStr(row[i])
        subContentList.append(subContentDict)
        # print(subContentList)
    return subContentList

def toDict(data, columnNameList):
    subContentDict = {}
    for index,row in data.iterrows():
        subContentDict[row[1]] = nulToStr(row[2])
        # print(subContentList)
    return subContentDict

# 獲取一年的12個月
def getAllMonths(n = 0):
    last_year = str(datetime.now().year-n)
    months = []
    for x in range(1, 13):
        if x<10:
            x = '0'+ str(x)
        else:
            x = str(x)
        months.append(last_year+x)
    return months

def getEveryDay(beginDay=1,endDays=9):
    # 獲取每天的日期，默認8天
    dayslist = [datetime.strftime(date.today() + relativedelta(days=-x),'%Y%m%d') for x in range(beginDay,endDays)]
    return dayslist

def getTheLastDayofWeek(days = 28, beginFlag = 0, mondayFlay = True):
    # 獲取每週的最後一天，默認是4周
    # date.today() 當天日期
    
    # 當天是周几 datetime.weekday(date.today()) 
    # 周一不顯示本週數據
    lastDayList = []
    if mondayFlay:
        if int(time.strftime('%w')) == 1:
            # 多增加一周
            days = days + 7
        else:
            # 加上本週的最新一天
            lastDayList.append(datetime.strftime(date.today()-timedelta(beginFlag),'%Y%m%d'))
    else:
         # 加上本週的最新一天
        lastDayList.append(datetime.strftime(date.today()-timedelta(beginFlag),'%Y%m%d'))
    for day in range(1,days,7):
        lastDay = datetime.strftime(date.today()- timedelta(datetime.weekday(date.today()) + day),'%Y%m%d')
        lastDayList.append(lastDay)    
    # lastDayList = [datetime.strftime(date.today()- timedelta(datetime.weekday(date.today()) + x),'%Y%m%d') for x in range(1,days,7)]
    # 加上本週的最新一天
    # lastDayList.append(datetime.strftime(date.today()-timedelta(beginFlag),'%Y%m%d'))
    return  sorted(lastDayList,reverse=True)

def getTheLastDayOfMonth(months = 3, beginFlag=1, mondayFlay = True):

    # 獲取每月的最後一天
    # anydate.replace(day=28) 將每月設定為28天
    currentMonth = date.today().month #本月
    thisYear = date.today().year      #本年
    lastDayList = []
    if mondayFlay:
    # 每月的1日不顯示本月信息
        if date.today().day == 1:
            months += 1
        else:
            # 加上本月的最新一天
            lastDayList.append(datetime.strftime(date.today()-timedelta(beginFlag),'%Y%m%d'))
    else:
            # 加上本月的最新一天
        lastDayList.append(datetime.strftime(date.today()-timedelta(beginFlag),'%Y%m%d'))
    for month in range(currentMonth - months, currentMonth):
        # print(month)
        if month <= 0 :
            year = thisYear - 1*(months // 12)
            month = month + 12*(months // 12)
        else:
            year = thisYear
#             month = month if month > 0 else month + 12
        # print(year)
        anydate = date(year=year, month=month, day=1)
        nextMonth = anydate.replace(day=28) + timedelta(days=4)
        lastDayList.append(datetime.strftime(nextMonth - timedelta(days= nextMonth.day),'%Y%m%d') )
    # 加上本月的最新一天
    # lastDayList.append(datetime.strftime(date.today()-timedelta(beginFlag),'%Y%m%d'))
    return  sorted(lastDayList,reverse=True)

def getMonthWeekDays(monthBegin=0,mothEnd=12,weekBegin=0,weekEnd=4,dayBegin=0,dayEnd=7):
     # 獲取當前日期開始的倒數幾天
    days = [datetime.strftime(date.today() + relativedelta(days=-x),'%Y-%m-%d') for x in range(dayBegin,dayEnd)]
    # 獲取當前周開始的倒數幾周
    weeks = [datetime.strftime(date.today(),'%Y') + str(x) for x in [int(time.strftime("%W")) - x for x in range(weekBegin,weekEnd)]]
    # 獲取當前月份開始的倒數12個月
    months = [datetime.strftime(date.today() + relativedelta(months=-x), '%Y-%m') for x in range(monthBegin, mothEnd)]
    allKeys = months + days + weeks
    return allKeys
