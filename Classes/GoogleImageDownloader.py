from google_images_search import GoogleImagesSearch
import pathlib
import json
import cv2
import numpy
import os
import ctypes
import traceback
from PIL import UnidentifiedImageError


# Downloads images from google of a given key. Then it resizes
# it and calculates the average color and saves the image in a proper directory.
# If the directory doesn't exist then it creates a one

class GoogleImageDownloader:
    _Base_Directory = 'Images' # Base image directory name

    def __init__(self):
        self.check_if_base_dir_exists()

    # checks if base directory exists, if not then it creates it
    def check_if_base_dir_exists(self):
        if not os.path.exists(f'./{self._Base_Directory}'):
            os.mkdir(self._Base_Directory)

    # downloads, resizes and saves images in a directory responding to it's average color
    def download_images(self, key):
        if key == '':
            ctypes.windll.user32.MessageBoxW(0, 'Keyword can\'t be empty', '', 0)
            return

        keys = self.get_keys()
        gis = GoogleImagesSearch(keys['API key'], keys['Search_ID'])
        to_download = 100    # How many images it should download
        _search_params = {
            'q': key,
            'num': to_download,
        }

        try:
            gis.search(search_params=_search_params)
        except Exception as e:
            if 'HttpError 429' in str(e):
                print(e)
                ctypes.windll.user32.MessageBoxW(0, 'Daily limit of downloaded images has been reached. Please try again tommorow', '', 0)
            else:
                try:
                    git.next_page()  # Tries to search for images again. If it also fails displays an error message
                except:
                    ctypes.windll.user32.MessageBoxW(0, 'Something went wrong. Try again or try a different keyword', '', 0)
            return

        while to_download > 0:
            for image in gis.results():
                try:
                    image.download(f'{pathlib.Path().absolute()}\Images')
                except Exception:
                    continue
                is_image_corrupted = False
                try:
                    image.resize(20, 20)
                    image_name = self.get_image_name(image.path)
                    average_color = self.calculate_average_color(f'Images\\{image_name}')
                    new_path = self.get_new_image_path(average_color)

                    os.rename(f'.\\Images\\{image_name}', f'{new_path}{average_color[0]} {average_color[1]} {average_color[2]}.jpg')
                    to_download -= 1
                    if to_download <= 0:
                        break

                except UnidentifiedImageError:
                    is_image_corrupted = True
                except FileExistsError:
                    os.remove(image.path)
                except Exception:
                    traceback.print_exc()
                    try:
                        os.remove(image.path)
                    except Exception:
                        print('Couldn\'t remove the image')
                        traceback.print_exc()

                if is_image_corrupted:
                    try:
                        os.remove(image.path)
                    except Exception:
                        print('Couldn\'t remove the corrupted image')
                        traceback.print_exc()

            if to_download > 0:
                try:
                    gis.next_page()
                except Exception as e:
                    if 'HttpError 429' in str(e):
                        ctypes.windll.user32.MessageBoxW(0, 'Daily limit of downloaded images has been reached. Please try again tommorow', '', 0)
                    else:
                        try:
                            git.next_page()  # Tries to search for images again. If it also fails displays an error message
                        except:
                            ctypes.windll.user32.MessageBoxW(0, 'Something went wrong. Try again or try a different keyword', '', 0)
                    return
        ctypes.windll.user32.MessageBoxW(0, 'Finished downloading', '', 0)

    # Returns average color of an image taken from the image_path, in RGB string list format
    def calculate_average_color(self, image_path):
        img = cv2.imread(image_path)
        average_color_per_row = numpy.average(img, axis=0)
        average_color = numpy.average(average_color_per_row, axis=0)
        average_color = [str(int(average_color[0])), str(int(average_color[1])), str(int(average_color[2]))]
        return average_color[::-1]


    # Returns the name of a file from the given path
    def get_image_name(self, img_path):
        return img_path[len(img_path) - img_path[::-1].find('\\'):]

    # returns new image path, if directories don't exist then it creates them
    def get_new_image_path(self, average_color):
        path = '.\\Images\\'
        for av_color in average_color:
            if not os.path.exists(f'{path}{av_color}'):
                os.mkdir(f'{path}{av_color}')
            path += f'{av_color}\\'
        return path


    # returns API key and Search ID from a json. If json doesn't exist then it raises an error
    def get_keys(self):
        try:
            with open(f'{pathlib.Path().absolute()}\Data\Keys.json','r') as file:
                keys = json.load(file)
        except Exception as e:
            raise BaseException('Can\'t get key data')
        return keys
