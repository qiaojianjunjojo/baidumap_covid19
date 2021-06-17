使用百度地圖APi,輔助公司疫情防控。  
1.收集公司員工的住宅信息，用百度地圖API轉換成對應的經度緯度。
2.政府公佈疫情風險區，也轉換成對應的經度緯度。
3.將這些點描繪(Marker)在百度地圖上,在風險區範圍1km内的員工用不同的顔色標識。顔色區分是否接種疫苗等信息
4.防疫小组采取防疫措施：對這些風險内的員工 申請居家辦公。。。

前端主要使用到的技術：H5,C3,JS,Jquery,AJAx ,百度地圖
後端：python flask,sqlserver2008,Docker, CI/CD 

---

应用预览：
![Image text](https://github.com/qiaojianjunjojo/baidumap_covid19/blob/master/Covid19_map_web/images/1.PNG)

  
![Image text](https://github.com/qiaojianjunjojo/baidumap_covid19/blob/master/Covid19_map_web/images/2.PNG)
## 相關鏈接及注意事項
百度地圖API(https://lbsyun.baidu.com/index.php?title=jspopular3.0);裏面會有一些demo教你怎麽在html初始化一個map,怎麽在上面畫點。。。  
注意事項一：使用前需要先申請一个自己的服務密鑰.会使用在html ```<script>```中，不然你是看不到地图的。
注意事项二：坐标系。百度地图(BD09)用腾讯地图(GCJ02)产生出来的坐标定位会有偏差，一定要确保坐标系一致；
```
目前国内主要有以下三种坐标系：
WGS84：为一种大地坐标系，也是目前广泛使用的GPS全球卫星定位系统使用的坐标系。

GCJ02：又称火星坐标系，是由中国国家测绘局制订的地理信息系统的坐标系统。由WGS84坐标系经加密后的坐标系。

BD09：为百度坐标系，在GCJ02坐标系基础上再次加密。其中bd09ll表示百度经纬度坐标，bd09mc表示百度墨卡托米制坐标。

非中国地区地图，服务坐标统一使用WGS84坐标。
```

