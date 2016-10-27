#!/usr/bin/env python
"""
Written by Luckylau
Github: https://github.com/Luckylau
Email: laujunbupt0913@163.com

delete portgroup of dvs by name

Known issues:
This script is running well in centos6.5,python 2.7
"""

import argparse
import getpass
from pyVim.connect import SmartConnect, Disconnect
import atexit
from pyVmomi import vim


def get_args():
    parser = argparse.ArgumentParser(
        description='Argument for talking to vCenter'
    )

    parser.add_argument('-s','--host',
                        required=True,
                        action='store',
                        help='Vcenter Ip')

    parser.add_argument('-o', '--port',
                        type=int,
                        default=443,
                        action='store',
                        help='Port to connect on')

    parser.add_argument('-u', '--user',
                        required=True,
                        action='store',
                        help='User name to use')

    parser.add_argument('-p', '--password',
                        required=False,
                        action='store',
                        help='Password to use')

    parser.add_argument('-pg', '--port-group',
                        required=True,
                        action='store',
                        help='port group will be removed')

    args = parser.parse_args()

    if not args.password:
        args.password=getpass.getpass(prompt='Enter password:')

    return args


def get_obj(content, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder,vimtype,True
    )
    for c in container.view:
        if c.name==name:
            obj=c
            break
    return obj


def criteria(dvs,portgroup,connected):
    criteria = vim.dvs.PortCriteria()
    criteria.inside = True
    criteria.portgroupKey = portgroup.key
    if connected:
        criteria.connected = connected
    ports=dvs.FetchDVPorts(criteria)
    return ports

def delete_dvsportgroup(dvs,portgroup):
    unusedports=[]
    allports=[]
    unusedports=criteria(dvs,portgroup,False)
    allports=criteria(dvs,portgroup,None)

    if len(unusedports)==len(allports):
        portgroup.Destroy_Task()
        print "DvsPortGroup deleted sucess ..."
    else:
        print "DvsPortGroup are in use ,Can not be deleted ..."


def main():
    args=get_args()
    serviceInstance = SmartConnect(host=args.host,
                                   user=args.user,
                                   pwd=args.password,
                                   port=int(args.port)
                                   )

    if not serviceInstance:
        print("Could not connected ")
        return -1

    atexit.register(Disconnect, serviceInstance)

    print "Search DvsPortGroup by name ..."
    content = serviceInstance.RetrieveContent()
    portgroup = get_obj(content, [vim.dvs.DistributedVirtualPortgroup], args.port_group)
    if not portgroup:
        print "DvsPortGroup not Found ..."
        return -1
    dvs = portgroup.config.distributedVirtualSwitch
    delete_dvsportgroup(dvs,portgroup)

if __name__ == '__main__':
    main()