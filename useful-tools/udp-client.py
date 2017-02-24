#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Author: Lucky lau

E-mail:laujunbupt0913@163com

simulate udp
"""
from socket import *


class udp_client():

    def __init__(self):
        pass

    def setConfig(self, host, port):
        self.host = host
        self.port = port

    def init_service(self):
        client = socket(AF_INET, SOCK_DGRAM)
        client.connect((self.host, self.port))
        while True:
            for i in range(0,10000):
                message = 'udp-message-'+str(i)
                client.sendall(message)
                data = client.recv(2048)
                print ("recieve data from server : %s " % data)
            if i==9999:
                break
        client.close()
if __name__ == '__main__':
    udp_client=udp_client()
    udp_client.setConfig("10.0.36.157",2000)
    udp_client.init_service()