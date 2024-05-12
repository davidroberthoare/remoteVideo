import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.window import Window

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

        # Define the fade function
        self.fadeAmount = 0.01
        def fade_image(dt):
          if image2.opacity < 0 or image2.opacity > 1:
               self.fadeAmount *= -1     
          image2.opacity += self.fadeAmount

        # Start the clock to call the fade function every 2 seconds
        Clock.schedule_interval(fade_image, 0.01)

        return main_window


if __name__ == "__main__":
    KivyApp().run()