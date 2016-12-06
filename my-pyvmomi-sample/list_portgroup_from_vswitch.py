#!/usr/bin/env python
"""
Written by Luckylau
Github: https://github.com/Luckylau
Email: laujunbupt0913@163.com

list portgroup information of virutal switch by name,
 including thier name ,vlanId

Known issues:
This script is running well in centos6.5
"""


import sys
from pyVim.connect import SmartConnect, Disconnect
import atexit
from pyVmomi import vim


def getarg():
    if len(sys.argv) > 1:
        host, user, password, vswitch = sys.argv[1:]
    else:
        host = raw_input("Host IP : ")
        user = raw_input("Username: ")
        password = raw_input("Password: ")
        vswitchname = raw_input("Vswitch name: ")
    return host, user, password, vswitchname


def get_obj(content, vimtype):
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True
    )
    for host in container.view:
        obj = host
    return obj


def get_vswitch(host, name):
    obj = None
    if host:
        for vswitch in host.config.network.vswitch:
            if vswitch.name == name:
                obj = vswitch
                break
    else:
        print "Host not found"
    return obj


def list_portgroup(host, vswitch):
    if vswitch.portgroup:
        print "portgroup info:\n"
        for pg in vswitch.portgroup:
            for portgroup in host.config.network.portgroup:
                if portgroup.key == pg:
                    print "name :" + portgroup.spec.name + " vlanId :" + str(portgroup.spec.vlanId)
    else:
        print " Portgroup not found ..."


def main():
    host, user, password, vswitchname = getarg()
    # host="10.0.36.17"
    # user="root"
    # password="1111111"
    # vswitchname="vSwitch1"
    default_port = "443"

    serviceInstance = SmartConnect(host=host,
                                   user=user,
                                   pwd=password,
                                   port=default_port)

    atexit.register(Disconnect, serviceInstance)

    print "Search Virtual Switch by name ..."

    vswitch = None
    host = None
    content = serviceInstance.RetrieveContent()
    host = get_obj(content, [vim.HostSystem])
    vswitch = get_vswitch(host, vswitchname)
    if vswitch:
        print "Find Virtual Switch , Search portgroup ..."
        list_portgroup(host, vswitch)
    else:
        print "Virtual Switch not found ..."
if __name__ == '__main__':
    main()
