'''
导入所需的库和模块，包括 NumPy、cv2、single_building_copy_paste、os.path、glob、tqdm、os、shapely.geometry、shapely.wkt、argparse、rasterio 和 utils。
创建一个命令行参数解析器（argparse.ArgumentParser）。
定义两个命令行参数，分别是 "dataset_dir" 和 "output_masks_dir"。
解析命令行参数，并将它们存储在变量 args 中。
从命令行参数中获取数据集所在的目录路径和输出掩膜文件存储的目录路径。
创建两个子目录 "pngs" 和 "tifs" 在输出掩膜文件存储目录中，用于存储生成的 PNG 和 TIFF 格式的掩膜图像。
使用 glob.glob() 函数获取标签文件目录中所有符合特定条件（"labels/*.json"）的文件列表（label_files）。
遍历每个标签文件：
从标签文件路径中提取图像文件名（image_filename）。
使用 BuildingPaster.load_image_with_geoprofile() 方法加载图像和其地理信息概要文件（profile）。
载入标签文件中的标签数据（labels）。
创建一个空的掩膜图像（mask_img）作为输出掩膜。
定义一个字典（dmg_type），将不同的损伤类型映射到整数标签。
根据标签数据中的几何信息和损伤类型，将相应的多边形区域填充到掩膜图像中。
根据输出文件名的规则，保存掩膜图像为 PNG 和 TIFF 格式的文件，分别存储在 "pngs" 和 "tifs" 子目录下。
***********************************************************************************************************************************************
*总之，以上代码的目的是从数据集中的标签文件中加载标签信息和图像，根据标签中的几何信息和损伤类型生成对应的掩膜图像，并将生成的掩膜图像以 PNG 和 TIFF 格式保存到指定的输出目录中*
***********************************************************************************************************************************************


'''

import numpy as np
import cv2
from single_building_copy_paste import BuildingPaster
import os.path as osp
import glob
import tqdm
import os

from shapely.geometry import Polygon
from shapely import wkt
import argparse

import rasterio
from utils import save_image, save_labels

parser = argparse.ArgumentParser()
parser.add_argument(
    "dataset_dir",
    help=
    "path where the dataset of interest (with subfolders \"labels\" and \"images\" are located",
    type=str)
parser.add_argument("output_masks_dir",
                    help="where the generated masks are stored",
                    type=str)

args = vars(parser.parse_args())
dataset_dir = args['dataset_dir']
output_masks_dir = args['output_masks_dir']

for folder in ['pngs', 'tifs']:
    os.makedirs(osp.join(output_masks_dir, folder), exist_ok=True)

label_files = glob.glob(osp.join(dataset_dir, "labels/*.json"))
for label_file in tqdm.tqdm(label_files):
    image_filename = osp.basename(label_file).replace(".json", ".tif")
    image, profile = BuildingPaster.load_image_with_geoprofile(
        osp.join(dataset_dir, f"images/{image_filename}"))

    labels = BuildingPaster.load_labels(label_file)
    height, width = 1024, 1024
    mask_img = np.zeros([height, width], dtype=np.uint8)
    dmg_type = {
        "background": 0,
        "no-damage": 1,
        "minor-damage": 2,
        "major-damage": 3,
        "destroyed": 4,
        "un-classified": 5,
    }
    polys_sorted = {a: [] for a in dmg_type.keys()}

    for pidx in range(len(labels['features']['xy'])):
        poly = Polygon(wkt.loads(labels['features']['xy'][pidx]['wkt']))
        damage_level = labels['features']['xy'][pidx]['properties']['subtype']
        poly = (np.array(list(poly.exterior.coords)).round().astype(
            np.int32).reshape(-1, 1, 2))
        if damage_level == 'un-classified':
            continue
        polys_sorted[damage_level].append(poly)
    for k, v in polys_sorted.items():
        cv2.fillPoly(mask_img, v, [dmg_type[k]])

    output_fn = f"{image_filename.replace('post_disaster', 'dam_target')}"
    save_image(
        osp.join(output_masks_dir,
                 f"pngs/{output_fn.replace('.tif', '.png')}"), mask_img)
    save_image(osp.join(output_masks_dir, f"tifs/{output_fn}"),
               mask_img,
               profile=profile)
    #output_fn = output_fn.replace("dam_target", "loc_target")
    #loc_mask = (mask_img > 0).astype(np.uint8)
    #save_image(osp.join(output_masks_dir, f"pngs/{output_fn.replace('.tif', '.png')}"), loc_mask)
    #save_image(osp.join(output_masks_dir, f"tifs/{output_fn}") , loc_mask, profile=profile)
