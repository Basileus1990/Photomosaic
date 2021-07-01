import tkinter
from tkinter import filedialog
from PIL import Image
import numpy
import ctypes
import os


# Takes the image path from the user,
# devides it to squares 10x10pixels
# searches for the most suitable image from the Images
# Connects all images to form a mosaic
# Displays the mosaic and saves it where user decides
class MosaicCreator:
    def __init__(self, main_window):
        self.main_window = main_window

    # main method for creating mosaic. Calls all other needed to complete the proccess
    def create_mosaic(self):
        try:
            #print(self.find_matching_image(['145', '25', '99']))
            #return
            image_path = self.get_user_image_path()
            self.main_window.displayed_image_path = image_path
            tiles, tiles_per_row = self.divide_image(image_path)

            # creates a dictionary of tiles and of average color of these tiles
            tiles_average = [self.calculate_average_color(tile) for tile in tiles]
            for tile in tiles_average:
                print(self.find_matching_image(tile))
        except CreatorError:
            return

    # makes an dialog window pop out which enables the user select a file. Returns a path to this file
    def get_user_image_path(self):
        root = tkinter.Tk()
        root.withdraw()
        return filedialog.askopenfilename()

    # divides an image and returns a list of single tiles as Image objects
    def divide_image(self, image_path):
        try:
            image = Image.open(image_path)
        except Exception:
            ctypes.windll.user32.MessageBoxW(0, 'Couldn\'t open the image. Try selecting again or check if image is not corrupted', '', 0)
            raise CreatorError()

        size = 10 # tile size
        image = image.resize((round(image.size[0]/10)*10, round(image.size[1]/10)*10))
        tiles_per_row = image.size[0]/10
        im = numpy.array(image)
        # Cuts an image into tiles and converts them back into an Image object.
        tiles = [Image.fromarray(numpy.uint8(im[x:x+size, y:y+size])).convert('RGB') for x in range(0,im.shape[0],size) for y in range(0,im.shape[1],size)]
        return [tiles, tiles_per_row]

    # Returns average color of an image taken from the image_path, in RGB string list format
    def calculate_average_color(self, image):
        img = numpy.array(image)
        average_color_per_row = numpy.average(img, axis=0)
        average_color = numpy.average(average_color_per_row, axis=0)
        average_color = [str(int(average_color[0])), str(int(average_color[1])), str(int(average_color[2]))]
        return average_color

    def find_matching_image(self, base_av):
        if os.path.exists(f'{os.getcwd()}/Images/{base_av[0]}/{base_av[1]}/{base_av[2]}/{base_av[0]} {base_av[1]} {base_av[2]}.jpg'):
            return f'{os.getcwd()}/Images/{base_av[0]}/{base_av[1]}/{base_av[2]}/{base_av[0]} {base_av[1]} {base_av[2]}.jpg'

        deviation = 0
        while True:
            new_path = self.check_directories(deviation, f'{os.getcwd()}/Images', base_av)
            if new_path != '':
                return new_path
            deviation += 1

    # a recursive method which checks all directories within deviation and returns it's path if file is found
    # if file is not found, then it returns an empty string
    # deviation -> how many around to search
    # path -> path to the current dictionary
    # base_av -> average color of the base tile
    # level -> which nested directory lever it is in
    # checked_dir -> contains all already checked directories. In those directories it only looks for directories which are a deviation away from it
    def check_directories(self, deviation, path, base_av, level=0, checked_dir=[]):
        if not os.path.exists(path):
            return ''
        elif os.listdir(path) != [] and 'jpg' in os.listdir(path)[0]:
            return path
        else:
            for i in range([0, deviation][path in checked_dir and level == 2], deviation+1):
                new_path = self.check_directories(deviation, f'{path}/{str(int(base_av[level])+i)}',
                                                  base_av, level+1, checked_dir)
                #if not str(int(base_av[level])+i) in checked_dir[level]:
                #    checked_dir[level].append(str(int(base_av[level])+i))
                if new_path != '':
                    return new_path

                new_path = self.check_directories(deviation, f'{path}/{str(int(base_av[level])-i)}',
                                                  base_av, level+1, checked_dir)

                if new_path != '':
                    return new_path
            if level == 2 and not path in checked_dir:
                checked_dir.append(path)
            return ''



# used to exit the MosaicCreator after errors in methods
class CreatorError(Exception):
    pass
