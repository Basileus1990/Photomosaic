import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

from Classes.GoogleImageDownloader import GoogleImageDownloader
from Classes.MosaicCreator import MosaicCreator


class MainWindow(BoxLayout):
    displayed_image_path = StringProperty('')
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(*kwargs)
        self.google_image_downloader = GoogleImageDownloader()
        self.mosaic_creator = MosaicCreator(self)


class PhotomosaicApp(App):
    def build(self):
        return MainWindow()

if __name__ == "__main__":
    PhotomosaicApp().run()
