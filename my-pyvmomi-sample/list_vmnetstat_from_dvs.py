#!/usr/bin/env python
"""
Written by Luckylau
Github: https://github.com/Luckylau
Email: laujunbupt0913@163.com

list  network information of all vms in vds ,including portgroup,
portkey,macaddress,vlanId etc.

example :
   input:
         vcenter ip  , username , password ,
   output:
         virtualMachine: XXXX network information:
         [dvs] XXX [portGroup] XXX [port_id] XXX [vlanId] XXX [macAddress] XXXX [connectable] XXX
Known issues:
This script is running well in centos6.5
"""

import sys
from pyVim.connect import SmartConnect, Disconnect
import atexit
from pyVmomi import vim
import types


def getarg():
    if len(sys.argv) > 1:
        vcenter_ip, user, password = sys.argv[1:]
    else:
        vcenter_ip = raw_input("Vcenter IP : ")
        user = raw_input("Username: ")
        password = raw_input("Password: ")
    return vcenter_ip, user, password


def get_alldvs(content, vimtype):
    obj = []
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True
    )
    for dvs in container.view:
        obj.append(dvs)
    return obj


def get_dvportgroup(dvswitch):
    dv_portgroup = {}
    for dvs in dvswitch:
        dv_portgroup[dvs] = dvs.portgroup
    return dv_portgroup


def get_vms(dvportgroup):
    vms = {}
    for dvs in dvportgroup:
        for pg in dvportgroup[dvs]:
            vms[pg] = pg.vm
    return vms


def list_netstatus(vms):
    portkey = None
    portGroup = None
    vlanId = None
    connectable = None
    for pg in vms:
        for vm in vms[pg]:
            for dev in vm.config.hardware.device:
                if isinstance(dev, vim.vm.device.VirtualEthernetCard):
                    dev_backing = dev.backing
                    if hasattr(dev_backing, 'port'):
                        portkey = dev_backing.port.portKey
                    dvs = pg.config.distributedVirtualSwitch.name
                    portGroup = pg.config.name
                    vlanId = pg.config.defaultPortConfig.vlan.vlanId
                    if not isinstance(vlanId, types.IntType):
                        vlanId = None
                    macAddress = dev.macAddress
                    connectable = dev.connectable.connected
            print "virtualMachine:" + vm.name + " network information:\n " + " [dvs] " + dvs + " [portGroup] " + portGroup + " [port_id] " + portkey + " [vlanId] " + str(vlanId) + " [macAddress] " + macAddress + " [connectable] " + str(connectable)


def main():
    vcenter_ip, user, password = getarg()
    default_port = "443"
    serviceInstance = SmartConnect(host=vcenter_ip,
                                   user=user,
                                   pwd=password,
                                   port=default_port)
    atexit.register(Disconnect, serviceInstance)

    print "Serach the DistributedVirtualSwitch..."
    host = None
    global content
    content = serviceInstance.RetrieveContent()
    dvs = get_alldvs(content, [vim.DistributedVirtualSwitch])

    print "Search the portgroup in dvs..."
    dvportgroup = get_dvportgroup(dvs)

    print "Search the vms in portgroup ..."
    vms_portgroup = get_vms(dvportgroup)

    print " list the network status of vms"

    list_netstatus(vms_portgroup)

if __name__ == '__main__':
    main()
