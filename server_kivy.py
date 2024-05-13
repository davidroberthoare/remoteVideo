# THIS IS THE SERVER LOGIC FILE

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.video import Video
from kivy.core.window import Window

class ServerLayout(BoxLayout):
    def test(self, arg1):
        print(f"Test Pressed {arg1}")
    pass
    

class ServerApp(App):
    def build(self):
        Window.size = (Window.width, Window.height)
        return ServerLayout()


if __name__ == "__main__":
    ServerApp().run()