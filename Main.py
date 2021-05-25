import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from Classes.GoogleImageDownloader import GoogleImageDownloader
from Classes.MosaicCreator import MosaicCreator


class MainWindow(BoxLayout):
    google_image_downloader = GoogleImageDownloader()
    mosaic_creator = MosaicCreator()


class PhotomosaicApp(App):
    def build(self):
        return MainWindow()

if __name__ == "__main__":
    PhotomosaicApp().run()
