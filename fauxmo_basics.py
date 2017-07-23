''' 
|  @file fauxmo_basics.py
|  @brief Basic Functions for Fauxmo Handlers
|  
'''

import time, socket, logging, sys, os

def send_command(ip, command):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((device_ips[device], device_ports[device]))
	sock.settimeout(2)
	logging.debug("Sending command: " + command + " to " + device)
	sock.sendall(commands[command]+"\r")
	msg = sock.recv(4096)
	logging.debug("Recevied message: " + msg + " from " + device)
	sock.close()
	del sock
	return True

def ping(ip):
	results = os.system("ping -c1 -W2 -q " + ip)
	return (results == 0)

class debounce_handler(object):
    """Use this handler to keep multiple Amazon Echo devices from reacting to
       the same voice command.
    """
    DEBOUNCE_SECONDS = 0.3

    def __init__(self):
        self.lastEcho = time.time()

    def on(self, client_address, name):
        if self.debounce():
            return True
        return self.act(client_address, True, name)

    def off(self, client_address, name):
        if self.debounce():
            return True
        return self.act(client_address, False, name)

    def act(self, client_address, state):
        pass

    def debounce(self):
        if (time.time() - self.lastEcho) < self.DEBOUNCE_SECONDS:
            return True

        self.lastEcho = time.time()
        return False