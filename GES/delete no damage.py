# import os
# import shutil
# import random
# from PIL import Image, ImageDraw
#
# # 设置输入和输出文件夹的路径
# input_image_folder = r"D:\GuoZhoupeng\datasets\xfbd_aug_cloud_fog_yolo - delete\images\train"
# input_label_folder = r"D:\GuoZhoupeng\datasets\xfbd_aug_cloud_fog_yolo - delete\labels\train"
# output_image_folder = r"D:\GuoZhoupeng\datasets\xfbd_aug_cloud_fog_yolo - delete\images_de\train"
# output_label_folder = r"D:\GuoZhoupeng\datasets\xfbd_aug_cloud_fog_yolo - delete\labels_de\train"
#
# # 创建输出文件夹
# os.makedirs(output_image_folder, exist_ok=True)
# os.makedirs(output_label_folder, exist_ok=True)
#
# label_files = os.listdir(input_label_folder)
#
# for label_file in label_files:
#     with open(os.path.join(input_label_folder, label_file), 'r') as f:
#         lines = f.readlines()
#
#     new_lines = []
#     image_name = label_file.replace(".txt", ".png")
#     image_path = os.path.join(input_image_folder, image_name)
#     output_image_path = os.path.join(output_image_folder, image_name)
#     output_label_path = os.path.join(output_label_folder, label_file)
#
#     image = Image.open(image_path)
#     draw = ImageDraw.Draw(image)
#
#     for line in lines:
#         parts = line.split()
#         class_id = int(parts[0])
#         if class_id == 0 and random.random() < 0.9:
#             continue
#
#         new_lines.append(line)
#
#         x_center = float(parts[1]) * image.width
#         y_center = float(parts[2]) * image.height
#         width = float(parts[3]) * image.width
#         height = float(parts[4]) * image.height
#
#         x_min = int(x_center - width / 2)
#         y_min = int(y_center - height / 2)
#         x_max = int(x_center + width / 2)
#         y_max = int(y_center + height / 2)
#
#         if class_id == 0:
#             draw.rectangle([x_min, y_min, x_max, y_max], fill='black')
#
#     image.save(output_image_path)
#
#     with open(output_label_path, 'w') as f:
#         f.writelines(new_lines)


import os
import shutil
import random
from PIL import Image, ImageDraw

# 设置输入和输出文件夹的路径
input_image_folder = r"D:\GuoZhoupeng\datasets\xfbd_aug_cloud_fog_yolo - delete\images\train"
input_label_folder = r"D:\GuoZhoupeng\datasets\xfbd_aug_cloud_fog_yolo - delete\labels\train"
output_image_folder = r"D:\GuoZhoupeng\datasets\xfbd_aug_cloud_fog_yolo - delete\images_de30\train"
output_label_folder = r"D:\GuoZhoupeng\datasets\xfbd_aug_cloud_fog_yolo - delete\labels_de30\train"

# 创建输出文件夹
os.makedirs(output_image_folder, exist_ok=True)
os.makedirs(output_label_folder, exist_ok=True)

label_files = os.listdir(input_label_folder)

for label_file in label_files:
    with open(os.path.join(input_label_folder, label_file), 'r') as f:
        lines = f.readlines()

    new_lines = []
    image_name = label_file.replace(".txt", ".png")
    image_path = os.path.join(input_image_folder, image_name)
    output_image_path = os.path.join(output_image_folder, image_name)
    output_label_path = os.path.join(output_label_folder, label_file)

    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    for line in lines:
        parts = line.split()
        class_id = int(parts[0])
        x_center = float(parts[1]) * image.width
        y_center = float(parts[2]) * image.height
        width = float(parts[3]) * image.width
        height = float(parts[4]) * image.height

        x_min = int(x_center - width / 2)
        y_min = int(y_center - height / 2)
        x_max = int(x_center + width / 2)
        y_max = int(y_center + height / 2)

        if class_id == 0 and random.random() < 0.6:
            draw.rectangle([x_min, y_min, x_max, y_max], fill='black')
        else:
            new_lines.append(line)

    image.save(output_image_path)

    with open(output_label_path, 'w') as f:
        f.writelines(new_lines)

