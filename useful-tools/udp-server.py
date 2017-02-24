#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Author: Lucky lau

E-mail:laujunbupt0913@163com

simulate udp
"""

from socket import *
from time import ctime
import subprocess


def close_iptables():
    print("begin closing iptables ...")
    re = subprocess.call("service iptables stop", shell=True)
    if re == 0:
        print("service iptables stop sucessfully...")
    else:
        print ("check iptables on or off ,turn off manually...")
        exit(0)


class udp_server():

    def __init__(self):
        pass

    def setConfig(self, host, port):

        self.host = host
        self.port = port

    def init_service(self):

        try:
            server = socket(AF_INET, SOCK_DGRAM)
            server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
            server.bind((self.host, self.port))
            print("waiting message from udp_client ....")
            while True:
                data, address = server.recvfrom(2048)
                server.sendto('[%s] %s' % (ctime(), data), address)
                print("receive message : %s " % data)
        except KeyboardInterrupt:
             print("KeyboardInterrupt : %s" % ctime())
        finally:
            server.close()




if __name__ == '__main__':
    close_iptables();
    udp_server = udp_server()
    udp_server.setConfig("10.0.36.157", 2000)
    udp_server.init_service()
