import os.path


class StanzaBasic(object):
	def __init__(self,list_interfaces):
		'''
			list_interfaces is list
		'''
		self.type = ''
		self.interfaces = []
		if isinstance(list_interfaces,list):
			for i in list_interfaces:
				self.interfaces.append(i)
		else:
			raise Exception("list_interfaces may be list")
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
		try:
			self.interfaces.remove(interface)
			return interface
		except:
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
		if not isinstance(option_string,str):
			raise Exception('Option must be string')
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
			raise Exception("list_interfaces may be list")
	#def __init__
	
	def set_path(self,path):
		if(type(path) == type('')):
			self.path = path
		else:
			raise Exception("list_interfaces may be list")
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
				raise Exception("Options hasn't method")
			else:
				for x in family:
					if (aux in self.__list_family[x]):
						self.family = x
						self.method = aux
					else:
						raise Exception("Method not supported")
	#def __init__

	def change_to_dhcp(self):
		if (self.family == 'can' or self.family == 'ipx'):
			raise Exception("Family no support dhcp method")
		self.method = 'dhcp'
		not_removed_options = []
		list_to_remove = ['address','netmask','gateway','network','dns-search']
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
			raise Exception("Now not support change to static method for family " + self.family)
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
	
	def set_option(self,option_string,unique=False):
		if not isinstance(option_string,str):
			raise Exception('Option must be string')
		strip_option = option_string.strip()
		if unique:
			if strip_option in self.options:
				return True
		self.options.append(option_string)
		return True
	#def set_option
	
	def remove_option(self,option_string,startswith=False):
		if (startswith):
			return_list = []
			for i in range(len(self.options)-1,-1,-1):
				if self.options[i].startswith(option_string):
					return_list.append(self.options.pop(i))
			return return_list
		if (option_string in self.options):
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

	def check_option(self,option,contain=False):
		if option in self.options:
			return True
		if contain:
			for aux_option in self.options:
				if aux_option.startswith(option):
					return True
		return False


	def change_ip(self,ip):
		if self.method != 'static' :
			raise Exception("This interface isn't on static configuration")
		for x in range(0,len(self.options)):
			if self.options[x].startswith('address'):
				self.options[x] = 'address ' + ip
				return True
		self.options.append('address ' + ip)
		return True
	#def change_ip

	def change_netmask(self,netmask):
		if self.method != 'static' :
			raise Exception("This interface isn't on static configuration")
		for x in range(0,len(self.options)):
			if self.options[x].startswith('netmask'):
				self.options[x] = 'netmask ' + netmask
				return True
		self.options.append('netmask ' + netmask)
		return True
	#def change_netmask



class StanzaComment:
	def __init__(self,comment):
		self.comment = comment
	#def __init__
	
	def print_stanza(self):
		return self.comment

class InterfacesParser:
	def __init__(self,logfile='/tmp/InterfacesParser'):
		self.content = []
		self.stanza_supported = ['iface','allow','auto','source','mapping']
		self.interface_mapping = {}
		self.log_path = logfile
		self.path = ""		
	def write_file(self,path):
		output = open(path,'w')
		for x in self.content:
			output.write(x.print_stanza()+"\n")
			#output.write(x+"\n")
	def print_file(self):
		result = ""
		for x in self.content:
			result += x.print_stanza()+"\n"
		return result
	def __insert_interface_reference(self,interface,stanza):
		if(not interface in self.interface_mapping.keys()):
			self.interface_mapping[interface] = []
		self.interface_mapping[interface].append(stanza)	
	def load(self,path,log_write_method='a'):
		if( not os.path.exists(path)):
			raise Exception("Path " + str(path) + " not exists")
		'''
		Clean vars
		'''
		self.content = []
		self.interface_mapping = {}
		'''
		Clean vars
		'''
		
		log_fh = open(self.log_path,log_write_method)
		self.path = path
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
					raise Exception("There is a mistake")
				
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
			
		for stanza in self.content:
			if (hasattr(stanza,'get_interfaces')):
				for aux_interface in stanza.get_interfaces():
					self.__insert_interface_reference(aux_interface,stanza)	
	def get_info_interface(self,interface):
		aux_return = []
		if interface in self.interface_mapping:
			for stanza in self.interface_mapping[interface]:
				aux_return.append(stanza.print_stanza())
		return aux_return
	def get_real_list_interfaces(self):
		list_of_interfaces = []
		if os.path.exists('/proc/net/dev'):
			f = open('/proc/net/dev','r')
			lines = f.readlines()
			for x in lines[2:	]:
				try: 
					list_of_interfaces.append(x.split(':')[0].strip())
				except:
					pass
		return list_of_interfaces
	def get_list_interfaces(self):
		return self.interface_mapping.keys()	
	def change_to_dhcp(self,interface):
		for stanza in self.interface_mapping[interface]:
			if (hasattr(stanza,'change_to_dhcp')):
				stanza.change_to_dhcp()	
	def change_to_static(self,interface,options):
		for stanza in self.interface_mapping[interface]:
			if (hasattr(stanza,'change_to_static')):
				address = options.pop('address')
				netmask = options.pop('netmask')
				list_options = []
				for key in options.keys():
					list_options.append(str(key) + " " + options[key])
				stanza.change_to_static(address,netmask,list_options)
	def update_dns(self,interface,dns):
		for stanza in self.interface_mapping[interface]:
			if (hasattr(stanza,'remove_option')):
				stanza.remove_option('dns-nameservers',startswith=True)
				for key in dns:
					if key.strip() != "" :
						stanza.set_option('dns-nameservers ' + key)
	def change_option_sysctl(self,file_path,needle,value):
		if (os.path.exists(file_path)):
			f = open(file_path,'r')
			lines = f.readlines()
			f.close()
		else:
			lines = []
		found = False
		f = open(file_path,'w')
		for x in lines:
			if(needle in x):
				f.write(value+"\n")
				found = True
				continue
			f.write(x)
		if (not found):
			f.write(value+"\n")
		f.close()	
	def enable_forwarding_ipv4(self,persistent=False):
		if (persistent):
			self.change_option_sysctl('/etc/sysctl.d/network-parser-forwarding.conf','net.ipv4.ip_forward','net.ipv4.ip_forward=1')
		f = open('/proc/sys/net/ipv4/ip_forward','w')
		f.write('1')
		f.close()	
	def disable_forwarding_ipv4(self,persistent=False):
		if (persistent):
			self.change_option_sysctl('/etc/sysctl.d/network-parser-forwarding.conf','net.ipv4.ip_forward','net.ipv4.ip_forward=0')
		f = open('/proc/sys/net/ipv4/ip_forward','w')
		f.write('0')
		f.close()
	def enable_forwarding_ipv6(self,persistent=False):
		if (persistent):
			self.change_option_sysctl('/etc/sysctl.d/network-parser-forwarding.conf','net.ipv6.conf.all.forwarding','net.ipv6.conf.all.forwarding=1')
		f = open('/proc/sys/net/ipv6/conf/all/forwarding','w')
		f.write('1')
		f.close()
	def disable_forwarding_ipv6(self,persistent=False):
		if (persistent):
			self.change_option_sysctl('/etc/sysctl.d/network-parser-forwarding.conf','net.ipv6.conf.all.forwarding','net.ipv6.conf.all.forwarding=0')
		f = open('/proc/sys/net/ipv6/conf/all/forwarding','w')
		f.write('0')
		f.close()
	def is_enable_forwarding_ipv4(self):
		try:
			f = open('/proc/sys/net/ipv4/ip_forward')
		except:
			return False
		try:
			result = f.readlines()[0].strip()
		except:
			result = '0'
		f.close()
		if (result == '0'):
			return False
		else:
			return True
	def is_enable_forwarding_ipv6(self):
		try:
			f = open('/proc/sys/net/ipv6/conf/all/forwarding')
		except:
			return False
		try:
			result = f.readlines()[0].strip()
		except:
			result = '0'
		f.close()
		if (result == '0'):
			return False
		else:
			return True	
	def enable_nat(self,interfaces_list,internal_interfaces_script):
		if not isinstance(interfaces_list,list):
			raise Exception("interfaces must be list")
		for x in interfaces_list:
			if ( x in self.interface_mapping.keys()):
				for stanza in self.interface_mapping[x]:
					if(stanza.__class__.__name__ == 'StanzaIface'):
						stanza.set_option('up enablenat A ' + internal_interfaces_script,unique=True)
			else:
				raise Exception("Interface " + x  + " is not defined on " + self.path)
	def disable_nat(self, interfaces_list):
		if not isinstance(interfaces_list,list):
			raise Exception("interfaces must be list")
		for x in interfaces_list:
			if ( x in self.interface_mapping.keys()):
				for stanza in self.interface_mapping[x]:
					if(stanza.__class__.__name__ == 'StanzaIface'):
						stanza.remove_option('up enablenat',startswith=True)
			else:
				raise Exception("Interface " + x  + " is not defined on " + self.path)
	def insert_stanza(self, stanza):
		if stanza.__class__.__name__ in ['StanzaIface','StanzaAuto','StanzaComment','StanzaMapping','StanzaSource']:
			self.content.append(stanza)
			if (hasattr(stanza,'get_interfaces')):
				for aux_interface in stanza.get_interfaces():
					self.__insert_interface_reference(aux_interface,stanza)
		else:
			raise Exception("Stanza not supported")
	def get_nat_persistent(self,interface):
		for stanza in self.interface_mapping[str(interface)]:
			if(stanza.__class__.__name__ == 'StanzaIface'):
				for x in stanza.options:
					if 'up enablenat' in x:
						return True
		return False
	def get_routing_persistent(self, type):
		if str(type) == 'ipv4':
			needle = 'net.ipv4.ip_forward'
		elif str(type) == 'ipv6':
			needle = 'net.ipv6.conf.all.forwarding'
		else:
			raise Exception("Type not supported")
		try:
			f = open('/etc/sysctl.d/network-parser-forwarding.conf','r')
		except :
			return False
		
		lines = f.readlines()
		for x in lines:
			if x.strip().startswith(needle):
				try:
					return bool(int(x.split('=')[1]))
				except Exception:
					return False

	def delete_all_interface(self,interface):
		try:
			self.__delete_stanza(interface,StanzaBasic)
			return True
		except:
			return False
	def auto_toggle(self,interface,status):
		if status:
			if interface in self.interface_mapping:
				for stanza in self.interface_mapping[interface]:
					if isinstance(stanza,StanzaAuto):
						return True
			aux_stanza = StanzaAuto([interface])
			self.insert_stanza(aux_stanza)
		else:
			self.delete_auto(interface)
			return True

	def delete_auto(self,interface):
		try:
			self.__delete_stanza(interface,StanzaAuto)
			return True
		except:
			return False

	def __delete_stanza(self,interface,objectclass):
		if interface in self.interface_mapping.keys():
			for index in range(len(self.interface_mapping[interface]) -1 , -1 , -1):
				stanza = self.interface_mapping[interface][index]
				if isinstance(stanza,objectclass):
					self.__delete_interface(interface,stanza)
			if len(self.interface_mapping[interface]) <= 0:
				self.interface_mapping.pop(interface)

	def __delete_interface(self,interface,stanza):
		stanza.remove_interface(interface)
		self.interface_mapping[interface].remove(stanza)
		if len(stanza.get_interfaces()) <= 0 :
			self.content.remove(stanza)
		