# THE CLIENT LOGIC FILE
import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.video import Video
from kivy.core.window import Window


class ServerApp(App):
    def build(self):
        # Set the window properties
        Window.size = (Window.width, Window.height)
        Window.borderless = True
     #    Window.fullscreen = True

        # Define the fade function
        self.fadeAmount = 0.01
        def fade_image(dt):
            image = self.root.ids.video
            if image.opacity < 0 or image.opacity > 1:
                self.fadeAmount *= -1     
            image.opacity += self.fadeAmount

        # Start the clock to call the fade function every 2 seconds
        Clock.schedule_interval(fade_image, 0.01)


if __name__ == "__main__":
    ServerApp().run()