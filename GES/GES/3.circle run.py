"""
这个代码比较麻烦，就是更新位置的时候，意图首先通过计算与最近的三个boxes的距离来判断哪个方向是最好的方向。
之后朝着这个方向一直逃逸，直到跑出去为止，但是可能由于代码问题，while循环的时候陷入死循环。
有时间再检查改改吧
"""


import os
import math
import random

def point_on_box_edge(point, box):
    comback=2
    if point is None:
        print(point)
        return "NoneType"

    x, y = point
    x_min, y_min = box[0], box[1]
    x_max, y_max = x_min + box[2], y_min + box[3]

    if abs(x - x_min)<15 or abs(x - x_max)<15:
        return "Left or Right Edge"
    elif abs(y - y_min)<15 or abs(y - y_max)<15:
        return "Top or Bottom Edge"
    else:
        return "Not on Edge"


def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def symmetry_update_LR(updated_position,box):
    updated_position = list(updated_position)
    box = list(box)
    updated_position[0] = updated_position[0]+abs(box[0]-updated_position[0])
    if updated_position[0]>=1024 :
        updated_position[0]=1024
    elif updated_position[0]<=0 :
        updated_position[0]=0
    updated_position = tuple(updated_position)
    return updated_position
def symmetry_update_TB(updated_position,box):
    updated_position = list(updated_position)
    box = list(box)
    updated_position[1] = updated_position[1]+abs(box[1]-updated_position[1])
    if updated_position[1]>=1024 :
        updated_position[1]=1024
    elif updated_position[1]<=0 :
        updated_position[1]=0
    updated_position = tuple(updated_position)
    return updated_position
def is_inside_object(position, label_lines):
    add =0
    image_size =1024
    position = position.split()[1:]
    for object_position in label_lines:
        parts = object_position.split()[1:]
        object_position_list = [float(part) for part in parts]
        x_min, y_min = object_position_list[0]*image_size - 0.5 * object_position_list[2]*image_size, object_position_list[1]*image_size - 0.5 * object_position_list[3]*image_size
        x_max, y_max = object_position_list[0]*image_size + 0.5 * object_position_list[2]*image_size, object_position_list[1]*image_size + 0.5 * object_position_list[3]*image_size

        centry_x = float(position[0])*image_size
        centry_y = float(position[1])*image_size

        if x_min - 10 <= centry_x <= x_max + 10 and y_min - 10 <= centry_y <= y_max + 10:
            add += 1
    if add > 0:
        return True
    else:
        return False

def is_inside_object_inputnochanged(position, label_lines):
    image_size =1024
    add=0
    for object_position in label_lines:
        parts = object_position.split()[1:]
        object_position_list = [float(part) for part in parts]
        x_min, y_min = object_position_list[0]*image_size - 0.5 * object_position_list[2]*image_size, object_position_list[1]*image_size - 0.5 * object_position_list[3]*image_size
        x_max, y_max = object_position_list[0]*image_size + 0.5 * object_position_list[2]*image_size, object_position_list[1]*image_size + 0.5 * object_position_list[3]*image_size

        centry_x = float(position[0])
        centry_y = float(position[1])

        if x_min-5 <= centry_x <= x_max+5 and y_min-5 <= centry_y <= y_max+5:
            add+=1
    if add>0:
        return True
    else:
        return False
def update_position_random(original_position, target_positions, image_size):
    # 列表中的元素
    o=10
    direction = [(0, -o), (0, o), (-o, 0), (o, 0), (-o, -o), (-o, o), (o, -o), (o, o)]
    random_choice_direction = random.choice(direction)
    #列表中任选一个元素
    updated_position = (original_position[0] + random_choice_direction[0], original_position[1] + random_choice_direction[1])
    return updated_position

def update_position_correct_direction(original_position, target_positions, image_size,max_dir):
    o=10
    dir_1 = [0, -o]
    dir_2 = [o, o]
    dir_3 = [0, o]
    dir_4 = [-o, 0]
    dir_5 = [o, 0]
    dir_6 = [-o, -o]
    dir_7 = [-o, o]
    dir_8 = [o, -o]
    variable_mapping = {
        "dir1": dir_1,
        "dir2": dir_2,
        "dir3": dir_3,
        "dir4": dir_4,
        "dir5": dir_5,
        "dir6": dir_6,
        "dir7": dir_7,
        "dir8": dir_8,
    }
    if max_dir in variable_mapping:
        direction = variable_mapping[max_dir]
        updated_position = (original_position[0] + direction[0], original_position[1] + direction[1])
    return updated_position
    # best_distance_sum = float('inf')
    # best_updated_position = None
    # o=10
    # for dx, dy in [(0, -o), (0, o), (-o, 0), (o, 0), (-o, -o), (-o, o), (o, -o), (o, o)]:
    #     updated_position = (original_position[0] + dx, original_position[1] + dy)
    #     distance_sum = sum(distance(updated_position, target_position) for target_position in target_positions)
    #
    #     if distance_sum < best_distance_sum:
    #         best_distance_sum = distance_sum
    #         best_updated_position = updated_position
    #
    # return best_updated_position


def find_direction(nearest_boxes,updated_position):
    o=10
    direction_1 = [0, -o]
    direction_2 = [o, o]
    direction_3 = [0, o]
    direction_4 = [-o, 0]
    direction_5 = [o, 0]
    direction_6 = [-o, -o]
    direction_7 = [-o, o]
    direction_8 = [o, -o]
    updated_position = list(updated_position)
    updated_position_dir1=(updated_position[0] + direction_1[0], updated_position[1] + direction_1[1])
    updated_position_dir2=(updated_position[0] + direction_2[0], updated_position[1] + direction_2[1])
    updated_position_dir3=(updated_position[0] + direction_3[0], updated_position[1] + direction_3[1])
    updated_position_dir4=(updated_position[0] + direction_4[0], updated_position[1] + direction_4[1])
    updated_position_dir5=(updated_position[0] + direction_5[0], updated_position[1] + direction_5[1])
    updated_position_dir6=(updated_position[0] + direction_6[0], updated_position[1] + direction_6[1])
    updated_position_dir7=(updated_position[0] + direction_7[0], updated_position[1] + direction_7[1])
    updated_position_dir8=(updated_position[0] + direction_8[0], updated_position[1] + direction_8[1])

    distance_sum_dir1 = 0
    distance_sum_dir2 = 0
    distance_sum_dir3 = 0
    distance_sum_dir4 = 0
    distance_sum_dir5 = 0
    distance_sum_dir6 = 0
    distance_sum_dir7 = 0
    distance_sum_dir8 = 0

    for nearest_box in nearest_boxes:
        distances =distance(nearest_box,updated_position_dir1)
        distance_sum_dir1 += distances
    for nearest_box in nearest_boxes:
        distances =distance(nearest_box,updated_position_dir2)
        distance_sum_dir2 += distances
    for nearest_box in nearest_boxes:
        distances =distance(nearest_box,updated_position_dir3)
        distance_sum_dir3 += distances
    for nearest_box in nearest_boxes:
        distances =distance(nearest_box,updated_position_dir4)
        distance_sum_dir4 += distances
    for nearest_box in nearest_boxes:
        distances =distance(nearest_box,updated_position_dir5)
        distance_sum_dir5 += distances
    for nearest_box in nearest_boxes:
        distances =distance(nearest_box,updated_position_dir6)
        distance_sum_dir6 += distances
    for nearest_box in nearest_boxes:
        distances =distance(nearest_box,updated_position_dir7)
        distance_sum_dir7 += distances
    for nearest_box in nearest_boxes:
        distances =distance(nearest_box,updated_position_dir8)
        distance_sum_dir8 += distances

    distances = {
        "dir1": distance_sum_dir1,
        "dir2": distance_sum_dir2,
        "dir3": distance_sum_dir3,
        "dir4": distance_sum_dir4,
        "dir5": distance_sum_dir5,
        "dir6": distance_sum_dir6,
        "dir7": distance_sum_dir7,
        "dir8": distance_sum_dir8,
    }

    # 找到值最大的方向
    max_dir = max(distances, key=distances.get)
    return max_dir

def find_nearest_boxes(target_boxes, original_position, num_boxes):
    sorted_boxes = sorted(target_boxes, key=lambda box: distance((box[1], box[2]), original_position))
    return sorted_boxes[:num_boxes]

def find_largest_box(boxes):
    largest_box = max(boxes, key=lambda box: box[2] * box[3])
    return largest_box[2], largest_box[3]


input_folder = r'E:\xfbd_clusters_n-bi3\3.clusters_have_run - del_edge_connect'     #center的txt
#center txt

label_folder = r'D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\labels\train'   #label的txt
#label txt

output_folder = r'D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\center txt ++'  # Change this to the desired output folder path

image_size = (1024, 1024)  # Image size in pixels

if not os.path.exists(output_folder):
    os.makedirs(output_folder)


for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):
        input_path = os.path.join(input_folder, filename)
        label_path = os.path.join(label_folder, filename.replace('.txt', '.txt'))

        with open(input_path, 'r') as input_file, open(label_path, 'r') as label_file:
            input_lines = input_file.readlines()# list element-str '0 0.3294917887369792 0.40110337727864587'

            label_lines = [line.strip() for line in label_file.readlines() if line.strip()]# list element-str '0 0.9898390625 0.9129980468750001 0.020321875 0.0321111328125'

            target_positions = [(float(parts[1]) * image_size[0], float(parts[2]) * image_size[1]) for parts in
                                [line.split() for line in label_lines]]# list element-tuple (1013.5952, 934.9100000000001)

            updated_positions = []  # Initialize updated_positions for this input file

            for line in input_lines:

                    #如果中心位置在目标框内
                    if is_inside_object(line, label_lines):
                        parts = line.strip().split()
                        original_position = (float(parts[1]) * image_size[0], float(parts[2]) * image_size[1])
                        # 1.直接开始围绕圆圈跳点


                        label_lines_lists = [[float(value) for value in line.split()] for line in label_lines]
                        target_boxes = [(item[1] * 1024, item[2] * 1024, item[3] * 1024, item[4] * 1024) for item in
                                        label_lines_lists]  # box的信息
                        # 2.记录标签中的目标框信息

                        updated_position = update_position_random(original_position, target_positions, image_size)  # 先跳一次
                        a = 0
                        while(is_inside_object_inputnochanged(updated_position,label_lines)):
                            nearest_boxes = find_nearest_boxes(target_boxes, original_position, num_boxes=2)
                            max_dir = find_direction(nearest_boxes,updated_position)
                            updated_position = update_position_correct_direction(original_position, target_positions,image_size,max_dir)  # 如果还在框内则进入循环再跳
                            #3.将跳圈后的位置与所有box开始匹配，如果跳到边界了则对称跳（继续跳点）
                            for box in target_boxes:

                                edge_status = point_on_box_edge(updated_position, box)
                                if edge_status == "Not on Edge":
                                    continue
                                elif edge_status =="Left or Right Edge":
                                    updated_position = symmetry_update_LR(updated_position,box)
                                elif edge_status =="Top or Bottom Edge":
                                    updated_position = symmetry_update_TB(updated_position, box)
                            print("1")
                            a += 1
                            if a > 50:
                                break
                            # parts = line.strip().split()
                            # original_position = (float(parts[1]) * image_size[0], float(parts[2]) * image_size[1])
                            #
                            # best_updated_position = original_position
                            #
                            # label_lines_lists = [[float(value) for value in line.split()] for line in label_lines]
                            # target_boxes = [(item[1] * 1024, item[2] * 1024, item[3] * 1024, item[4] * 1024) for item in label_lines_lists]
                            # nearest_boxes = find_nearest_boxes(target_boxes, original_position, num_boxes=3)
                            # largest_width, largest_height = find_largest_box(nearest_boxes)
                            # threshold_distance=max(largest_height,largest_width)#这个是中心点到周围最大目标的距离应该大于这个值
                            #
                            #
                            # for target_position in nearest_boxes:
                            #     if distance(original_position, target_position) <= threshold_distance:
                            #         updated_position = update_position(original_position, target_positions, image_size)
                            #         if 0 <= updated_position[0] <= image_size[0] and 0 <= updated_position[1] <= image_size[1]:
                            #             best_updated_position = updated_position
                            #             break

                        # #如果出现None的异常情况则保持原结果
                        # if updated_position == None:
                        #     updated_position =original_position

                        # #否则就使用更新后的，然后换回原比例
                        # else:
                            updated_positions.append(
                                (parts[0], updated_position[0] / image_size[0], updated_position[1] / image_size[1]))
                    #如果中心位置在中心框外
                    else:
                        original_position = (float(parts[1]) * image_size[0], float(parts[2]) * image_size[1])
                        updated_position = original_position
                        updated_positions.append((parts[0], updated_position[0] / image_size[0], updated_position[1] / image_size[1]))
                    print("*********************************************")
            output_path = os.path.join(output_folder, filename)
            with open(output_path, 'w') as output_file:
                for label, x, y in updated_positions:
                    output_file.write(f"{label} {x} {y}\n")

print("Position information updated and saved.")

#这段代码中的逻辑似乎会导致在一个循环中多次更新位置，可能会导致位置不断趋近目标位置但无法稳定下来的情况。这可能会导致位置在目标框内来回震荡而无法收敛。为了改进这种情况，可以尝试以下修改：
# 在代码的开头，为每个输入文件创建一个单独的 updated_positions 列表，用于保存每个输入文件的更新位置。
# 在循环处理每个输入文件时，将 updated_positions 初始化为空列表，并在内部循环中更新该列表，而不是外部循环。这样可以确保每个输入文件的位置更新是独立的。
# 在这个修改后的代码中，每个输入文件的位置更新都是独立的，不会相互影响。我们只保留了一个最佳的更新位置，以确保更新后的位置不再跳跃在目标框内。


