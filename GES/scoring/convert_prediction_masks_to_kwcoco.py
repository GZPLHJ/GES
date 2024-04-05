import kwimage
import kwcoco
import numpy as np
import pandas as pd
import glob
import os.path as osp
import cv2
import tqdm
import argparse

# Input masks should be named as palu-tsunami_{img_id}_{building_id}_dam_pred.png
parser = argparse.ArgumentParser()
parser.add_argument("masks_dir",
        help="path where the mask files are located(pngs)",
        type=str)
parser.add_argument("output_dataset_name",
        help="filename where the kwcoco dataset made from the masks is stored",
        type=str)

args = vars(parser.parse_args())
masks_dir = args['masks_dir']
output_dataset_name = args['output_dataset_name']



#masks_dir = "/data/xbd/palu_single_building_paste_dataset/masks/pngs/"
#output_dataset_name = "/data/xbd/palu_single_building_paste_dataset/pred_ds.kwcoco.json"

def extract_connected_components(mask):
    bboxes = []
    labels = []
    for damage_level in [1,2,3,4]:
        pred_polygons = kwimage.Mask((mask==damage_level).astype(np.uint8), 'c_mask').to_multi_polygon()
        for poly in pred_polygons:
            box = poly.bounding_box()
            bboxes.append(box)
            labels.append(damage_level)
    return bboxes, labels



pred_ds = kwcoco.CocoDataset()
damage_classes = {1:'no-damage', 2:'minor-damage', 3:'major-damage', 4:'destroyed'}
for catname in damage_classes.values():
    pred_ds.add_category(name=catname)

mask_fns = glob.glob(osp.join(masks_dir, "*.png"))
for mask_fn in tqdm.tqdm(mask_fns):
    disaster, img_id, building_id, *_ = osp.basename(mask_fn).split("_")

    gid = pred_ds.add_image(f"{disaster}_{img_id}_{building_id}_post_disaster.tif")

    mask = cv2.imread(mask_fn, cv2.IMREAD_GRAYSCALE)
    bounding_boxes, labels = extract_connected_components(mask)
    for bbox, label in zip(bounding_boxes, labels):
        pred_ds.add_annotation(bbox=bbox.to_xywh(), image_id=gid, category_id=pred_ds.index.name_to_cat[damage_classes[label]]['id'])
pred_ds.dump(output_dataset_name, newlines=True)
