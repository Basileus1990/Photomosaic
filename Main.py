import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from Classes.GoogleImageDownloader import GoogleImageDownloader


class MainWindow(BoxLayout):
    google_image_downloader = GoogleImageDownloader()


class PhotomosaicApp(App):
    def build(self):
        return MainWindow()

if __name__ == "__main__":
    PhotomosaicApp().run()
