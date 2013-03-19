class StanzaBasic(object):
	def __init__(self,list_interfaces):
		'''
			list_interfaces is list
		'''
		self.type = ''
		self.interfaces = []
		if(type(list_interfaces) == type([])):
			for i in list_interfaces:
				self.interfaces.append(i)
		else:
			raise "list_interfaces may be list"
	#def __init__
	
	def append_interface(self,interface,order=-1):	
		if(order < 0):
			self.interfaces.append(interface)
		else:
			aux_interface_list = self.interfaces[:order] + [interface]+ self.interfaces[order:]
			self.interfaces = aux_interface_list
		
		return interface
	#def append_interface
	
	def remove_interface(self,interface):
		if interface in self.interface:
			i = self.interface(interface)
			return self.options.pop(i)
		return None
	#def append_interface

	def get_interfaces(self):
		return self.interfaces
	#def get_interfaces

class StanzaAuto(StanzaBasic):
	def __init__(self,list_interfaces):
		'''
			list_interfaces is list
		'''
		super(StanzaAuto,self).__init__(list_interfaces)
		self.type = 'auto'
	#def init_stanza_auto
	
	def print_stanza(self):
		return "auto " + " ".join(self.interfaces)
	#def print_stanza

class StanzaMapping(StanzaBasic):
	def __init__(self,list_interfaces):
		'''
			list_interfaces is list
		'''
		super(StanzaMapping,self).__init__(list_interfaces)
		self.type = 'mapping'
		self.script = {'path':'','order':0}
		self.options = []
	#def __init__
	
	def get_rules(self):
		return self.options
	#def get_rules
	
	def get_script(self):
		return self.script['path']
	#def get_script
	
	def get_all_options(self):
		if ( self.script['path'] == '' ):
			return self.options
		else:
			return self.options[:self.script['order']] + ['script ' + self.script['path']] + self.options[self.script['order']:]
	#def get_all_options
	
	def set_option(self,option_string):
		if (type(option_string) != type('')):
			raise 'Option must be string'
		strip_option = option_string.strip()
		if (strip_option.lower().startswith('script')):
			self.script['order'] = len(self.options)
			self.script['path'] = strip_option[7:]
		else:
			self.options.append(option_string)
		return True
	#def set_option

	def remove_option(self,option_string):
		if option_string in self.options:
			i = self.options.index(option_string)
			if ( self.script['order'] > i ):
				self.script['order'] -= 1;
			return self.options.pop(i)
		else:
			return None
	#def remove_option
	
	def print_stanza(self):
		aux_options = ""
		for x in self.get_all_options():
			aux_options += "\n\t" + x 
		return "mapping " + " ".join(self.interfaces) + aux_options
	#def print_stanza

class StanzaSource:
	def __init__(self,path):
		self.type = 'source'
		self.path = ''
		if(type(path) == type('')):
			self.path = path
		else:
			raise "list_interfaces may be list"
	#def __init__
	
	def set_path(self,path):
		if(type(path) == type('')):
			self.path = path
		else:
			raise "list_interfaces may be list"
		return True
	#def set_path
	
	def print_stanza(self):
		return "source " + self.path
	#def print_stanza

class StanzaAllow(StanzaBasic):
	def __init__(self,allow,list_interfaces):
		'''
			list_interfaces is list
		'''
		super(StanzaAllow,self).__init__(list_interfaces)
		self.type = 'allow'
		self.allow_option = allow[len('allow-'):]
	#def __init__
	
	def print_stanza(self):
		return "allow-" + self.allow_option + " " + " ".join(self.interfaces)
	#def print_stanza

class StanzaIface(StanzaBasic):
	
	def __init__(self,list_interfaces,options):
		'''
			list_interfaces is list
		'''
		super(StanzaIface,self).__init__(list_interfaces)
		self.type = 'iface'
		self.options = []
		self.__list_family = {\
			'inet' :['loopback','static','manual','dhcp','bootp','tunnel','ppp','wvdial','ipv4ll'],\
			'inet6':['auto','loopback','static','manual','dhcp','v4tunnel','6to4'],\
			'can':['static'],\
			'ipx':['static','dynamic']}
		self.family = ''
		self.method = ''
		aux = options.split(" ")
		if (len(aux) == 2 ):
			self.family = aux[0]
			self.method = aux[1]
		elif(len(aux) == 1):
			family = self.__list_family.keys()
			if (aux in family):
				raise "Options hasn't method"
			else:
				for x in family:
					if (aux in self.__list_family[x]):
						self.family = x
						self.method = aux
					else:
						raise "Method not supported"
	#def __init__

	def change_to_dhcp(self):
		if (self.family == 'can' or self.family == 'ipx'):
			raise "Family no support dhcp method"
		self.method = 'dhcp'
		not_removed_options = []
		list_to_remove = ['address','netmask','gateway','network']
		for x in self.options:
			x_lower = x.lower()
			aux_option = x_lower.split(" ")
			if( not aux_option[0] in list_to_remove ):
				not_removed_options.append(x)
		self.options = not_removed_options
		return True
	#def change_to_dhcp

	def change_to_static(self,address,netmask,aux_options=[]):
		if (self.family == 'can' or self.family == 'ipx'):
			raise "Now not support change to static method for family " + self.family
		self.method = 'static'
		not_removed_options = []
		not_removed_options.append('address ' + address)
		not_removed_options.append('netmask ' + netmask)
		not_removed_options = not_removed_options + aux_options
		list_new_options = []
		for x in not_removed_options:
			list_new_options.append(x.split(' ')[0].lower())
			
		for x in self.options:
			x_lower = x.lower()
			aux_option = x_lower.split(" ")
			if( not aux_option[0] in list_new_options ):
				not_removed_options.append(x)
		self.options = not_removed_options
		return True
	#def change_to_static
	
	def set_option(self,option_string):
		if (type(option_string) != type('')):
			raise 'Option must be string'
		strip_option = option_string.strip()
		self.options.append(option_string)
		return True
	#def set_option
	
	def remove_option(self,option_string):
		if option_string in self.options:
			i = self.options.index(option_string)
			return self.options.pop(i)
		else:
			return None
	#def remove_option
	
	def print_stanza(self):
		aux_options = ""
		for x in self.options:
			aux_options += "\n\t" + x 
		return "iface " + " ".join(self.interfaces) + " " + self.family + " " + self.method + aux_options
	#def print_stanza

class StanzaComment:
	def __init__(self,comment):
		self.comment = comment
	#def __init__
	
	def print_stanza(self):
		return self.comment

import os.path
import exceptions
class InterfacesParser:
	def __init__(self,logfile='/tmp/InterfacesParser'):
		self.content = []
		self.stanza_supported = ['iface','allow','auto','source','mapping']
		self.interface_mapping = {}
		self.log_path = logfile
		
	def write_file(self,path):
		output = open(path,'w')
		for x in self.content:
			output.write(x.print_stanza()+"\n")
			#output.write(x+"\n")
	def __insert_interface_reference(self,interface,position):
		if(not self.interface_mapping.has_key(interface)):
			self.interface_mapping[interface] = []
		self.interface_mapping[interface].append(position)
	
	def load(self,path,log_write_method='a'):
		if( not os.path.exists(path)):
			raise "Path " + str(path) + " not exists"
		
		log_fh = open(self.log_path,log_write_method)
		input_file = open(path,'r')
		line = input_file.readline()
		aux_lines = []
		multiline = False
		while line:
			striped_line = line.strip()
			if (not multiline):
				aux_lines.append(striped_line)
			else:
				aux_lines[-1] = aux_lines[-1] + " " + striped_line

			if (striped_line.endswith('\\')):
				if (not striped_line.startswith('#')):
					multiline = True
					aux_lines[-1] = aux_lines[-1][:-1]
				else:
					multiline = False
			else:
				multiline = False
			line = input_file.readline()
		aux_stanza = None
		for x in aux_lines:
			if (x.startswith('#')):
				if (aux_stanza != None):
					self.content.append(aux_stanza)
					aux_stanza = None
				self.content.append(StanzaComment(x))
				continue
			
			
			stanza_splited = x.split(" ")
			if (stanza_splited[0] in self.stanza_supported):
				
				if (aux_stanza != None):
					self.content.append(aux_stanza)
				
				if( len(stanza_splited) < 2):
					log_fh.write("File contain error with '" + " ".join(stanza_splited) + "' .This line will omitted." )
					continue
				if (stanza_splited[0].lower() == 'auto'):
					aux_stanza = StanzaAuto(stanza_splited[1:])
				elif(stanza_splited[0].lower() == 'mapping'):
					aux_stanza = StanzaMapping(stanza_splited[1:])
				elif(stanza_splited[0].lower() == 'source'):
					aux_stanza = StanzaSource(" ".join(stanza_splited[1:]))
				elif(stanza_splited[0].lower() == 'iface'):
					if( len(stanza_splited) < 3):
						log_fh.write("File contain error with '" + " ".join(stanza_splited) + "' .This line will omitted." )
						continue
					aux_stanza = StanzaIface([stanza_splited[1]]," ".join(stanza_splited[2:]))
				else:
					raise "There is a mistake"
				
			elif(stanza_splited[0].lower().startswith('allow')):
				if (aux_stanza != None):
					self.content.append(aux_stanza)
					
				if( len(stanza_splited) < 2):
					log_fh.write("File contain error with '" + " ".join(stanza_splited) + "' .This line will omitted." )
					continue
				aux_stanza = StanzaAllow(stanza_splited[0],stanza_splited[1:])
			else:
				if (aux_stanza != None):
					try:
						aux_stanza.set_option(" ".join(stanza_splited))
					except Exception as e:
						if ('has no attribute \'set_option\'' in e.message):
							log_fh.write("File contain error with '" + " ".join(stanza_splited) + "' .This line is in invalid stanza." )
							continue
						
		if (aux_stanza != None):
			self.content.append(aux_stanza)
			
		for i in range(0,len(self.content)):
			if (hasattr(self.content[i],'get_interfaces')):
				for aux_interface in self.content[i].get_interfaces():
					self.__insert_interface_reference(aux_interface,i)
			
	def get_info_interface(self,interface):
		aux_return = []
		for x in self.interface_mapping[interface]:
			aux_return.append(self.content[x].print_stanza())
		return aux_return
	
	def get_list_interfaces(self):
		return self.interface_mapping.keys()
	
	def change_to_dhcp(self,interface):
		for x in self.interface_mapping[interface]:
			if (hasattr(self.content[x],'change_to_dhcp')):
				self.content[x].change_to_dhcp()
	
	def change_to_static(self,interface,options):
		for x in self.interface_mapping[interface]:
			if (hasattr(self.content[x],'change_to_static')):
				address = options.pop('address')
				netmask = options.pop('netmask')
				list_options = []
				for key in options.keys():
					list_options.append(str(key) + " " + options.pop(key))
				self.content[x].change_to_static(address,netmask,list_options)
import sys

if __name__ == '__main__':
	if (len(sys.argv) > 1):
		p = InterfacesParser()
		p.load(sys.argv[1])
		#p.write_file(sys.argv[2])
		#print p.get_info_interface('eth0')
		#p.change_to_dhcp('eth0')
		p.change_to_static('eth0',{'address':'192.168.1.254','netmask':'255.255.255.0','gateway':'192.168.1.1','network':'192.168.1.0','broadcast':'192.168.1.255'})
		p.write_file(sys.argv[2])
	else:
		print "te falta el fichero"

	'''
	Test 
	
	
	x = StanzaAuto(['eth0'])
	x.append_interface('eth1')
	x.append_interface('eth2')
	x.append_interface('eth4')
	x.append_interface('eth3',3)
	print x.get_interfaces()
	print x.type
	print x.print_stanza()
	
	x = StanzaMapping(['eth0'])
	
	x.append_interface('eth1')
	x.append_interface('eth2')
	x.append_interface('eth4')
	
	x.append_interface('eth3',3)
	print x.get_interfaces()
	print x.type
	
	x.set_option('script /home/kbut/miscript')
	x.set_option('map 11:22:33:44:55:66 lan')
	x.set_option('map AA:BB:CC:DD:EE:FF internet')
	print x.get_rules()
	print x.print_stanza()
	print x.get_rules()
	print x.get_script()
	x.set_option('script /home/kbut/otroscript')
	x.remove_option('map AA:BB:CC:DD:EE:FF internet')
	print x.print_stanza()
	
	x = StanzaAllow('allow-auto',['eth0','eth1'])
	print x.print_stanza()
	
	x = StanzaIface(['eth0'],'inet static')
	x.set_option('address 192.168.1.15')
	x.set_option('netmask 255.255.255.0')
	x.set_option('network 192.168.1.0')
	x.set_option('gateway 192.168.1.1')
	x.set_option('broadcast 255.255.255.255')
	x.set_option('up route add -net 192.168.1.128 netmask 255.255.255.128 gw 192.168.1.2')
	print x.print_stanza()
	print "\n\n"
	x.change_to_dhcp()
	print x.print_stanza()
	print "\n\n"
	x.change_to_static('192.168.1.15','255.255.255.0',['gateway 192.168.1.1','broadcast 255.255.255.128'])
	x.remove_option('broadcast 255.255.255.128')
	print x.print_stanza()
	'''