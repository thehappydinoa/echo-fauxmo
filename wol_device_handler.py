''' 
|  @file wol_device_handler.py
|  @brief Wake-over-lan device handlers
|  
'''
import fauxmo, fauxmo_basics, aquos, fmip, socket, logging, time, sys, os
import itach_device_handler as itach
from wakeonlan import wol

logging.basicConfig(level=logging.DEBUG)

device_ips = {'itach':'192.168.1.111',
			  'tv':'192.168.1.12',
			  'blueray':'192.168.1.27',
			  'dvr':'192.168.1.100',
			  'xbox':'192.168.1.4',
			  'laptop':'192.168.1.21'}
			  
device_ports = {'itach':4998,
				'xbox':5050}

xbox_live_id = ''
computer_mac_address = '80:19:34:4D:07:60'
icloud_username = ''
icloud_password = ''


class xbox_handler(fauxmo_basics.debounce_handler):
	starting_port = 52000
	device_names = ["xbox"]

	def act(self, client_address, state, name):
		xbox_live_id = xbox_live_id.encode()
		xbox_power_payload = b'\x00' + chr(len(xbox_live_id)).encode() + xbox_live_id + b'\x00'
		xbox_power_header = b'\xdd\x02\x00' + chr(len(power_payload)).encode() + b'\x00\x00'
		xbox_power_packet = power_header + power_payload
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.setblocking(0)
		sock.bind(("", 0))
		sock.connect((device_ips['xbox'], device_ports['xbox']))
		logging.debug("Sending power on packets to " + device_ips['xbox'])
		for i in range(0, 5):
			sock.send(xbox_power_packet)
			time.sleep(1)
		return True
		
class bluetooth_handler(fauxmo_basics.debounce_handler):
	starting_port = 52100
	device_names = ["bluetooth speaker"]

	def act(self, client_address, state, name):
		send_command('itach','stereo_input_tv')
		return True
		
class apple_tv_handler(fauxmo_basics.debounce_handler):
	starting_port = 52200
	device_names = ["apple tv"]

	def act(self, client_address, state, name):
		send_command('itach','stereo_input_sat')
		return True
		
class laptop_handler(fauxmo_basics.debounce_handler):
	starting_port = 52300
	device_names = ["laptop"]
	
	def act(self, client_address, state, name):
		wol.send_magic_packet(computer_mac_address)
		logging.debug("Wake-over-lan magic packet sent to " + computer_mac_address)
		
class find_my_iphone_handler(fauxmo_basics.debounce_handler):
	starting_port = 52400
	device_names = ["find my iPhone"]
	
	def act(self, client_address, state, name):
		fmip.play_sound_device1(icloud_username,icloud_password)

if __name__ == "__main__":
	os.system("clear")
	fauxmo.DEBUG = True
	p = fauxmo.poller()
	u = fauxmo.upnp_broadcast_responder()
	u.init_socket()
	p.add(u)

	handler_list = [xbox_handler,bluetooth_handler,apple_tv_handler,laptop_handler,find_my_iphone_handler]
	
	for handler_index,handler in enumerate(handler_list):
		handler = handler_list[handler_index]()
		for device_index,device in enumerate(handler.device_names):
			fauxmo.fauxmo(device, u, p, None, handler.starting_port+device_index, handler)

	logging.debug("Entering fauxmo polling loop")
	while True:
		try:
			p.poll(100)
			time.sleep(0.1)
		except Exception, e:
			logging.critical("Critical exception: " + str(e))
			break