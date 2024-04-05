# -*- coding: utf-8 -*-
"""
请写一段python代码，代码要求如下：
D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-kmeans+taoyi+smote+sml\train\labels
这个路径下存放着数据集训练集的图片对应的标签文件，每个标签文件都是一个txt文件，其中txt文件内容示例如下：
0 0.34666547851562496 0.042437353515625 0.04110732421875 0.03559736328125
0 0.338754248046875 0.027579541015625 0.04023505859375 0.03576455078125
0 0.32641884765625 0.016032568359375 0.0423576171875 0.03206513671875
1 0.4164822916666668 0.40687895507812505 0.0214453125 0.0254861328125
1 0.7611493652343754 0.762106884765625 0.02664892578125 0.0135359375
2 0.31573746892755683 0.06253630149147726 0.0213671875 0.027873046875
2 0.594691866048177 0.8851663859049479 0.02280322265625 0.0195384765625
2 0.8315712890625007 0.19815673828125002 0.0191724609375 0.02025908203125
其中第一个数为类别索引，其中类别0的目标为非受损建筑目标，类比为1和2的目标为受损建筑目标。第二个数和第三个数是这个目标的目标框的中心位置，第三个数和第四个数为此目标框的宽和高。
请逐个判断标签为1和2的受损建筑目标，判断每个受损建筑目标是否与图片内的任何一个非受损建筑目标（标签为0的目标）重叠。如果某个受损建筑目标A与某个非受损建筑目标B重叠。且受损建筑目标A与非受损建筑目标B相交的面积s1除以此非受损建筑目标B的面积S的值达到了0.5以上，则把此非受损建筑目标的标签删除。（记住不是求iou，iou是交并比，我这个只是单纯的除以非受损建筑目标B的面积）
把找到的此目标的标签信息从这个txt文件中删除掉。
"""
# import os
#
#
# def calculate_area(box):
#     return box[2] * box[3]
#
# def calculate_intersection_area(object1, object2):
#     x1, y1, w1, h1 = object1['box'][0]*1024,object1['box'][1]*1024,object1['box'][2]*1024,object1['box'][3]*1024
#     x2, y2, w2, h2 = object2['box'][0]*1024,object2['box'][1]*1024,object2['box'][2]*1024,object2['box'][3]*1024
#
#     x_overlap = max(0, min(x1 + w1 / 2, x2 + w2 / 2) - max(x1 - w1 / 2, x2 - w2 / 2))
#     y_overlap = max(0, min(y1 + h1 / 2, y2 + h2 / 2) - max(y1 - h1 / 2, y2 - h2 / 2))
#
#     return x_overlap * y_overlap
#
#
# def main():
#     label_dir = r'D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-kmeans+taoyi+smote+sml\train\labels'
#
#     for filename in os.listdir(label_dir):
#         if filename.endswith('.txt'):
#             with open(os.path.join(label_dir, filename), 'r') as file:
#                 lines = file.readlines()
#
#             damaged_objects = []
#             undamaged_objects = []
#
#             for line in lines:
#                 parts = line.strip().split()
#                 class_idx = int(parts[0])
#                 x_center = float(parts[1])
#                 y_center = float(parts[2])
#                 width = float(parts[3])
#                 height = float(parts[4])
#                 area = width * height*1024*1024
#
#                 if class_idx in [1, 2]:
#                     damaged_objects.append({
#                         'class_idx': class_idx,
#                         'box': [x_center, y_center, width, height],
#                         'area': area
#                     })
#                 elif class_idx == 0:
#                     undamaged_objects.append({
#                         'box': [x_center, y_center, width, height],
#                         'area': area
#                     })
#
#             objects_to_delete = set()
#
#             for damaged_object in damaged_objects:
#                 for undamaged_object in undamaged_objects:
#                     intersection_area = calculate_intersection_area(undamaged_object,damaged_object)
#                     overlap_ratio = intersection_area/undamaged_object['area']
#                     if overlap_ratio >= 0.5:
#                         objects_to_delete.add(tuple(undamaged_object['box']))  # Convert dict to tuple
#                 undamaged_objects = [obj for obj in undamaged_objects if obj['box'] not in objects_to_delete]
#
#             print(f"File: {filename}")
#             print("Objects to delete:", objects_to_delete)
#             print("\n")
#
#             # Now you can process the deletion of labels based on 'objects_to_delete' list
#
#
# if __name__ == "__main__":
#     main()
#
import os


def overlap_area(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    x_overlap = max(0, min(x1 + w1 / 2, x2 + w2 / 2) - max(x1 - w1 / 2, x2 - w2 / 2))
    y_overlap = max(0, min(y1 + h1 / 2, y2 + h2 / 2) - max(y1 - h1 / 2, y2 - h2 / 2))

    return x_overlap * y_overlap


# def main():
#     labels_dir = r"D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-kmeans+taoyi+smote+sml\train\labels"
#
#     for label_file in os.listdir(labels_dir):
#         label_file_path = os.path.join(labels_dir, label_file)
#         with open(label_file_path, "r") as f:
#             lines = f.readlines()
#
#         new_lines = []
#         for line in lines:
#             parts = line.split()
#             class_idx = int(parts[0])
#             x, y, w, h = map(float, parts[1:])
#             current_box = (x, y, w, h)
#
#             if class_idx in [1, 2]:
#                 delete_box = False
#                 for other_line in lines:
#                     other_parts = other_line.split()
#                     other_class_idx = int(other_parts[0])
#                     if other_class_idx == 0:
#                         other_x, other_y, other_w, other_h = map(float, other_parts[1:])
#                         other_box = (other_x, other_y, other_w, other_h)
#                         area_overlap = overlap_area(current_box, other_box)
#                         if area_overlap / (other_w * other_h) >= 0.5:
#                             delete_box = True
#                             break
#                 if not delete_box:
#                     new_lines.append(line)
#             else:
#                 new_lines.append(line)
#
#         with open(label_file_path, "w") as f:
#             f.writelines(new_lines)
#
#
# if __name__ == "__main__":
#     main()

def main():
    labels_dir = r"D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\linshi_final_dataset_delete_occ\train"

    for label_file in os.listdir(labels_dir):
        label_file_path = os.path.join(labels_dir, label_file)
        with open(label_file_path, "r") as f:
            lines = f.readlines()
        delete_lines = []
        new_lines = []
        for line in lines:
            parts = line.split()
            class_idx = int(parts[0])
            x, y, w, h = map(float, parts[1:])
            current_box = (x, y, w, h)

            if class_idx in [1, 2]:
                for other_line in lines:
                    other_parts = other_line.split()
                    other_class_idx = int(other_parts[0])
                    if other_class_idx == 0:
                        other_x, other_y, other_w, other_h = map(float, other_parts[1:])
                        other_box = (other_x, other_y, other_w, other_h)
                        area_overlap = overlap_area(current_box, other_box)
                        if area_overlap / (other_w * other_h) >= 0.5:
                            delete_lines.append(other_line)
        for line in lines:
            if line not in delete_lines:
                new_lines.append(line)
        with open(label_file_path, "w") as f:
            f.writelines(new_lines)


if __name__ == "__main__":
    main()