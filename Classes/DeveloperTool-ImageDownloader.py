import cv2
import numpy
import os
import winsound
import google_images_download
from PIL import Image


# Type here the keys of your search. The keys have to be separated by a comma.
# For each key the script will download and process 100 images
# Only English characters search keys
keys = ''
keys = keys.split(',')

def download_images_with_gid():

    response = google_images_download.googleimagesdownload()

    for key in keys:
        argument = {'keywords':key, 'limit':100}
        paths = response.download(argument)
        paths = list(paths[:len(paths)-1][0].values())[0]
        for path in paths:
            try:
                image = Image.open(path)
            except Exception:
                continue
            try:
                image = image.convert('RGB')
                image = image.resize((20, 20))
                image_name = get_image_name(path)
                image.save(path)
                average_color = calculate_average_color(path)
                new_path = get_new_image_path(average_color)
                print(new_path)

                os.rename(path, f'{new_path}{average_color[0]} {average_color[1]} {average_color[2]}.jpg')
                os.remove(path)
            except Exception as e:
                try:
                    os.remove(path)
                except Exception as e:
                    continue
                continue
    winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)

def check_if_base_dir_exists():
    if not os.path.exists(f'./{self._Base_Directory}'):
        os.mkdir(self._Base_Directory)

# Returns average color of an image taken from the image_path, in RGB string list format
def calculate_average_color(image_path):
    myimg = cv2.imread(image_path)
    avg_color_per_row = numpy.average(myimg, axis=0)
    avg_color = numpy.average(avg_color_per_row, axis=0)
    avg_color = [str(int(avg_color[0])), str(int(avg_color[1])), str(int(avg_color[2]))]
    return avg_color[::-1]


# Returns the name of a file from the given path
def get_image_name(img_path):
    return img_path[len(img_path) - img_path[::-1].find('\\'):]

# returns new image path, if directories don't exist then it creates them
def get_new_image_path(average_color):
    path = f'{os.path.dirname(os.getcwd())}\\Images\\'
    for av_color in average_color:
        if not os.path.exists(f'{path}{av_color}'):
            os.mkdir(f'{path}{av_color}')
        path += f'{av_color}\\'
    return path

if __name__ == '__main__':
    download_images_with_gid()
