# D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\center txt ++9在这个路径下的文件夹A存放着很多个txt文件，每个txt文件都对应一个图像，txt文件中的内容为图像中某些点的位置信息，具体内容如下：
# 0 0.7611493652343754 0.8264149902343749
# 0 0.35108964843749996 0.15271127929687492
# 0 0.826904296875 0.6911179361979166
# 0 0.30214230143229165 0.3638953776041667
# 0 0.9516019531249997 1.0
# 0 0.94364716796875 1.0
# 0 0.94364716796875 1.0
# 0 0.94364716796875 1.0
# （其中第一个数代表类别标签索引，第二三个数代表点在图像中的位置信息x和y）
# 请写一段python代码，将非常靠近图像边缘的点删除，即xy值非常靠近1的0.99-1的都删除
import os
input_folder = r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\1.center txt ++9'
output_folder = r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\1.center txt ++9'

# Threshold for considering points near the image edge
EDGE_THRESHOLD = 0.003  # Adjust as needed

def point_near_edge(x, y):
    return x < EDGE_THRESHOLD or y < EDGE_THRESHOLD or x > 1 - EDGE_THRESHOLD or y > 1 - EDGE_THRESHOLD

def filter_points(file_path):
    filtered_points = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split()
            label_index, x, y = int(parts[0]), float(parts[1]), float(parts[2])
            if not point_near_edge(x, y):
                filtered_points.append(line)
    return filtered_points

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for file_name in os.listdir(input_folder):
    input_file_path = os.path.join(input_folder, file_name)
    output_file_path = os.path.join(output_folder, file_name)

    filtered_lines = filter_points(input_file_path)

    with open(output_file_path, 'w') as output_file:
        for line in filtered_lines:
            output_file.write(line)
