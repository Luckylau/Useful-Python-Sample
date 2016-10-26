#!/usr/bin/env python
"""
Written by Luckylau
Github: https://github.com/Luckylau
Email: laujunbupt0913@163.com

add nic to vm ,the networkadapter is set in dvs portgroup

Known issues:
This script is running well in centos6.5
"""


from pyVim.connect import SmartConnect,Disconnect
import atexit
from pyVmomi import vim
import sys


def add_nic(vm,mac,port):
    spec=vim.vm.ConfigSpec()
    nic_changes=[]
    nic_spec=vim.vm.device.VirtualDeviceSpec()
    nic_spec.operation=vim.vm.device.VirtualDeviceSpec.Operation.add

    nic_spec.device=vim.vm.device.VirtualE1000()
    nic_spec.device.deviceInfo=vim.Description()
    nic_spec.device.deviceInfo.summary='vCenter API'

    nic_spec.device.backing=vim.vm.device.VirtualEthernetCard.DistributedVirtualPortBackingInfo()
    nic_spec.device.backing.port=vim.dvs.PortConnection()
    nic_spec.device.backing.port.portgroupKey=port.portgroupKey
    nic_spec.device.backing.port.switchUuid=port.dvsUuid
    nic_spec.device.backing.port.portKey =port.key


    nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
    nic_spec.device.connectable.startConnected = True
    nic_spec.device.connectable.allowGuestControl = True
    nic_spec.device.connectable.connected = False
    nic_spec.device.connectable.status = 'untried'

    nic_spec.device.wakeOnLanEnabled = True
    nic_spec.device.addressType = 'assigned'
    nic_spec.device.macAddress = mac

    nic_changes.append(nic_spec)
    spec.deviceChange = nic_changes
    e = vm.ReconfigVM_Task(spec=spec)
    print "Nic card added success ..."

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

def search_port_old(content,dvs,portgroupkey):
    portkey=None
    portkeys=[]
    criteria=vim.dvs.PortCriteria()
    criteria.inside = True
    criteria.portgroupKey=portgroupkey
    portkeyvds=dvs.FetchDVPortKeys(criteria)

    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.VirtualMachine], True
    )
    for vm in container.view:
        for dev in vm.config.hardware.device:
            if isinstance(dev, vim.vm.device.VirtualEthernetCard):
                dev_backing = dev.backing
                if hasattr(dev_backing, 'port'):
                    if portgroupkey ==dev_backing.port.portgroupKey:
                        portkey = dev_backing.port.portKey
                        portkeys.append(portkey)
    search_portkey=list(set(portkeyvds).difference(set(portkeys)))
    print search_portkey
    return search_portkey[0]

def search_port(dvs,portgroupkey):
    search_portkey=[]
    criteria= vim.dvs.PortCriteria()
    criteria.connected=False
    criteria.inside = True
    criteria.portgroupKey = portgroupkey
    ports=dvs.FetchDVPorts(criteria)
    for port in ports:
        search_portkey.append(port.key)
    print search_portkey
    return search_portkey[0]

def get_args():
    if len(sys.argv)>1:
        host,user,password,vm_name,port_group,macAddress=sys.argv[1:]
    else:
        host=raw_input("Vcenter IP : ")
        user=raw_input("User: ")
        password=raw_input("Password: ")
        vm_name=raw_input("VM_name: ")
        port_group=raw_input("Port_Group: ")
        macAddress=raw_input("Input MacAddress :")
        port_name=raw_input("Input portname:")
        port_description=raw_input("Input port description:")
    return host,user,password,vm_name,port_group,macAddress,port_name,port_description

def port_find(dvs, key):
    obj = None
    ports=dvs.FetchDVPorts()
    for c in ports:
        if c.key==key:
            obj=c
    return obj
def set_port(dvs,portkey,name,description):
    port_configs = []
    portconfig = vim.dvs.DistributedVirtualPort.ConfigSpec()
    portconfig.operation = "edit"
    portconfig.key = portkey
    portconfig.name = name
    portconfig.description = description
    port_configs.append(portconfig)
    dvs.ReconfigureDVPort_Task(port_configs)


def main():
    host,user,password,vm_name,port_group,macAddress,port_name,port_description=get_args()
    ''''
    host="10.0.36.60"
    user="administrator@vsphere.local"
    password=" "
    vm_name="liujuntestvm83"
    port_group="DPortGroup"
    macAddress="fa:cd:45:ed:56:e6"
    port_name="luckylau"
    port_description="laujunbupt0913@163.com"
    '''


    default_port="443"

    serviceInstance=SmartConnect(host=host,
                                 user=user,
                                 pwd=password,
                                 port=default_port)

    atexit.register(Disconnect,serviceInstance)
    content = serviceInstance.RetrieveContent()

    print "Search VDS PortGroup by name ..."
    portgroup=None
    portgroup = get_obj(content, [vim.dvs.DistributedVirtualPortgroup], port_group)
    if portgroup is None:
        print "Portgroup not Found ..."
        exit(0)

    print "Search available(unused) port for vm ..."
    dvs = portgroup.config.distributedVirtualSwitch
    #portKey=search_port_old(content,dvs,portgroup.key)
    portKey=search_port(dvs,portgroup.key)
    print portKey

    print "Set port_name, port_description for port ..."
    set_port(dvs, portKey, port_name, port_description)

    print "Search vm by name ..."
    vm=None
    vm=get_obj(content,[vim.VirtualMachine],vm_name)
    if vm:
        print "Find Vm , add nic card ..."
        port = port_find(dvs, portKey)
        add_nic(vm,macAddress,port)
    else:
        print "Vm not Found ..."

if __name__ == '__main__':
    sys.exit(main())