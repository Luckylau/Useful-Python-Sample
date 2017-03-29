#-*- coding: utf-8 -*-
# Author: Lucky lau
# E-mail:laujunbupt0913@163com
htmlStr = '''
 <!DOCTYPE html>
 <head>
    <meta charset="utf-8">
     <title>%(title)s</title>
 </head>
 <body>
     <div id="main" style="height:600px;width:900px;margin:20px auto;"></div>
     <script src="http://echarts.baidu.com/build/dist/echarts-all.js"></script>
     <script type="text/javascript">
         var myChart = echarts.init(document.getElementById('main'));
         var option = {
             backgroundColor: '#1b1b1b',
             color: ['gold', 'aqua', 'lime'],
             title: {
                 text: '%(title)s',
                 subtext: '%(subtitle)s',
                 x: 'center',
                  textStyle: {
                      color: '#fff'
                  }
              },
              tooltip: {
                  trigger: 'item',
                  formatter: '{b}'
              },
              dataRange: {
                  show:false,
                  min : 0,
                  max : 100,
                  calculable : true,
                  color: ['#ff3333', 'orange', 'yellow','lime','aqua'],
                  textStyle:{
                      color:'#fff'
                  }
              },
              series: [{
                  name: '全国',
                  type: 'map',
                  roam: true,
                  hoverable: false,
                  mapType: '%(region)s',
                  itemStyle: {
                      normal: {
                          borderColor: 'rgba(100,149,237,1)',
                          borderWidth: 0.5,
                          areaStyle: {
                              color: '#1b1b1b'
                          }
                      }
                  },
                  data: [],
                  geoCoord: %(alldata)s
              }, {
                  name: '足迹',
                  type: 'map',
                  mapType: '%(region)s',
                  data: [],
                  markLine: {
                      smooth: true,
                      effect: {
                          show: true,
                          scaleSize: 1,
                          period: 30,
                          color: '#fff',
                          shadowBlur: 10
                      },
                      itemStyle: {
                          normal: {
                              borderWidth: 1,
                              lineStyle: {
                                  type: 'solid',
                                  shadowBlur: 10
                              },
                              label:{
                                  show:false
                              },
                          }
                      },
                      data: %(linedata)s
                  },
                  markPoint: {
                      symbol: 'emptyCircle',
                      symbolSize: function(v) {
                          return 10 + v / 10
                      },
                      effect: {
                          show: true,
                          shadowBlur: 0
                      },
                      itemStyle: {
                          normal: {
                              label: {
                                 show: false
                              }
                         },
                          emphasis: {
                              label: {
                                  position: 'top'
                              }
                          }
                      },
                      data: %(pointdata)s
                  }
              }]
          };
          myChart.setOption(option);
      </script>
  </body>
  /html>
  '''.replace('\n','')