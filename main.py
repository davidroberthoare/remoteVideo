import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
# from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
# from kivy.core.video import Video
from kivy.uix.video import Video
from kivy.core.window import Window

class KivyApp(App):
    def build(self):
        # Set the window properties
        Window.size = (Window.width, Window.height)
        Window.borderless = True
     #    Window.fullscreen = True

        # Create a FloatLayout as the main window
        main_window = GridLayout(cols=1)

        # Add an Image widget to the main window
     #    image_path1 = "media/test1.jpg"
     #    image1 = Image(source=image_path1, keep_ratio=True, allow_stretch=True)
     #    main_window.add_widget(image1)

     #    image_path2 = "media/test3.jpg"
     #    image2 = Image(source=image_path2, keep_ratio=True, allow_stretch=True)
     #    image2.opacity = 0.5  # Set the initial opacity to 50%
     #    main_window.add_widget(image2)
        
          # Add a Video widget to the main window
        video_path = "media/test1.mp4" 
        video = Video(source=video_path, state='play', eos='loop')
        main_window.add_widget(video)
        
        # Add a VideoImage widget to the main window
     #    video_image = VideoImage(source=video_path, state='play', loop='repeat')
     #    main_window.add_widget(video_image)

        # Define the fade function
     #    self.fadeAmount = 0.01
     #    def fade_image(dt):
     #      if video.opacity < 0 or video.opacity > 1:
     #           self.fadeAmount *= -1     
     #      video.opacity += self.fadeAmount

        # Start the clock to call the fade function every 2 seconds
     #    Clock.schedule_interval(fade_image, 0.01)

        return main_window


if __name__ == "__main__":
    KivyApp().run()