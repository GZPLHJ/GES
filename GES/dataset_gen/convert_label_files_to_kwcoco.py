'''
导入所需的库和模块，包括 NumPy、Pandas、os、kwimage、kwcoco、glob、tqdm 和 argparse。
创建一个命令行参数解析器（argparse.ArgumentParser）。
定义两个命令行参数，分别是 "labels_dir" 和 "output_dataset_name"。
解析命令行参数，并将它们存储在变量 args 中。
从命令行参数中获取标签文件所在的目录路径和输出数据集的文件名。
创建一个 kwcoco.CocoDataset 对象（gt_ds）来存储标签数据集。
定义一个包含损伤类别的列表（damage_classes）。
使用 gt_ds.add_category() 方法为每个损伤类别添加一个分类。
使用 glob.glob() 函数获取标签文件目录中所有符合特定条件（post.json）的文件列表（label_files）。
遍历每个标签文件：
从标签文件路径中提取图像文件名（image_filename）。
使用 gt_ds.add_image() 方法将图像添加到数据集中，并获取图像的唯一标识符（gid）。
载入标签文件中的标签数据（labels）。
遍历每个标签：
根据标签中的几何信息创建一个边界框（bbox）。
获取标签的损伤级别（damage_level）。
如果损伤级别不在损伤类别列表中，则跳过该标签。
获取损伤级别对应的分类对象（cat）。
使用 gt_ds.add_annotation() 方法将标注信息添加到数据集中。
使用 gt_ds.dump() 方法将数据集以 kwcoco 格式保存到指定的输出文件中。
**************************************************************************************************************
*脚本的目的是将指定目录中的标签文件（JSON格式）转换为 kwcoco 数据集，并保存为特定的输出文件。数据集中包含图像、标注边界框和分类信息。*
**************************************************************************************************************
KWCOCO（kwimage COCO）和 COCO（Common Objects in Context）数据集是用于计算机视觉任务的两种不同的数据集格式。
COCO 数据集是一个广泛使用的数据集，用于目标检测、实例分割和关键点检测等计算机视觉任务。它由微软团队创建，并提供了统一的数据格式和标注标准。COCO 数据集的标注信息以 JSON 格式存储，包括图像路径、对象类别、边界框位置、关键点位置等。COCO 数据集的设计目标是提供一个大规模、多样化和具有挑战性的数据集，用于评估计算机视觉算法的性能。
KWCOCO 是一个基于 COCO 数据集格式的 Python 包，扩展了 COCO 数据集的功能。KWCOCO 提供了一系列用于读取、操作和处理 COCO 数据集的工具和函数。它增加了对一些特殊数据类型的支持，例如多边形、遮罩、关键点等，并提供了更多的数据操作和查询功能。KWCOCO 还提供了对图像处理、对象检测、实例分割等常见任务的支持，使得在 COCO 数据集上进行数据处理和算法开发更加方便。
因此，可以说 KWCOCO 是 COCO 数据集的一个增强版本，提供了更多的功能和工具，使得在 COCO 数据集上的数据处理和算法开发更加便捷。它是建立在 COCO 数据集基础上的一个扩展，旨在提供更多的灵活性和功能性。
'''
import numpy as np
import pandas as pd
import os
import os.path as osp
import kwimage
import kwcoco
import glob
import tqdm
import argparse
from single_building_copy_paste import BuildingPaster

parser = argparse.ArgumentParser()
parser.add_argument("labels_dir",default=r'E:\labels_val',
                    help="path where the label files are located",
                    type=str)
parser.add_argument(
    "output_dataset_name",default=r'E:\xfbd_hold_val_label_kwcoco.json',
    help="filename where the kwcoco dataset made from the labels is stored",
    type=str)

args = vars(parser.parse_args())
labels_dir = args['labels_dir']
output_dataset_name = args['output_dataset_name']

gt_ds = kwcoco.CocoDataset()
damage_classes = ['no-damage', 'minor-damage', 'major-damage', 'destroyed']
for catname in damage_classes:
    gt_ds.add_category(name=catname)

label_files = glob.glob(osp.join(labels_dir, "*post*.json"))
for label_file in (file_pbar := tqdm.tqdm(label_files)):
    image_filename = osp.basename(label_file).replace(".json", ".tif")
    gid = gt_ds.add_image(image_filename)
    labels = BuildingPaster.load_labels(label_file)
    for label in (label_pbar := tqdm.tqdm(labels['features']['xy'],
                                          leave=False)):
        bbox = kwimage.Polygon.from_wkt(label['wkt']).bounding_box()
        damage_level = label['properties']['subtype']
        if damage_level not in damage_classes:
            continue

        cat = gt_ds.index.name_to_cat[damage_level]
        gt_ds.add_annotation(bbox=bbox, image_id=gid, category_id=cat['id'])

gt_ds.dump(output_dataset_name, newlines=True)
