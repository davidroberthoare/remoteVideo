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

# other misc libraries
import json, os

# network settings
MCAST_GRP = '224.1.1.1'
MCAST_PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((MCAST_GRP, MCAST_PORT))
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
        print("LEFT SCREEN")
        
        
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
        vid.source = path
        
        vid.state = 'play'
        vid.opacity = 1
        self.updateStatus(f"playing video: {path}")
        pass
    

class customScreenManager(ScreenManager):
    @mainthread
    def changeMedia(self, path):
        print("Changing Media")
        old_screen = self.get_screen(self.current)
        new_screen = self.get_screen(self.next())
        new_screen.playMedia(path)
        # time.sleep(1)
        self.current = new_screen.name
        # time.sleep(2)

    
class ClientApp(App):
        
    def build(self):
        # Set the window properties
        Window.size = (Window.width, Window.height)
        Window.borderless = show['window']['borderless']
        Window.fullscreen = show['window']['fullscreen']
        Window.show_cursor = show['window']['show_cursor']
        # Window.clearcolor = (0, 0, 0, 1)
        # Window.clear()
        
        # Create the screen manager
        sm = customScreenManager(transition=FadeTransition(duration=1))
        sm.add_widget(ClientScreen(name='s1'))
        sm.add_widget(ClientScreen(name='s2'))
        
        listener_thread = MulticastListenerThread(sock, sm)
        listener_thread.setDaemon(True)
        listener_thread.start() 
        
        return sm
        
    



def load_show(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    else:
        print(f"The file {file_path} does not exist.")
        return {}

def save_show(show):
    sorted_show = dict(sorted(show.items()))
    with open('media/show.json', 'w') as f:
        json.dump(sorted_show, f, indent=4)


#*********** 
# set the global variable "show" for the client.
# this is written to as needed by the client and saved whenever updated with received data from server
show = {}
#load settings file, or default
if os.path.exists('media/show.json'):
    show = load_show('media/show.json')
else:
    show = load_show('default_show.json')
print("show:")
print(show)
#******** end show setup

if __name__ == "__main__":
    ClientApp().run()