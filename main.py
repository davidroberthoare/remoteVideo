import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.window import Window

class KivyApp(App):
    def build(self):
          # Set the window properties
          #    Window.size = (Window.width, Window.height)
          Window.borderless = True
          #    Window.fullscreen = True

          # Create a GridLayout as the main window
          main_window = FloatLayout()

          # Add an Image widget to the main window
          image_path1 = "media/test1.jpg"
          image1 = Image(source=image_path1, keep_ratio=True, allow_stretch=True)
          main_window.add_widget(image1)

          image_path2 = "media/test3.jpg"
          image2 = Image(source=image_path2, keep_ratio=True, allow_stretch=True)
          image2.opacity = 0.5 
          main_window.add_widget(image2)

          return main_window


if __name__ == "__main__":
    KivyApp().run()