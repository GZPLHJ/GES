import numpy as np
import pandas as pd
import glob
import argparse
import os.path as osp
import os
from single_building_copy_paste import BuildingPaster

import matplotlib.pyplot as plt
import cv2
import rasterio
import json
import tqdm

from utils import save_labels, save_image

parser = argparse.ArgumentParser()
parser.add_argument(
    "original_xbd_dir",
    help=
    "path (under which are dirs \"images\", and \"labels\") to the original .tif xbd data",
    type=str)
parser.add_argument("secondary_pre_images_dir",
                    help="path where the secondary image tifs reside",
                    type=str)
parser.add_argument("output_dir",
                    help="path where the output images and labels are put",
                    type=str)

args = vars(parser.parse_args())
original_xbd_dir = args['original_xbd_dir']
secondary_pre_images_dir = args['secondary_pre_images_dir']
output_dir = args['output_dir']

for folder in ['images', 'labels']:
    os.makedirs(osp.join(output_dir, folder), exist_ok=True)

original_pre_image_files = glob.glob(
    osp.join(original_xbd_dir, "images/*pre*.tif"))

n_files_used = 0
for original_pre_image_file in (file_pbar :=
                                tqdm.tqdm(original_pre_image_files)):
    disaster, img_id, _, _ = osp.basename(original_pre_image_file).split("_")
    file_pbar.set_description(f"{disaster} {img_id}")
    original_post_image_file = original_pre_image_file.replace("pre", "post")
    secondary_pre_image_file = glob.glob(
        osp.join(secondary_pre_images_dir, f"*{disaster}_{img_id}*.tif"))
    if len(secondary_pre_image_file) == 1:
        secondary_pre_image_file = secondary_pre_image_file[0]
    else:
        print("unable to find single match for this pre image, skipping")
        continue

    label_file = osp.join(original_xbd_dir,
                          f"labels/{disaster}_{img_id}_post_disaster.json")

    bp = BuildingPaster(original_pre_image_file, original_post_image_file,
                        secondary_pre_image_file, label_file)

    if len(bp) > 0:
        n_files_used += 1

    for building_idx in (building_pbar := tqdm.tqdm(range(len(bp)),
                                                    leave=False)):
        pasted_data = bp[building_idx]

        new_pre_image, new_pre_image_profile, pasted_post_image, pasted_post_image_profile, pasted_labels, pasted_buid = \
                pasted_data["pre_image"], \
                pasted_data["pre_image_profile"],\
                pasted_data["post_image"],\
                pasted_data["post_image_profile"],\
                pasted_data["new_annotation"],\
                pasted_data["pasted_buid"]

        building_pbar.set_description(f"{pasted_buid}")

        pre_image_fn = osp.join(
            output_dir,
            f"images/{disaster}_{img_id}_{pasted_buid}_pre_disaster.tif")
        post_image_fn = osp.join(
            output_dir,
            f"images/{disaster}_{img_id}_{pasted_buid}_post_disaster.tif")
        label_fn = osp.join(
            output_dir,
            f"labels/{disaster}_{img_id}_{pasted_buid}_post_disaster.json")

        save_image(pre_image_fn, new_pre_image, new_pre_image_profile)
        save_image(post_image_fn, pasted_post_image, pasted_post_image_profile)
        save_labels(label_fn, pasted_labels)
print(f"# files used: {n_files_used}")
