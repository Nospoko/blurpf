import os
import cv2
import numpy as np
from glob import glob

def crop_images():
    """ Utility for movie creation """
    paths = glob('imgs/*.png')

    # For some reason on ubuntu it is not automatic
    paths.sort()

    for path in paths:
        img = cv2.imread(path)
        # Negotiate with resolution
        frame = img[250 : 650, 50 : 850, :]
        savepath = 'imgs/cropped/' + os.path.split(path)[1]
        cv2.imwrite(savepath, frame)
        # Show progress
        print savepath

def make_movie_frames():
    """ Straight to youtube """
    paths = glob('imgs/*.png')
    paths.sort()

    border = cv2.imread('borders/stars_320p.png')
    hsv_border = cv2.cvtColor(border, cv2.COLOR_BGR2HSV)

    # Make copy of the hue part
    hue_border = np.copy(hsv_border[:, :, 0])
    hamp = 255 - hue_border.max()

    print 'Using border with resolution:', hue_border.shape

    for it, path in enumerate(paths):
        # Read image and cut
        img = cv2.imread(path)
        # Adjust manually
        xim_sta, xim_end = 85, 215
        yim_sta, yim_end = 25, 295
        croped = img[xim_sta:xim_end, yim_sta : yim_end, :]

        # Prepare funky border
        hue_shift = 0.5*(1+np.sin(it/60.)) * hamp
        hsv_border[:, :, 0] = hue_border + int(hue_shift)
        border = cv2.cvtColor(hsv_border, cv2.COLOR_HSV2BGR)

        # Put image in border
        bx_sta = 25
        bx_end = bx_sta + xim_end - xim_sta
        by_sta = 25
        by_end = by_sta + yim_end - yim_sta
        # border[25:155, :,:] = croped
        border[bx_sta:bx_end, by_sta:by_end,:] = croped

        # Write to disk
        savepath = 'imgs/movie/' + os.path.split(path)[1]
        cv2.imwrite(savepath, border)

        if it%20 == 0: print it

