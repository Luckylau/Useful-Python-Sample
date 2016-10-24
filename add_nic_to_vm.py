from pyVim.connect import SmartConnect,Disconnect
import atexit
from pyVmomi import vim
import sys


def add_nic(si,vm,network,mac):
    spec=vim.vm.ConfigSpec()
    nic_changes=[]

    nic_spec=vim.vm.device.VirtualDeviceSpec()
    nic_spec.operation=vim.vm.device.VirtualDeviceSpec.Operation.add

    nic_spec.device=vim.vm.device.VirtualE1000()
    nic_spec.device.deviceInfo=vim.Description()
    nic_spec.device.deviceInfo.summary='vCenter API --- add mac address'

    nic_spec.device.backing=vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
    nic_spec.device.backing.useAutoDetect=False
    nic_spec.device.backing.deviceName=network
    content=si.RetrieveContent()
    nic_spec.device.backing.network=get_obj(content,[vim.Network],network)

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

def get_args():
    if len(sys.argv)>1:
        host,user,password,vm_name,port_group,macAddress=sys.argv[1:]
    else:
        host=raw_input("Host IP : ")
        user=raw_input("Username: ")
        password=raw_input("Password: ")
        vm_name=raw_input("Vm_name: ")
        port_group=raw_input("Port_group: ")
        macAddress=raw_input("Set macAddress manually :")
    return host,user,password,vm_name,port_group,macAddress

def main():
    #args={"host":"10.0.36.17","user":"root","port":"443","password":"1111111","vm-name":"luckylauvlan12","port_group":"vlan12"}
    host,user,password,vm_name,port_group,macAddress=get_args()
    default_port="443"

    serviceInstance=SmartConnect(host=host,
                                 user=user,
                                 pwd=password,
                                 port=default_port)

    atexit.register(Disconnect,serviceInstance)

    print "Search VM by name ..."
    vm=None
    content=serviceInstance.RetrieveContent()
    vm=get_obj(content,[vim.VirtualMachine],vm_name)

    if vm:
        print "Find Vm , add nic card ..."
        add_nic(serviceInstance,vm,port_group,macAddress)
    else:
        print "VM not Found ..."
if __name__ == '__main__':
    sys.exit(main())
