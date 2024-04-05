import cv2
import rasterio
import json 
import numpy as np

def save_image(fn, image, profile=None):
    if len(image.shape) == 3 and image.shape[2] == 3: #RGB
        if profile is None:
            cv2.imwrite(fn, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        else:
            with rasterio.open(fn, 'w', **profile) as dst:
                dst.write(image.transpose(2,0,1))
    elif len(image.shape) == 2:#image.shape[2] == 1: #grayscale
        if profile is None:
            cv2.imwrite(fn, image)
        else:
            profile['count'] = 1
#            profile['nodata'] = 0
#            profile['dtype'] = rasterio.uint8
            #print(profile)
            with rasterio.open(fn, 'w', **profile) as dst:
                dst.write(image, 1)
    else:
        print("unable to save file")


def save_labels(fn, labels):
    with open(fn, 'w') as outfile:
        json.dump(labels, outfile, indent=4)
