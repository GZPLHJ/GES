"""

D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\center txt ++9 - del edge and in label and connected points在这个路径下的文件夹A存放着很多个txt文件，每个txt文件都对应一个图像（所有图像的原尺寸都很大），txt文件中的内容为图像中某些点的位置信息，具体内容如下：
0 0.7611493652343754 0.8264149902343749
0 0.35108964843749996 0.15271127929687492
0 0.826904296875 0.6911179361979166
0 0.30214230143229165 0.3638953776041667
0 0.9516019531249997 1.0
0 0.94364716796875 1.0
0 0.94364716796875 1.0
0 0.94364716796875 1.0
（其中第一个数代表类别标签索引，第二三个数代表点在图像中的位置信息x和y。像素位置x和y是具体的像素位置再除以图片尺寸后的结果，比如x和y假如是50和100.则对应的txt文件中xy的值是：50/1024和100/1024.）
但是这些点存在这距离很近的情况，即两个点挨得很近。我想删除这些像素距离在10个像素距离大小的点。请写出完整的python代码
请注意10是像素距离。

"""
import os
import math


def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


# def filter_close_points(points, min_distance):
#     filtered_points = []
#     for i, p1 in enumerate(points):
#         is_close = False
#         for j, p2 in enumerate(points):
#             if i != j and euclidean_distance(p1[1:], p2[1:]) < min_distance:
#                 is_close = True
#                 break
#         if not is_close:
#             filtered_points.append(p1)
#     return filtered_points

def filter_close_points(points, min_distance):
    filtered_points = []
    marked_for_removal = set()

    for i, p1 in enumerate(points):
        if i not in marked_for_removal:
            for j, p2 in enumerate(points):
                if i != j and euclidean_distance(p1[1:], p2[1:]) < min_distance:
                    marked_for_removal.add(j)

            filtered_points.append(p1)

    return filtered_points



input_folder = r"D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\1.center txt ++9"
output_folder = r"D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\1.center txt ++9" # Change this to your desired output folder
min_distance = 10  # Minimum distance in pixels

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        with open(input_path, 'r') as f:
            lines = f.readlines()

        points = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 3:
                class_index = int(parts[0])
                x = float(parts[1]) * 1024
                y = float(parts[2]) * 1024
                points.append((class_index, x, y))

        filtered_points = filter_close_points(points, min_distance)

        with open(output_path, 'w') as f:
            for point in filtered_points:
                f.write(f"{point[0]} {point[1] / 1024} {point[2] / 1024}\n")

print("Processing complete.")
