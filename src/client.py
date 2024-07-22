import json, os
from utils import load_json, save_json

# THE CLIENT LOGIC FILE
import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.clock import mainthread
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.video import Video
from kivy.core.window import Window


# networking includes
import socket
import struct
import marshal
import threading


# network settings
MCAST_GRP = '224.1.1.1'
MCAST_PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# sock.bind((MCAST_GRP, MCAST_PORT))
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


class MulticastListenerThread(threading.Thread):
    def __init__(self, sock, sm):
        threading.Thread.__init__(self)
        self.sock = sock
        self.sm = sm

    def run(self):
        while True:
            received_data = self.sock.recv(10240)
            received_dict = marshal.loads(received_data)
            received_dict['sender_ip'] = socket.inet_ntoa(received_data[0:4])  # Extract sender's IP address
            print(f"received: {received_dict}")
            if 'type' in received_dict:
                if received_dict['type'] == 'test':
                    self.root.updateStatus(received_dict['value'])
                else:
                    self.sm.changeMedia(received_dict['value'])
                    




class ClientScreen(Screen):
    
    def on_leave(self, *args):
        # print("LEFT SCREEN")
        pass
        
        
    def on_duration_change(instance, value=None):
        print('The duration of the video is', value)
    def on_position_change(instance, value=None):
        # print('The position in the video is', value)
        pass
    def on_eos_change(instance, value=None):
        print('The EOS of the video is', value)
    
        
    def updateStatus(self, text):
        self.ids.status_text.text = text
        
    @mainthread
    def playMedia(self, path, options=None): 
        vid = self.ids.videoplayer
        fullpath = config['media_path'] + "/" + path
        print(f"Loading media: {fullpath}")
        vid.source = fullpath
        vid.state = 'play'
        vid.opacity = 1 #just because the initial state is transparent
        self.updateStatus(f"playing media: {fullpath}")
        pass
    

class customScreenManager(ScreenManager):
    @mainthread
    def changeMedia(self, path):
        print("Changing Media")
        old_screen = self.get_screen(self.current)
        new_screen = self.get_screen(self.next())
        new_screen.playMedia(path)
        self.current = new_screen.name

    
class ClientApp(App):
        
    def build(self):
        # Set the window properties
        # Window.size = (Window.width, Window.height)
        # Window.size = (config['width'], config['height'])
        # Window.borderless = show['window']['borderless']
        # Window.fullscreen = show['window']['fullscreen']
        # Window.show_cursor = show['window']['show_cursor']
        
        # Create the screen manager
        sm = customScreenManager(transition=FadeTransition(duration=1))
        # sm = customScreenManager()
        sm.add_widget(ClientScreen(name='s1'))
        sm.add_widget(ClientScreen(name='s2'))
        
        listener_thread = MulticastListenerThread(sock, sm)
        listener_thread.setDaemon(True)
        listener_thread.start() 
        
        return sm
        
    

#*********** 
# set the global variable "CONFIG" for the client. should never be re-written by program
config = {}
#load settings file, or default
if os.path.exists('client.json'):
    config = load_json('client.json')
print("config:")
print(config)
#******** end config setup

#*********** 
# set the global variable "show" for the client.
# this is written to as needed by the client and saved whenever updated with received data from server
show = {}
#load settings file, or default
showfile = config['media_path'] + '/show.json'
if not os.path.exists(showfile):
    showfile = 'default_show.json'
show = load_json(showfile)
print("show:")
print(show)
#******** end show setup

if __name__ == "__main__":
    ClientApp().run()