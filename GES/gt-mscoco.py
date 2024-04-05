import os
import cv2
import json

# 定义输入目录、输出目录和标签文件路径
input_dir = r'E:\xfbd_clusters_n-bi3\data\coco\val2017'  # 输入图片文件夹路径
output_dir = r'E:\xfbd_clusters_n-bi3\data\coco\gtaaaaval2017'  # 输出图片文件夹路径
label_file = r'E:\xfbd_clusters_n-bi3\data\coco\annotations\instances_val2017.json'  # MSCOCO标签文件路径

# 创建输出目录
os.makedirs(output_dir, exist_ok=True)

# 读取MSCOCO标签文件
with open(label_file, 'r') as file:
    data = json.load(file)

# 遍历标签数据
for item in data['images']:
    image_id = item['id']
    image_file = os.path.join(input_dir, item['file_name'])
    annotations = [ann for ann in data['annotations'] if ann['image_id'] == image_id]

    if not annotations:
        continue

    image = cv2.imread(image_file)

    for annotation in annotations:
        category_id = annotation['category_id']
        bbox = annotation['bbox']

        x, y, width, height = map(int, bbox)
        cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)

    output_file = os.path.join(output_dir, os.path.basename(image_file))
    cv2.imwrite(output_file, image)

print("目标检测完成，结果图片保存在", output_dir)
