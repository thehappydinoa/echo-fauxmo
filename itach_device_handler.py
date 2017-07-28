''' 
|  @file itach_device_handler.py
|  @brief iTach device handlers
|  
'''
import fauxmo, fauxmo_basics, aquos, fmip, socket, logging, time, sys, os
import wol_device_handler as itach
from wakeonlan import wol

logging.basicConfig(level=logging.DEBUG)


class tv_handler(fauxmo_basics.debounce_handler):
	starting_port = 51100
	device_names = ["tv", "television"]
		
	def on(self, client_address, name):
		if not(fauxmo_basics.ping(fauxmo_basics.device_ips['tv'])):
			fauxmo_basics.send_command('itach','tv_toggle')
		return True
		
	def off(self, client_address, name):
		if (fauxmo_basics.ping(fauxmo_basics.device_ips['tv'])):
			fauxmo_basics.send_command('itach','tv_toggle')
		return True
		
class stereo_handler(fauxmo_basics.debounce_handler):
	starting_port = 51200
	device_names = ["stereo"]

	def act(self, client_address, state, name):
		fauxmo_basics.send_command('itach','stero_toggle')
		fauxmo_basics.send_command('itach','stereo_input_tv') # Temp change to SAT input
		return True
		
class dvr_handler(fauxmo_basics.debounce_handler):
	starting_port = 51300
	device_names = ["dvr", "cable"]
		
	def on(self, client_address, name):
		fauxmo_basics.send_command('itach','dvr_toggle')
		if not(fauxmo_basics.ping(fauxmo_basics.device_ips['tv'])):
			aquos.aquos.set_ip(fauxmo_basics.device_ips['tv'])
			aquos.aquos.set_tv_input(1)
		return True
		
	def off(self, client_address, name):
		fauxmo_basics.send_command('itach','dvr_toggle')
		return True	
		
class blueray_handler(fauxmo_basics.debounce_handler):
	starting_port = 51400
	device_names = ["blueray", "blueray player"]
		
	def on(self, client_address, name):
		if not(fauxmo_basics.ping(fauxmo_basics.device_ips['blueray'])):
			fauxmo_basics.send_command('itach','blueray_toggle')
			fauxmo_basics.send_command('itach','stereo_input_bd')
		if not(fauxmo_basics.ping(fauxmo_basics.device_ips['tv'])):
			aquos.aquos.set_ip(fauxmo_basics.device_ips['tv'])
			aquos.aquos.set_tv_input(2)
		return True
		
	def off(self, client_address, name):
		if (fauxmo_basics.ping(fauxmo_basics.device_ips['blueray'])):
			fauxmo_basics.send_command('itach','blueray_toggle')
			fauxmo_basics.send_command('itach','stereo_input_sat')
		return True

if __name__ == "__main__":
	os.system("clear")
	fauxmo.DEBUG = True
	p = fauxmo.poller()
	u = fauxmo.upnp_broadcast_responder()
	u.init_socket()
	p.add(u)

	handler_list = [tv_handler,stereo_handler,dvr_handler,blueray_handler]
	
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