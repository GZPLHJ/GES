"""
要求：
D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\center txt ++9 - del edge and in label and connected points在这个路径下的文件夹A存放着很多个txt文件，每个txt文件都对应一个图像（所有图像的原尺寸都很大），txt文件中的内容为图像中某些点的位置信息，具体内容如下：
0 0.7611493652343754 0.8264149902343749
0 0.35108964843749996 0.15271127929687492
0 0.826904296875 0.6911179361979166
0 0.30214230143229165 0.3638953776041667
0 0.9516019531249997 0.3564654
0 0.94364716796875 0.456468132
0 0.94364716796875 0.8974563415
0 0.94364716796875 0.65873546567
（其中第一个数代表类别标签索引，第二三个数代表点在图像中的位置信息x和y。这些xy的信息再乘以1024才是真正在图片中的位置）
我想使用smote算法，对这些点进行扩充。请写出代码。



"""


import random

import os

def generate_synthetic_point(p1, p2, alpha):
    x_new = p1[0] + alpha * (p2[0] - p1[0])
    y_new = p1[1] + alpha * (p2[1] - p1[1])
    return (x_new, y_new)

def smote_oversample(points, num_samples=5, alpha=0.5):
    synthetic_points = []
    for _ in range(num_samples):
        p1 = random.choice(points)
        p2 = random.choice(points)
        synthetic_point = generate_synthetic_point(p1, p2, alpha)
        synthetic_points.append(synthetic_point)
    return synthetic_points

input_folder = r"D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\linshi_center txt++9 smote"
output_folder = r"D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\linshi_center txt++9 smote"  # Change this to your desired output folder

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        with open(input_path, 'r') as f:
            lines = f.readlines()

        # Check if the file is empty, skip processing if it is
        if len(lines) == 0:
            continue

        points = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 3:
                x = float(parts[1]) * 1024
                y = float(parts[2]) * 1024
                points.append((x, y))

        synthetic_points = smote_oversample(points, num_samples=5, alpha=0.5)

        with open(output_path, 'w') as f:
            for point in points:
                f.write(f"0 {point[0] / 1024} {point[1] / 1024}\n")
            for synthetic_point in synthetic_points:
                f.write(f"0 {synthetic_point[0] / 1024} {synthetic_point[1] / 1024}\n")

print("SMOTE-based oversampling complete.")
