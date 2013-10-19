network_interfaces_parser
========================

With this library you can modify /etc/network/interfaces easily

Examples of use
==============
Firstly create object and l
```python
import interfacesparser
...
my_interface_file = interfacesparser.InterfacesParser()
```

Load file you want
```python
file_path = '/etc/network/interfaces'
try:
	my_interface_file.load(file_path)
except Exception as e:
	if 'not exist' in e.message:
		print 'File ' +file_path+' not exists'
```
Get interfaces defined on file
```python
>>>my_interface_file.get_list_interfaces()
['lo', 'eth1', 'eth0']
```
Get info of interface
```python
>>> my_interface_file.get_info_interface('eth0')
['auto eth0', 'iface eth0 inet static\n\taddress 10.2.1.254\n\tnetmask 255.255.255.0']
```
Also you can get detail information or better structured by
```python
>>> my_interface_file.interface_mapping['eth0']
[2, 3]
>>> my_interface_file.content[2]
<interfacesparser.StanzaAuto object at 0xa4045cc>
>>> my_interface_file.content[3]
<interfacesparser.StanzaIface object at 0xa4044ec>
>>> my_interface_file.content[3].options
['address 10.2.1.254', 'netmask 255.255.255.0']
>>> my_interface_file.content[3].family
'inet'
>>> my_interface_file.content[3].method
'static'
```
To get more info of StanzaIface or StanzaAuto view wiki page.
If you want change interface to dhcp mode , you can use change_to_dhcp function
```python
>>> my_interface_file.get_info_interface('eth0')
['auto eth0', 'iface eth0 inet static\n\taddress 10.2.1.254\n\tnetmask 255.255.255.0']
>>> my_interface_file.change_to_dhcp('eth0')
>>> my_interface_file.get_info_interface('eth0')
['auto eth0', 'iface eth0 inet dhcp']
```
On the other hand, if you want set static ip to interface , exist change_to_static:
```python
>>> my_interface_file.get_info_interface('eth0')
['auto eth0', 'iface eth0 inet dhcp']
>>>options = {'address':'192.168.1.10','netmask':'255.255.255.0','gateway':'192.168.1.1'}
>>> my_interface_file.change_to_static('eth0',options)
>>> my_interface_file.get_info_interface('eth0')
['auto eth0', 'iface eth0 inet static\n\taddress 192.168.1.10\n\tnetmask 255.255.255.0\n\tgateway 192.168.1.1']
```
If you want change only ip on static definded interface : 
```python
for x in my_interface_file.interface_mapping['eth0']:
    if my_interface_file.content[x].__class__.__name__ == 'StanzaIface':
        my_interface_file.content[x].change_ip('192.168.1.1')
```
Also you can change netmask:
```python
for x in my_interface_file.interface_mapping['eth0']:
    if my_interface_file.content[x].__class__.__name__ == 'StanzaIface':
        my_interface_file.content[x].change_netmask('255.255.0.0')
```
