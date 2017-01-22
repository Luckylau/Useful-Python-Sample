'''
author: Lucky lau
email:laujunbupt0913@163com

classify Pic_files by jpg,gif,png
'''

import os
import glob
import shutil
import platform
import sys


def check_platform():
    if platform.system() != 'Windows':
        return False
    return True


def get_Pics():

    jpg_files = glob.glob('*.[Jj][Pp][Gg]')
    png_files = glob.glob('*.[Pp][Nn][Gg]')
    gif_files = glob.glob('*.[Gg][Ii][Ff]')

    if len(jpg_files) and len(png_files) and len(gif_files) == 0:
        print ("There is no Pic files")
        if check_platform():
            os.system("pause")
            sys.exit(0)
    return jpg_files, png_files, gif_files


def classify_Pics(jpg_files, png_files, gif_files):

    if not os.path.exists('JPG') and len(jpg_files) != 0:
        os.mkdir('JPG')
    if not os.path.exists('PNG') and len(png_files) != 0:
        os.mkdir('PNG')
    if not os.path.exists('GIF') and len(gif_files) != 0:
        os.mkdir('GIF')

    if jpg_files:
        for jpg_file in jpg_files:
            print(
                "Move %s to %s " %
                (jpg_file,
                 os.path.join(
                     '\JPG',
                     jpg_file)))
            try:
                shutil.move(jpg_file, './JPG')
            except shutil.Error as e:
                print (e)
    if png_files:
        for png_file in png_files:
            print(
                "Move %s to %s " %
                (png_file,
                 os.path.join(
                     '\PNG',
                     png_file)))
            try:
                shutil.move(png_file, './PNG')
            except shutil.Error as e:
                print (e)

    if gif_files:
        for gif_file in gif_files:
            print(
                "Move %s to %s " %
                (gif_file,
                 os.path.join(
                     '\GIF',
                     gif_file)))
            try:
                shutil.move(gif_file, './GIF')
            except shutil.Error as e:
                print (e)

    print (" All Pic are classified ")

if __name__ == '__main__':

    if not check_platform():
        print ('Not in Windows')
    jpg_files, png_files, gif_files = get_Pics()
    classify_Pics(jpg_files, png_files, gif_files)
    sys.exit(0)
