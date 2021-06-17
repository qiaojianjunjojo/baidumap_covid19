$(function () {
    //添加控件和比例尺
    function main(distance, number) {
        var map = new BMap.Map("allmap");
        map.centerAndZoom(new BMap.Point(113.15989144423916, 23.07016845200719), 13);
        map.enableScrollWheelZoom(true); //開啓鼠標滾輪功能；
        var top_left_control = new BMap.ScaleControl({
            anchor: BMAP_ANCHOR_TOP_LEFT
        }); // 左上角，添加比例尺
        var top_left_navigation = new BMap.NavigationControl(); //左上角，添加默认缩放平移控件
        var top_right_navigation = new BMap.NavigationControl({
            anchor: BMAP_ANCHOR_TOP_RIGHT,
            type: BMAP_NAVIGATION_CONTROL_SMALL
        }); //右上角，仅包含平移和缩放按钮
        /*缩放控件type有四种类型:
        BMAP_NAVIGATION_CONTROL_SMALL：仅包含平移和缩放按钮；BMAP_NAVIGATION_CONTROL_PAN:仅包含平移按钮；BMAP_NAVIGATION_CONTROL_ZOOM：仅包含缩放按钮*/
        map.addControl(top_left_control);
        map.addControl(top_left_navigation);
        map.addControl(top_right_navigation);

        var chkRadio = $('input:radio[name="type"]:checked').val();
        if (chkRadio == '1') {
            const lowriskman = localStorage.getItem('lowRiskEmpee') ? JSON.parse(localStorage.getItem('lowRiskEmpee')) : undefined;
            var date = new Date().getTime();
            if (lowriskman && (date - lowriskman.startTime < lowriskman.expires)) {
                paintPoint(lowriskman.data)
            } else {
                localStorage.getItem('lowRiskEmpee') && localStorage.removeItem('lowRiskEmpee');
                $.ajax({
                    type: "get",
                    // url: "http://10.189.127.62:40025/getEmpLocationApi",
                    url: "./testJSON/Empee.json",
                    success: function (data) {
                        const newData = data["data"];
                        const options = {
                            data: newData,
                            expires: 1000 * 60 * 60 * 6, //過期時間6小時
                            startTime: new Date().getTime() //记录何时将值存入缓存，毫秒级
                        }
                        localStorage.setItem('lowRiskEmpee', JSON.stringify(options));
                        paintPoint(newData)
                    }
                });
            }

            function paintPoint(dataset) {
                const safepeople = dataset.filter(item => !item.isInclosearea)
                const myIcongreen = new BMap.Icon("./images/green.png", new BMap.Size(26, 26));
                // const c = new Convertor();
                for (let i = 0; i < safepeople.length; i++) {
                    if (i == number) break
                    // const res = c.GCJ2BD09({
                    //     lng: dataset[i].DIMENSIONS,
                    //     lat: dataset[i].LONGITUDE
                    // });
                    // const point = new BMap.Point(res.lng, res.lat);
                    const point = new BMap.Point(safepeople[i].longitude, safepeople[i].latitude);
                    const marker = new BMap.Marker(point, {
                        icon: myIcongreen
                    });
                    map.addOverlay(marker);
                    marker.addEventListener('click', function () {
                        this.openInfoWindow(new BMap.InfoWindow(safepeople[i].emp_no + ',' + safepeople[i].emp_name + ',' + safepeople[i].address));
                    });
                }
            }

            //危險地區，以病毒為園星半徑 r=distance km畫個圓圈 
            function paintRedPoint(dataset) {
                const c = new Convertor();
                for (let i = 0; i < dataset.length; i++) {
                    const res = c.GCJ2BD09({
                        lng: dataset[i].DIMENSIONS,
                        lat: dataset[i].LONGITUDE
                    });
                    const point = new BMap.Point(res.lng, res.lat);
                    const marker = new BMap.Marker(point);
                    map.addOverlay(marker);
                    marker.addEventListener('click', function () {
                        this.openInfoWindow(new BMap.InfoWindow(dataset[i].LOCATION));
                    });
                    const circle = new BMap.Circle(point, distance * 1000, {
                        strokeColor: "red",
                        strokeWeight: 2,
                        strokeOpacity: 0.3,
                    });
                    map.addOverlay(circle);
                }
            }

            const virusLocation = localStorage.getItem('pubRiskAera') ? JSON.parse(localStorage.getItem('pubRiskAera')) : undefined;
            var date = new Date().getTime();
            if (virusLocation && (date - virusLocation.startTime < virusLocation.expires)) {
                paintRedPoint(virusLocation.data)
            } else {
                $.ajax({
                    type: "get",
                    // url: "http://10.189.127.62:40025/getHighRiskAreaApi",
                    url: './testJSON/publicRIskAera.json',
                    success: function (data) {
                        const newData = data["data"];
                        const options = {
                            data: newData,
                            expires: 1000 * 60 * 60 * 6, //過期時間6小時
                            startTime: new Date().getTime() //记录何时将值存入缓存，毫秒级
                        }
                        localStorage.setItem('pubRiskAera', JSON.stringify(options));
                        paintRedPoint(newData)
                    }
                });
            }

            //高風險地圖人員繪製; add:高風險地區内人員需要區分是否有打疫苗
            function paintYellowPoint(dataset) {
                $('#overlay').css({
                    'display': 'none',
                    'opacity': '0'
                })
                // const c = new Convertor();
                const vaccination = dataset.filter(item => item.vaccination)
                const myIconblue = new BMap.Icon("./images/blue.png", new BMap.Size(26, 26));
                for (let i = 0; i < vaccination.length; i++) {
                    // const res = c.GCJ2BD09({
                    //     lng: dataset[i].DIMENSIONS,
                    //     lat: dataset[i].LONGITUDE
                    // });
                    const point = new BMap.Point(vaccination[i].LONGITUDE, vaccination[i].DIMENSIONS);
                    const marker = new BMap.Marker(point, {
                        icon: myIconblue
                    });
                    map.addOverlay(marker);
                    marker.addEventListener('click', function () {
                        this.openInfoWindow(new BMap.InfoWindow(vaccination[i].emp_no + ',' + vaccination[i].emp_name + ' 風險區域：' + vaccination[i].riskarea + 'Address:' + vaccination[i].emp_addr));
                    });
                }
                const unvaccination = dataset.filter(item => !item.vaccination)
                $('#numberofRighrisk').text(dataset.length)
                $('#number1').text(vaccination.length)
                $('#number2').text(unvaccination.length)
                const myIconYellow = new BMap.Icon("./images/yellow.png", new BMap.Size(26, 26));
                for (let i = 0; i < unvaccination.length; i++) {
                    // const res = c.GCJ2BD09({
                    //     lng: dataset[i].DIMENSIONS,
                    //     lat: dataset[i].LONGITUDE
                    // });
                    const point = new BMap.Point(unvaccination[i].LONGITUDE, unvaccination[i].DIMENSIONS);
                    const marker = new BMap.Marker(point, {
                        icon: myIconYellow
                    });
                    map.addOverlay(marker);
                    marker.addEventListener('click', function () {
                        this.openInfoWindow(new BMap.InfoWindow(unvaccination[i].emp_no + ',' + unvaccination[i].emp_name + ' 風險區域：' + unvaccination[i].riskarea + 'Address:' + unvaccination[i].emp_addr));
                    });
                }

                var col = ['工號', '姓名', '風險區'];
                var table = document.getElementById('highriskman');
                table.innerHTML = "";
                // Create table header row using the extracted headers above.
                var tr = table.insertRow(-1); // table row
                for (var i = 0; i < col.length; i++) {
                    var th = document.createElement("th"); // table header.
                    th.innerHTML = col[i];
                    th.style.textAlign = 'center';
                    th.style.position = 'sticky';
                    th.style.top = 0;
                    tr.appendChild(th);
                }
                for (var i = 0; i < unvaccination.length; i++) {
                    tr = table.insertRow(-1);
                    if (i == 10) { //只展示10笔数据
                        for (var j = 0; j < 3; j++) {
                            var tabCell = tr.insertCell(-1);
                            tabCell.innerHTML = '...';
                        }
                        break
                    }
                    for (var item in unvaccination[i]) {
                        if (item == 'emp_no' || item == 'emp_name' || item == 'riskarea') {
                            var tabCell = tr.insertCell(-1);
                            tabCell.innerHTML = unvaccination[i][item];
                        }
                    }
                }

            }

            const highriskman = localStorage.getItem('highRiskEmpee' + distance) ? JSON.parse(localStorage.getItem('highRiskEmpee' + distance)) : undefined;
            var date = new Date().getTime();
            if (highriskman && (date - highriskman.startTime < highriskman.expires)) {
                paintYellowPoint(highriskman.data)
            } else {
                localStorage.getItem('highRiskEmpee' + distance) && localStorage.removeItem('highRiskEmpee' + distance);
                $.ajax({
                    type: "get",
                    // url: "http://10.189.127.62:40025/getPeopleInRiskAreaApi?dis=" + distance,
                    url: './testJSON/highriskempee.json',
                    success: function (data) {
                        const newData = data["data"];
                        const options = {
                            data: newData,
                            expires: 1000 * 60 * 60 * 6, //過期時間6小時
                            startTime: new Date().getTime() //记录何时将值存入缓存，毫秒级
                        }
                        localStorage.setItem('highRiskEmpee' + distance, JSON.stringify(options));
                        paintYellowPoint(newData)
                    }
                });
            }

        } else {
            //任意 多边形覆盖物 
            const polygon = new BMap.Polygon([
                new BMap.Point(113.146865, 23.078419),
                new BMap.Point(113.148177, 23.106859),
                new BMap.Point(113.138515, 23.150982),
                new BMap.Point(113.153216, 23.138603),
                new BMap.Point(113.172467, 23.136427),

                new BMap.Point(113.166484, 23.151256),
                new BMap.Point(113.18012, 23.184281),
                new BMap.Point(113.184414, 23.220437),
                new BMap.Point(113.173778, 23.235282),
                new BMap.Point(113.187001, 23.238901),

                new BMap.Point(113.199991, 23.211054),
                new BMap.Point(113.21413, 23.197752),
                new BMap.Point(113.216574, 23.182952),
                new BMap.Point(113.188439, 23.15428),
                new BMap.Point(113.194404, 23.147301),

                new BMap.Point(113.217688, 23.147301),
                new BMap.Point(113.215406, 23.131766),
                new BMap.Point(113.223167, 23.095901),
                new BMap.Point(113.216178, 23.089552),
                new BMap.Point(113.182833, 23.083335),

                new BMap.Point(113.184576, 23.072363),
                new BMap.Point(113.217005, 23.049021),
                new BMap.Point(113.256818, 23.04528),
                new BMap.Point(113.273329, 23.03265),
                new BMap.Point(113.255309, 22.984233),

                new BMap.Point(113.222682, 23.012477),
                new BMap.Point(113.180498, 22.997175),
                new BMap.Point(113.145859, 23.033931),
                new BMap.Point(113.122674, 23.072513)
            ], {
                strokeColor: "red",
                strokeWeight: 2,
                strokeOpacity: 0.5,
                fillColor: 'darksalmon',
                fillOpacity: 0.5

            }); //创建多边形
            map.addOverlay(polygon);

            //封閉地區 人員繪製；區分是否注射疫苗
            // const lowriskman = Cookies.get('lowRiskEmpee'); cookie超過4k 無法存取，改成localStorage
            const lowriskman = localStorage.getItem('lowRiskEmpee') ? JSON.parse(localStorage.getItem('lowRiskEmpee')) : undefined;
            var date = new Date().getTime();
            if (lowriskman && (date - lowriskman.startTime < lowriskman.expires)) {
                paintGreenPoint(lowriskman.data)
            } else {
                localStorage.getItem('lowRiskEmpee') && localStorage.removeItem('lowRiskEmpee');
                $.ajax({
                    type: "get",
                    // url: "http://10.189.127.62:40025/getEmpLocationApi",
                    url: "./testJSON/Empee.json",
                    success: function (data) {
                        const newData = data["data"];
                        const options = {
                            data: newData,
                            expires: 1000 * 60 * 60 * 6, //過期時間6小時
                            startTime: new Date().getTime() //记录何时将值存入缓存，毫秒级
                        }
                        localStorage.setItem('lowRiskEmpee', JSON.stringify(options));
                        paintGreenPoint(newData)
                    }
                });
            }

            function paintGreenPoint(dataset) {
                $('#overlay').css({
                    'display': 'none',
                    'opacity': '0'
                })
                // const c = new Convertor();
                const vaccination = []
                const unvaccination = []
                const safepeople = []

                for (var i = 0; i < dataset.length; i++) {
                    if (dataset[i].isInclosearea && dataset[i].vaccination) {
                        vaccination.push(dataset[i])
                    } else if (dataset[i].isInclosearea && (!dataset[i].vaccination)) {
                        unvaccination.push(dataset[i])
                    } else if (!dataset[i].isInclosearea) {
                        safepeople.push(dataset[i])
                    }
                }
                const myIconblue = new BMap.Icon("./images/blue.png", new BMap.Size(26, 26));
                // const c = new Convertor();
                for (let i = 0; i < vaccination.length; i++) {
                    // const res = c.GCJ2BD09({
                    //     lng: dataset[i].DIMENSIONS,
                    //     lat: dataset[i].LONGITUDE
                    // });
                    // const point = new BMap.Point(res.lng, res.lat);
                    const point = new BMap.Point(vaccination[i].longitude, vaccination[i].latitude);
                    const marker = new BMap.Marker(point, {
                        icon: myIconblue
                    });
                    map.addOverlay(marker);
                    marker.addEventListener('click', function () {
                        this.openInfoWindow(new BMap.InfoWindow(vaccination[i].emp_no + ',' + vaccination[i].emp_name + ',' + vaccination[i].address));
                    });
                }
                $('#numberofRighrisk').text(vaccination.length + unvaccination.length)
                $('#number1').text(vaccination.length)
                $('#number2').text(unvaccination.length)
                const myIconyellow = new BMap.Icon("./images/yellow.png", new BMap.Size(26, 26));
                // const c = new Convertor();
                for (let i = 0; i < unvaccination.length; i++) {
                    // const res = c.GCJ2BD09({
                    //     lng: dataset[i].DIMENSIONS,
                    //     lat: dataset[i].LONGITUDE
                    // });
                    // const point = new BMap.Point(res.lng, res.lat);
                    const point = new BMap.Point(unvaccination[i].longitude, unvaccination[i].latitude);
                    const marker = new BMap.Marker(point, {
                        icon: myIconyellow
                    });
                    map.addOverlay(marker);
                    marker.addEventListener('click', function () {
                        this.openInfoWindow(new BMap.InfoWindow(unvaccination[i].emp_no + ',' + unvaccination[i].emp_name + ',' + unvaccination[i].address));
                    });
                }

                const myIcongreen = new BMap.Icon("./images/green.png", new BMap.Size(26, 26));
                // const c = new Convertor();
                for (let i = 0; i < safepeople.length; i++) {
                    if (i == number) break
                    // const res = c.GCJ2BD09({
                    //     lng: dataset[i].DIMENSIONS,
                    //     lat: dataset[i].LONGITUDE
                    // });
                    // const point = new BMap.Point(res.lng, res.lat);
                    const point = new BMap.Point(safepeople[i].longitude, safepeople[i].latitude);
                    const marker = new BMap.Marker(point, {
                        icon: myIcongreen
                    });
                    map.addOverlay(marker);
                    marker.addEventListener('click', function () {
                        this.openInfoWindow(new BMap.InfoWindow(safepeople[i].emp_no + ',' + safepeople[i].emp_name + ',' + safepeople[i].address));
                    });
                }

                var col = ['工號', '姓名', '住址'];
                var table = document.getElementById('highriskman');
                table.innerHTML = "";
                // Create table header row using the extracted headers above.
                var tr = table.insertRow(-1); // table row
                for (var i = 0; i < col.length; i++) {
                    var th = document.createElement("th"); // table header.
                    th.innerHTML = col[i];
                    th.style.textAlign = 'center';
                    th.style.position = 'sticky';
                    th.style.top = 0;
                    tr.appendChild(th);
                }
                for (var i = 0; i < unvaccination.length; i++) {
                    tr = table.insertRow(-1);
                    if (i == 10) {
                        for (var j = 0; j < 3; j++) {
                            var tabCell = tr.insertCell(-1);
                            tabCell.innerHTML = '...';
                        }
                        break
                    }
                    for (var item in unvaccination[i]) {
                        if (item == 'emp_no' || item == 'emp_name' || item == 'address') {
                            var tabCell = tr.insertCell(-1);
                            tabCell.innerHTML = unvaccination[i][item];
                        }
                    }
                }

            }
        }

    }

    $("#overlay").css({
        'display': 'block',
        'opacity': '0.8'
    });

    main(1, 200); //init 初始化

    $('#toexcel').click(function () {
        const dis = $("#iuputkm").val()
        const chkRadio = $('input:radio[name="type"]:checked').val();
        if (chkRadio == '1') {
            var jsonData = localStorage.getItem('highRiskEmpee' + dis) ? JSON.parse(localStorage.getItem('highRiskEmpee' + dis)).data : undefined;
            var str = `工號,姓名,地址,經度,緯度,type,confidence,風險區,第一次接種,是否接種\n`;
        } else {
            var rowdata = localStorage.getItem('lowRiskEmpee') ? JSON.parse(localStorage.getItem('lowRiskEmpee')).data : undefined;
            var jsonData = rowdata.filter(item => item.isInclosearea)
            var str = `工號,姓名,部門,job,title,indirect,address,經度,緯度,type,confidence,comprehension,第一次接種,第二次接種,vaccination,isInclosearea,isINCompany\n`;
        }

        //列标题，逗号隔开，每一个逗号就是隔开一个单元格

        //增加\t为了不让表格显示科学计数法或者其他格式
        for (let i = 0; i < jsonData.length; i++) {
            for (let item in jsonData[i]) {
                str += `${jsonData[i][item] + '\t'},`;
            }
            str += '\n';
        }
        //encodeURIComponent解决中文乱码
        let uri = 'data:text/csv;charset=utf-8,\ufeff' + encodeURIComponent(str);
        //通过创建a标签实现
        var link = document.createElement("a");
        link.href = uri;
        //对下载的文件命名
        link.download = "風險人員名單.csv";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

    })

    $("#search").click(function () {
        const distance = Number($("#iuputkm").val())
        const num = Number($("#peoplenum").val())
        $("#overlay").css({
            'display': 'block',
            'opacity': '0.8'
        });
        main(distance, num);
    })

    //點擊單選按鈕 隱藏/顯示div
    $('input[type=radio][name=type]').change(function () {
        if (this.value == '1') {
            $('#inputriskditance').removeClass('inputriskditance')
        } else if (this.value == '2') {
            $('#inputriskditance').addClass('inputriskditance');
        }
    });

    //清除緩存
    $('#clear').click(function () {
        localStorage.getItem('pubRiskAera') && localStorage.removeItem('pubRiskAera');
        localStorage.getItem('highRiskEmpee1') && localStorage.removeItem('highRiskEmpee1');
        localStorage.getItem('highRiskEmpee2') && localStorage.removeItem('highRiskEmpee2');
        localStorage.getItem('highRiskEmpee3') && localStorage.removeItem('highRiskEmpee2');
        localStorage.getItem('lowRiskEmpee') && localStorage.removeItem('lowRiskEmpee');
        alert('已成功清除緩存數據.')
    })
})