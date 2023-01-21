import tkinter
from tkinter import filedialog
from PIL import Image
import numpy
import ctypes
import os
import winsound


# devides it to squares 20x20pixels
# searches for the most suitable images from the Images
# Connects all images to form a mosaic
# Displays the mosaic and saves it where user decided
class MosaicCreator:
    def __init__(self, main_window, image_path, mosaic_path):
        if image_path == '' or mosaic_path=='':
            ctypes.windll.user32.MessageBoxW(0, 'You didn\'t select your image or your target directory. Please try again', '', 0)
            return

        self.main_window = main_window
        self.image_path = image_path
        self.mosaic_path = mosaic_path

        try:
            self.main_window.change_displayed_image_from_thread(self.image_path)
            tiles, original_image, tiles_per_row = self.divide_image()
            self.number_of_tiles = len(tiles)
            self.number_of_tiles_found = 0

            # creates a dictionary of tiles and of average color of these tiles
            average_tile_colors = [self.calculate_average_color(tile) for tile in tiles]
            average_tile_paths = [self.find_matching_image(average_color) for average_color in average_tile_colors]

            # mosaic = self.combine_tiles([Image.open(im_path) for im_path in average_tile_paths], original_image, tiles_per_row)
            mosaic = self.combine_tiles(average_tile_paths, original_image, tiles_per_row)
            self.save_mosaic(mosaic)

        except Exception as e:
            if str(e) != '':
                with open(f'{os.getcwd()}\\Error Log.txt', 'a') as error_file:
                    error_file.write(f'{e}\n\n')
            else:
                ctypes.windll.user32.MessageBoxW(0, 'Something went wrong. Please try again. If it doesn\'t help, try with another image', '', 0)
            return


    # makes an dialog window pop out which enables the user select a file. Returns a path to this file
    def get_user_image_path():
        root = tkinter.Tk()
        root.withdraw()
        return filedialog.askopenfilename(title='Select your image')

    # makes an dialog window pop out which enables the user select a folder. Returns a path to this filder
    def get_user_mosaic_target_path():
        root = tkinter.Tk()
        root.withdraw()
        return filedialog.askdirectory(title='Select a directory where you want to save your mosaic')

    # Resises the image to make it divisible by size of tiles
    # divides an image and returns a list of single tiles as Image objects,
    # the original image and number of tiles per row
    def divide_image(self):
        try:
            image = Image.open(self.image_path)
        except Exception:
            ctypes.windll.user32.MessageBoxW(0, 'Couldn\'t open the image. Try selecting again or check if image is not corrupted', '', 0)
            raise Exception()

        size = 20 # tile size
        image = image.resize((round(image.size[0]/size)*size, round(image.size[1]/size)*size))
        tiles_per_row = round(image.size[0]/size)
        im = numpy.array(image)
        # Cuts an image into tiles and converts them back into an Image object.
        tiles = [Image.fromarray(numpy.uint8(im[x:x+size, y:y+size])).convert('RGB') for x in range(0,im.shape[0],size) for y in range(0,im.shape[1],size)]
        return [tiles, image, tiles_per_row]

    # Returns average color of an image as a RGB string list format
    def calculate_average_color(self, image):
        img = numpy.array(image)
        average_color_per_row = numpy.average(img, axis=0)
        average_color = numpy.average(average_color_per_row, axis=0)
        average_color = [str(int(average_color[0])), str(int(average_color[1])), str(int(average_color[2]))]
        return average_color

    # Searches the Image folder for suitable images and updates the progress bar
    def find_matching_image(self, base_av):
        self.number_of_tiles_found += 1
        new_progress_bar_value = round((self.number_of_tiles_found/self.number_of_tiles)*100)
        if new_progress_bar_value != self.main_window.progress_bar_value:
            self.main_window.change_progress_bar_value(new_progress_bar_value)

        if os.path.exists(f'{os.getcwd()}/Images/{base_av[0]}/{base_av[1]}/{base_av[2]}/{base_av[0]} {base_av[1]} {base_av[2]}.jpg'):
            return f'{os.getcwd()}/Images/{base_av[0]}/{base_av[1]}/{base_av[2]}/{base_av[0]} {base_av[1]} {base_av[2]}.jpg'

        deviation = 0
        while True:
            new_path = self.check_directories(deviation, f'{os.getcwd()}/Images', base_av)
            if new_path != '':
                print(new_path)
                return f'{new_path}/{os.listdir(new_path)[0]}'
            deviation += 1

    # a recursive method which checks all directories within deviation and returns it's path if file is found
    # if file is not found, then it returns an empty string
    # deviation -> how many around to search
    # path -> path to the current dictionary
    # base_av -> average color of the base tile
    # level -> which nested directory lever it is in
    # checked_dir -> contains all already checked directories. In those directories it only looks for directories which are a deviation away from it
    def check_directories(self, deviation, path, base_av, level=0, checked_dir=[]):
        if not os.path.exists(path) or os.listdir(path) == []:
            return ''
        elif 'jpg' in os.listdir(path)[0]:
            return path
        else:
            for i in range([0, deviation][path in checked_dir and level == 2], deviation+1):
                new_path = self.check_directories(deviation, f'{path}/{str(int(base_av[level])+i)}',
                                                  base_av, level+1, checked_dir)
                if new_path != '':
                    return new_path

                new_path = self.check_directories(deviation, f'{path}/{str(int(base_av[level])-i)}',
                                                  base_av, level+1, checked_dir)

                if new_path != '':
                    return new_path
            if level == 2 and not path in checked_dir:
                checked_dir.append(path)
            return ''

    # Combines all tiles into a full image and returns it
    def combine_tiles(self, average_tiles_paths, original_image, tiles_per_row):
        total_width = original_image.size[0]
        total_height = original_image.size[1]
        with Image.open(average_tiles_paths[0]) as average_tile:
            tile_size = average_tile.size[0]
        new_image = Image.new('RGB', (total_width, total_height))

        y_offset = 0
        x_offset = 0
        for i in range(len(average_tiles_paths)):
            with Image.open(average_tiles_paths[i]) as average_tile:
                new_image.paste(average_tile, (x_offset, y_offset))
                x_offset += tile_size
                if (i + 1) % tiles_per_row == 0:
                    y_offset += tile_size
                    x_offset = 0

        return new_image

    # saves the mosaic in a folder given by the user and names it.
    def save_mosaic(self, mosaic):
        mosaic_name = 'Mosaic.jpg'
        for i in range(1, 9999999):
            if mosaic_name in os.listdir(self.mosaic_path):
                mosaic_name = f'Mosaic{i}.jpg'
                continue
            break
        self.mosaic_path = f'{self.mosaic_path}/{mosaic_name}'
        mosaic.save(self.mosaic_path)
        print(self.mosaic_path)
        self.main_window.change_progress_bar_value(0)
        self.main_window.change_displayed_image_from_thread(self.mosaic_path)

        winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
