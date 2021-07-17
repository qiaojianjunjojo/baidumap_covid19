## 项目target:借助百度地圖APi,輔助公司进行数字化疫情防控。  
  
主要实现步骤：  

1.收集公司員工的住宅信息(一般人事信息系统都会有);使用百度地圖API将住址信息轉換成對應的經度緯度。ex:北京市海淀区上地10街 => {lng(经度):103.254511,lat(纬度):23.54881}  
  
2.政府会公佈疫情風險區，也将其轉換成對應的經度緯度。  
  
3.將這些點描繪(Marker)在百度地圖上,在風險區範圍1km内的員工用不同的顔色標識,同时也區分是否接種疫苗等信息；(不在风险区内的显示绿色图标，在风险区内接种疫苗显示蓝色，在风险区内未接种疫苗显示橘色，风险区显示红色)  
  
4.前端要知道哪些点在不在风险区内其实是后端根据这些点的坐标去计算出来的，并将数据返回给前端；(func:getPeopleInRiskArea);  
  
5.本应用还有另外一个功能：可以计算任意封闭区域内，哪些员工在区域内；具体的做法可以参考func:IsPtInPoly，对应的数学模型就是在平面坐标系内，如何去判断一个点是否在任意一个多边形内部  
  
6.最后有了这些名单后，防疫小组就可以采取一些防疫措施；ex:为風險内的員工申請居家辦公、核酸检测证明等等  
  
## solution stack
前端：H5,C3,JS,Jquery,AJAx ,百度地圖api  
  
後端：python3 flask ,swagger,Docker,container, CI/CD 

---

应用预览：
![Image text](https://github.com/qiaojianjunjojo/baidumap_covid19/blob/master/Covid19_map_web/images/1.PNG)

  
![Image text](https://github.com/qiaojianjunjojo/baidumap_covid19/blob/master/Covid19_map_web/images/2.PNG)
## 相關鏈接及注意事項
百度地圖API(https://lbsyun.baidu.com/index.php?title=jspopular3.0)  
  
如何判断一个点是否在多边形内部(https://www.cnblogs.com/luxiaoxun/p/3722358.html)  
  
注意事項一：使用前需要先申請一个自己的服務密鑰.会使用在html ```<script src =XXXak=?>```中，不然你是看不到地图的。  
  
注意事项二：坐标系一致性。  
百度地图(BD09)用腾讯地图(GCJ02)产生出来的坐标定位会有偏差，一定要确保坐标系一致；  
```
目前国内主要有以下三种坐标系：
WGS84：为一种大地坐标系，也是目前广泛使用的GPS全球卫星定位系统使用的坐标系。

GCJ02：又称火星坐标系，是由中国国家测绘局制订的地理信息系统的坐标系统。由WGS84坐标系经加密后的坐标系。

BD09：为百度坐标系，在GCJ02坐标系基础上再次加密。其中bd09ll表示百度经纬度坐标，bd09mc表示百度墨卡托米制坐标。

非中国地区地图，服务坐标统一使用WGS84坐标。
```

