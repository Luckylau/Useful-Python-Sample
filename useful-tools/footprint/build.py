#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Author: Lucky lau
# E-mail:laujunbupt0913@163com

from configobj import ConfigObj
from base import htmlStr
import requests
import random
import sys ,os
import json
reload(sys)
sys.setdefaultencoding('utf8')

conf = 'info.conf'


def getconfig(conf):
    config = ConfigObj(conf, encoding='UTF8')
    return config


class footPrint(object):

    def __init__(self, config):
        self.key = 'q5mTrTGzCSVq5QmGpI9y18Bo'
        self.url = 'http://api.map.baidu.com/geocoder/v2/?output=json&ak=%s&address=' % (
            self.key)
        self.title = config['title']['title']
        self.color = config['config']['color']
        self.subtitle = config['title']['subtitle']
        self.data = config['foot']['foot']
        self.region = config['foot']['region']
        self.alldata = {}
        self.linedata = []
        self.pointdata = []
        self.cache = {}

    def getPoint(self, name):
        url = self.url + name
        try:
            r = requests.get(url)
            res = r.json()
            print res
            if res.get('result'):
                loc = res['result']['location']
                self.alldata[name] = [loc['lng'], loc['lat']]
                return True
            else :
                raise Exception('获取不到%s的经纬度信息'% (name) )
        except Exception,e:
            print str(e)
            return False



    def getValue(self):
        if self.color:
            return random.randint(2, 100)
        else:
            return 1

    def processData(self):
        foots=[]
        info = self.data.split()
        for foot in info:
            if foot not in self.alldata:
                if self.getPoint(foot):
                    self.cache[foot] = self.getValue()
                    foots.append(foot)
        for i in range(len(foots) - 1):
            self.linedata.append(
                    [
                        {
                            'name': foots[i]
                        },
                        {
                            'name': foots[i + 1],
                            'value': self.cache[foots[i + 1]]
                        }
                    ]
                )
        for name in self.alldata:
            self.pointdata.append(
                {
                    'name': name, 'value': self.cache[name]
                }
            )

    def writeFile(self):

        obj = {
            'title': self.title,
            'subtitle': self.subtitle,
            'region': self.region,
            'alldata': json.dumps(self.alldata),
            'linedata': json.dumps(self.linedata),
            'pointdata': json.dumps(self.pointdata)
        }

        with open('footprint.html', 'w') as f:
            f.write(htmlStr % obj)
        print '成功生成文件，打开看看吧！'

    def start(self):
        self.processData()
        self.writeFile()

if __name__ == '__main__':

    config = getconfig(conf)
    foot = footPrint(config)
    foot.start()