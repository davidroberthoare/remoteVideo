import json, os
from utils import load_json, save_json

# THIS IS THE SERVER LOGIC FILE

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

# NETWORKING
import socket
from time import sleep, time
import marshal
import threading

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 8080
MULTICAST_TTL = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

def broadcast(data_dict):
    data_dict['timestamp'] = time()
    try:
        sock.sendto(marshal.dumps(data_dict), (MCAST_GRP, MCAST_PORT))
    except Exception as e:
        print(f"Error sending data: {e}")
        

class MulticastBroadcasterThread(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock

    def run(self):
        while True:
            print("sending multicast packet...")
            message = {"hello": "world"}
            broadcast(message) 
            sleep(2)
            
            

class ServerLayout(BoxLayout):
    def test(self, arg1):
        print(f"Test Pressed {arg1}")
        broadcast({"type":"test", "value":f"button {arg1}"}) 
    
    def triggerMedia(self, path):
        print(f"trigger media {path}")
        broadcast({"type":"image", "value":path}) 
    

class ServerApp(App):
    def build(self):
        Window.size = (config['width'], config['height'])
        
        broadcaster_thread = MulticastBroadcasterThread(sock)
        broadcaster_thread.setDaemon(True)
        broadcaster_thread.start() 
        
        return ServerLayout()



#*********** 
# set the global variable "CONFIG" for the client. should never be re-written by program
config = {}
#load settings file, or default
if os.path.exists('server.json'):
    config = load_json('server.json')
print("config:")
print(config)
#******** end config setup



if __name__ == "__main__":
    ServerApp().run()