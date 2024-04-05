# -*- coding: utf-8 -*-
"""
D:\GuoZhoupeng\xfbd-dataset2\full information 1and2 object images\labels在这个文件夹下有很多个txt标签文件。D:\GuoZhoupeng\xfbd-datasets1\xfbd_yolo\train\images在这个文件下有很多png图片文件，D:\GuoZhoupeng\xfbd-datasets1\xfbd_yolo\train\images在这个文件夹下也有很多txt标签文件。请从D:\GuoZhoupeng\xfbd-datasets1\xfbd_yolo\train\images找到与D:\GuoZhoupeng\xfbd-dataset2\full information 1and2 object images\labels中任何一个文件名字都不相同的图片文件并保存到一个新的文件夹。另外，请从D:\GuoZhoupeng\xfbd-dataset2\full information 1and2 object images\labels找到与D:\GuoZhoupeng\xfbd-dataset2\full information 1and2 object images\labels中任何一个文件名字都不相同的图片文件并保存到一个新的文件夹。需要注意，我说的这个名字不包括后缀。
请写出完整的python代码
"""
import os
import shutil

# 设置两个文件夹的路径
images_dir_1 = r"D:\GuoZhoupeng\xfbd-datasets1\xfbd_aug_cloud_fog_yolo\images\train"
labels_dir_2 = r"D:\GuoZhoupeng\xfbd-dataset2\full information 1and2 object images\labels"

# 创建一个新文件夹来保存不相同文件名的图片
output_dir = r"D:\GuoZhoupeng\xfbd-dataset2\other images augmented\images\train"
os.makedirs(output_dir, exist_ok=True)

# 获取images_dir_1中的所有图片文件名（不包括后缀）
image_names_1 = {os.path.splitext(file)[0] for file in os.listdir(images_dir_1) if file.endswith(".png")}

# 获取labels_dir_2中的所有标签文件名（不包括后缀）
label_names_2 = {os.path.splitext(file)[0] for file in os.listdir(labels_dir_2) if file.endswith(".txt")}

# 找到不相同的文件名（不包括后缀）
unique_image_names = image_names_1.difference(label_names_2)

# 复制不相同文件名的图片到新文件夹
for image_name in unique_image_names:
    image_file = os.path.join(images_dir_1, image_name + ".png")
    output_file = os.path.join(output_dir, image_name + ".png")
    shutil.copy(image_file, output_file)

print(f"共找到 {len(unique_image_names)} 个不相同的图片文件，并已保存到 {output_dir} 文件夹中。")
