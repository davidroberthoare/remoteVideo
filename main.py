import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.video import Video
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle


class KivyApp(App):
    def build(self):
        # Set the window properties
        Window.size = (Window.width, Window.height)
        Window.borderless = True
     #    Window.fullscreen = True

        # Create a FloatLayout as the main window
        main_window = FloatLayout()

        # Add an Image widget to the main window
        image_path1 = "media/test1.jpg"
        image1 = Image(source=image_path1, keep_ratio=True, allow_stretch=True)
        main_window.add_widget(image1)

        image_path2 = "media/test3.jpg"
        image2 = Image(source=image_path2, keep_ratio=True, allow_stretch=True)
        image2.opacity = 0.5  # Set the initial opacity to 50%
        main_window.add_widget(image2)
        
        # Add a Video widget to the main window
        video_path = "media/test1.mp4" 
        video = Video(source=video_path, state='play', eos='loop', keep_ratio=True, allow_stretch=True)
        main_window.add_widget(video)
        

        # Define the fade function
        self.fadeAmount = 0.01
        def fade_image(dt):
          if video.opacity < 0 or video.opacity > 1:
               self.fadeAmount *= -1     
          video.opacity += self.fadeAmount

        # Start the clock to call the fade function every 2 seconds
        Clock.schedule_interval(fade_image, 0.01)
        
        
        # Add a Canvas widget to draw a black rectangle as the initial background
        with main_window.canvas:
            Color(0, 0, 0, 1)  # Set the color to black
            Rectangle(pos=(0, 0), size=(Window.width, Window.height))  # Draw a rectangle that covers the entire window


        return main_window


if __name__ == "__main__":
    KivyApp().run()