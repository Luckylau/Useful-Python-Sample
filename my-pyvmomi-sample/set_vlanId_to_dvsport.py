#!/usr/bin/env python
"""
Written by Luckylau
Github: https://github.com/Luckylau
Email: laujunbupt0913@163.com

Set unique vlanId for dvport when vm nic connects it.
Note that the dvportgroup'vlanId is "0" in default, and you
must set "vlan override" True



Known issues:
This script is running well in centos6.5
"""

from pyVim.connect import SmartConnect, Disconnect
import atexit
from pyVmomi import vim
import getpass
import argparse
import ssl


def get_args():
    parser = argparse.ArgumentParser(
        description='Argument for talking to vCenter'
    )

    parser.add_argument('-s', '--host',
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
                        help='Portgroup name')

    args = parser.parse_args()

    if not args.password:
        args.password = getpass.getpass(prompt='Enter password:')

    return args


def get_obj(content, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True
    )
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj


def GenerateVlanId(port_used):
    vlanId = range(1, 4095)
    search_portkey = list(set(vlanId).difference(set(port_used)))
    if search_portkey:
        return search_portkey


def set_port(dvs, ports, port_used):
    i=0
    port_configs = []
    setvlanId = GenerateVlanId(port_used)
    for port in ports:
        if port.config.setting.vlan.vlanId==0:
            portconfig = vim.dvs.DistributedVirtualPort.ConfigSpec()
            portconfig.operation = "edit"
            portconfig.key = port.key
            portconfig.setting = vim.dvs.VmwareDistributedVirtualSwitch.VmwarePortConfigPolicy()
            portconfig.setting.vlan = vim.dvs.VmwareDistributedVirtualSwitch.VlanIdSpec()
            portconfig.setting.vlan.vlanId = setvlanId[i]
            i=i+1
            port_configs.append(portconfig)
    dvs.ReconfigureDVPort_Task(port=port_configs)
    print ("All ports vlanId success...")



def set_port_vlanId(dvs, portgroup):
    port_used = []
    criteria = vim.dvs.PortCriteria()
    criteria.connected = True
    criteria.inside = True
    criteria.portgroupKey = portgroup.key
    ports = dvs.FetchDVPorts(criteria)
    if ports:
        for port in ports:
            vlanId = port.config.setting.vlan.vlanId
            port_used.append(vlanId)
        set_port(dvs, ports, port_used)
    else:
        print("No dvports in use ...")



def main():
    args = get_args()
    context = None
    if hasattr(ssl, "_create_unverified_context"):
        context = ssl._create_unverified_context()
    serviceInstance = SmartConnect(host=args.host,
                                   user=args.user,
                                   pwd=args.password,
                                   port=int(args.port),
                                   sslContext=context
                                   )

    if not serviceInstance:
        print("Could not connected ")
        return -1
    atexit.register(Disconnect, serviceInstance)

    print ("Search DvsPortGroup by name ...")
    content = serviceInstance.RetrieveContent()
    portgroup = get_obj(content,
                        [vim.dvs.DistributedVirtualPortgroup],
                        args.port_group)
    if not portgroup:
        print ("DvsPortGroup not Found ...")
        return -1
    dvs = portgroup.config.distributedVirtualSwitch
    print ("Set unique vlanId for used ports ...")
    set_port_vlanId(dvs, portgroup)

if __name__ == '__main__':
    main()
