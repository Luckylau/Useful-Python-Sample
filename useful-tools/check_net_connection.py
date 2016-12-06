#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Author: Lucky lau
# E-mail:laujunbupt0913@163com

import re
import subprocess


def check_net_connection(ip):
    try:
        p = subprocess.Popen(["ping -c 1 -w 1 " + ip],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)
        out = p.stdout.read()
        regex = re.compile('100% packet loss')
        if len(regex.findall(out)) == 0:
            print ip + " can be reachable"
        else:
            print ip + " can't be reachable"
    except Exception as e:
        print ("Error: " + str(e))

if __name__ == '__main__':
    check_net_connection('10.20.0.56')
    check_net_connection('10.10.0.56')
    check_net_connection('10.0.38.106')
