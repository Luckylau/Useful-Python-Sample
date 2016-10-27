#!/usr/bin/env python
"""
Written by Luckylau
Github: https://github.com/Luckylau
Email: laujunbupt0913@163.com

delete nic of vm by nic number

Known issues:
This script is running well in centos6.5,python 2.7
"""

import argparse
import getpass
from pyVim.connect import SmartConnect, Disconnect
import atexit
from pyVmomi import vim
#from tools import tasks


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

    parser.add_argument('-v', '--vm-name',
                        required=False,
                        action='store',
                        help='name of the vm')

    parser.add_argument('-m', '--unit-number',
                        required=True,
                        type=int,
                        help='HDD number to delete.' )

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


def delete_nic(si,vm,nic_number):
    spec = vim.vm.ConfigSpec()
    nic_changes = []
    nic_prefix_label="Network adapter "
    nic_label = nic_prefix_label + str(nic_number)
    virtual_nic_device = None
    for dev in vm.config.hardware.device:
        if isinstance(dev, vim.vm.device.VirtualEthernetCard) \
                and dev.deviceInfo.label == nic_label:
            virtual_nic_device = dev
    if not virtual_nic_device:
        raise RuntimeError('Virtual {} could not be found.'.format(nic_label))

    nic_spec = vim.vm.device.VirtualDeviceSpec()
    nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.remove
    nic_spec.device = virtual_nic_device
    nic_changes.append(nic_spec)
    spec.deviceChange=nic_changes
    task = vm.ReconfigVM_Task(spec=spec)
    #tasks.wait_for_tasks(si, [task])
    print "Nic card remoted success ..."



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
    print "Search vm by name ..."
    vm = None
    content = serviceInstance.RetrieveContent()
    vm = get_obj(content, [vim.VirtualMachine], args.vm_name)
    if vm:
        print "Find Vm , delete nic card ..."
        delete_nic(serviceInstance,vm,args.unit_number)
    else:
        print "Vm not Found ..."

if __name__ == '__main__':
    main()