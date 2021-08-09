import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
import threading
from Classes.MosaicCreator import MosaicCreator


class MainWindow(BoxLayout):
    displayed_image_path = StringProperty('')
    progress_bar_value = NumericProperty(0)
    def __init__(self, **kwargs):
        self.image_change_trigger = Clock.create_trigger(self.change_displayed_image_from_thread)
        self.progress_bar_value_trigger = Clock.create_trigger(self.change_progress_bar_value)

        super(MainWindow, self).__init__(*kwargs)
        self.mosaic_creator_thread = threading.Thread(target=MosaicCreator, args=(self, '',''), daemon=True)

    # Will start creating an mosaic. Collecting paths from the user before entering the thread is necessary.
    def start_mosaic_creator_thread(self):
        if not self.mosaic_creator_thread.is_alive():
            image_path = MosaicCreator.get_user_image_path()
            mosaic_path = MosaicCreator.get_user_mosaic_target_path()
            self.mosaic_creator_thread = threading.Thread(target=MosaicCreator, args=(self, image_path, mosaic_path), daemon=True)
            self.mosaic_creator_thread.start()

    # Changes displayed image from another thread.
    def change_displayed_image_from_thread(self, image_path):
        if threading.current_thread() is threading.main_thread():
            self.displayed_image_path = self.new_displayed_image_path
        else:
            self.new_displayed_image_path = image_path
            self.image_change_trigger()

    def change_progress_bar_value(self, value):
        if threading.current_thread() is threading.main_thread():
            self.progress_bar_value = self.new_progress_bar_value
        else:
            self.new_progress_bar_value = value
            self.progress_bar_value_trigger()

class PhotomosaicApp(App):
    def build(self):
        return MainWindow()

if __name__ == "__main__":
    PhotomosaicApp().run()
