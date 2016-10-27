#!/usr/bin/env python
"""
Written by Luckylau
Github: https://github.com/Luckylau
Email: laujunbupt0913@163.com

add portgroup to dvs ,default portnum=6000

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

    parser.add_argument('-v', '--vds-name',
                        required=True,
                        action='store',
                        help='Name of the vds')

    parser.add_argument('-pg', '--port-group',
                        required=True,
                        action='store',
                        help='port group will be created')

    parser.add_argument('-vlan', '--vlanId',
                        required=False,
                        default=0,
                        action='store',
                        help='port group will be set vlanId')

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


def add_portgroup(vds,pgname,vlanId):
    dvpgConfigSpec=vim.dvs.DistributedVirtualPortgroup.ConfigSpec()
    dvpgConfigSpec.name=pgname
    dvpgConfigSpec.numPorts=6000
    dvpgConfigSpec.description="laujunbupt0913@163.com"
    dvpgConfigSpec.type="earlyBinding"
    dvpgConfigSpec.defaultPortConfig=vim.dvs.VmwareDistributedVirtualSwitch.VmwarePortConfigPolicy()
    dvpgConfigSpec.defaultPortConfig.vlan=vim.dvs.VmwareDistributedVirtualSwitch.VlanIdSpec()
    dvpgConfigSpec.defaultPortConfig.vlan.vlanId=int(vlanId)

    vds.CreateDVPortgroup_Task(dvpgConfigSpec)
    print "Portgroup created success ..."

def main():
    args=get_args()

    '''

    host = "10.0.36.60"
    user = "administrator@vsphere.local"
    password = " "
    vds = "DSwitch"
    port_group = "luckylau1"
    vlanId=12
    default_port = "443"

    '''

    serviceInstance = SmartConnect(host=args.host,
                      user=args.user,
                      pwd=args.password,
                      port=int(args.port)
                      )


    if not serviceInstance:
        print("Could not connected ")
        return -1

    atexit.register(Disconnect, serviceInstance)

    content = serviceInstance.RetrieveContent()
    print "Search VDS by name ..."
    vds = get_obj(content, [vim.DistributedVirtualSwitch], args.vds_name)
    if not vds:
        print("VDS not found")
        return -1
    print "Create portgroup by name ..."
    add_portgroup(vds, args.port_group,args.vlanId)

if __name__ == '__main__':
    main()










