# THE CLIENT LOGIC FILE
import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.clock import mainthread
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
sock.bind((MCAST_GRP, MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


class MulticastListenerThread(threading.Thread):
    def __init__(self, sock, root):
        threading.Thread.__init__(self)
        self.sock = sock
        self.root = root

    def run(self):
        while True:
            received_data = self.sock.recv(10240)
            received_dict = marshal.loads(received_data)
            received_dict['sender_ip'] = socket.inet_ntoa(received_data[0:4])  # Extract sender's IP address
            print(f"received: {received_dict}")
            if 'type' in received_dict:
                if received_dict['type'] == 'test':
                    self.root.updateStatus(received_dict['value'])
                    
                elif received_dict['type'] == 'image':
                    self.root.updateStatus(received_dict['value'])
                    self.root.playImage(received_dict['value'])
                    
                elif received_dict['type'] == 'video':
                    self.root.updateStatus(received_dict['value'])
                    self.root.playVideo(received_dict['value'])




class ClientLayout(FloatLayout):
    
    def on_duration_change(instance, value=None):
        print('The duration of the video is', value)
    def on_position_change(instance, value=None):
        # print('The position in the video is', value)
        pass
    def on_eos_change(instance, value=None):
        print('The EOS of the video is', value)
    
    @mainthread
    def toTop(self, player):
        self.ids.image1.opacity = 0
        self.ids.video1.opacity = 0
        player.opacity = 1   #on top
        
    def updateStatus(self, text):
        self.ids.status_text.text = text
    @mainthread
    def playImage(self, path, options=None):
        img = self.ids.image1
        img.source = path
        self.toTop(img)
        self.updateStatus(f"playing image: {path}")
        pass
    @mainthread
    def playVideo(self, path, options=None): 
        vid = self.ids.video1
        vid.source = path
        self.toTop(vid)
        
        vid.state = 'play'
        self.updateStatus(f"playing video: {path}")
        pass
    
    # # # Define the fade function
    # # self.fadeAmount = 0.01
    # # def fade_image(dt):
    # #     image = self.root.ids.video
    # #     if image.opacity < 0 or image.opacity > 1:
    # #         self.fadeAmount *= -1     
    # #     image.opacity += self.fadeAmount

    # # # Start the clock to call the fade function every 2 seconds
    # # Clock.schedule_interval(fade_image, 0.01)
    
    
        
    
class ClientApp(App):
        
    def build(self):
        # Set the window properties
        Window.size = (Window.width, Window.height)
        # Window.borderless = True
        # Window.fullscreen = True
        Window.show_cursor = False
        
        root = ClientLayout()
        # root.playImage("media/test1.jpg")
        # root.playVideo("media/test3.mp4")
        
        
        listener_thread = MulticastListenerThread(sock, root)
        listener_thread.setDaemon(True)
        listener_thread.start() 
        
        return root


if __name__ == "__main__":
    ClientApp().run()