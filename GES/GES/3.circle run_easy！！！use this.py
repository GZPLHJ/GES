"""
算法概述：
1.首先判断聚类中心点是否处于任何一个目标框内
2.如果处于则执行A，不处于则执行B。
    A：
    进行while循环（直到不在目标框内为止）
    1)找到离聚类中心点最近的3个目标框，
    2)计算聚类中心带你到最近的3个目标框的距离
    3)以聚类中心为原点从上下左右，左上左下，右上右下八个方位分别移动，并计算每个方位到这3个目标框距离的大小取最大值。
    4）将距离最大的方向作为聚类中心点的移动方向，以此方向更新聚类中心点的位置。
    循环终止条件：
    1)跳出目标框外
    2）无论任何方向逃逸最终会以绕圈的行径无限循环于所处的特定区域时，超过10循环则终止逃逸，并在 delete in label points代码中舍弃此点。
    特殊点的处理：
    1）存在逃逸到图像边缘位置的点，这类点不适用于进行数据增强-----删除。于delete edge points.py中删除
    2）图像中存在连着的点，像素10距离内相连的点插入图片后会导致遮挡-----删除。于delete connected points.py中删除
    B：
    不处于目标框内则此类点为优质点。既处于集群建筑物的中心位置还不会与其他建筑物重叠导致重采样。
！！！！注意：还存在一些离目标框很近的一些点，这些点用于提供特殊的带有遮挡的案例。但是为了避免重采样！要设置阈值。
关于连接点和遮挡点的要求如下：
仍然存在处于目标框边界周围（用于加入遮挡案例）（在插入图片时，要记得遮挡的阈值在0.4或者更小。
由于我是之后插入的受损建筑的图像，所以受损建筑图像的采样是不受影响的，这个遮挡阈值应该是受损建筑与非受损建筑的相交面积比非受损建筑的面积。）
其次还存在连着的点的情况，点的半径是5个像素，像素半径在10范围内相连的点删除


记录一下代码中的bug：
1.在判断是否处于目标框之内的时候，必须严格的判断，不能加阈值。首先你在判断的x_min和x_max等加阈值的时候算到面积就差的很大了。如果说本身就面积大的目标你加了阈值最后的影响是非常大的。
会导致本来不在目标框内的目标被算进去，然后偏移后不仅没有往好的地方偏移还往目标框里偏移了。
2.其次就是在判断是否处于目标框的if语句那段。我们对于original position的定义必须在判断之前定义，并且在
                    else:
                        original_position = (float(parts[1]) * image_size[0], float(parts[2]) * image_size[1])
                        updated_position = original_position
                        updated_positions.append((parts[0], updated_position[0] / image_size[0], updated_position[1] / image_size[1]))
                        这段的关于未处于目标框内的点的位置的更新不能在这块又去定义这个original_position然后再更新到updated_position然后再使用这个。这样的话就重复定义了，就导致很乱。具体定义出现了什么问题需要debug才知道，
                        不过反正不能这么用。
                        具体什么原因之后debug看看！！！！！！！！！！！！！！！！
                        记住：对于if-else语句统一要用到的变量要在，使用此语句之前就定义好了。
                        然后这个逻辑千万要搞清楚。出一点错就全拉倒了。
不然会导致：即使他不是目标框内，而且也



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

        if x_min < centry_x < x_max and y_min < centry_y < y_max :
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

        if x_min < centry_x < x_max and y_min < centry_y < y_max:
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

def update_position_correct_direction(original_position, target_positions, image_size,nearest_boxes):

    best_distance_sum = float('inf')
    best_updated_position = None
    o=10
    for dx, dy in [(0, -o), (0, o), (-o, 0), (o, 0), (-o, -o), (-o, o), (o, -o), (o, o)]:
        updated_position = (original_position[0] + dx, original_position[1] + dy)
        distance_sum = sum(distance(updated_position, target_position) for target_position in nearest_boxes)

        if distance_sum < best_distance_sum:
            best_distance_sum = distance_sum
            best_updated_position = updated_position

    return best_updated_position



def find_nearest_boxes(target_boxes, original_position, num_boxes):
    sorted_boxes = sorted(target_boxes, key=lambda box: distance((box[1], box[2]), original_position))
    return sorted_boxes[:num_boxes]

def find_largest_box(boxes):
    largest_box = max(boxes, key=lambda box: box[2] * box[3])
    return largest_box[2], largest_box[3]


input_folder = r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\linshi_center txt++9 smote_circle_run'     #center的txt
#center txt

label_folder = r'D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\labels\train'   #label的txt
#label txt

output_folder = r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\marked_smote_circle_run'  # Change this to the desired output folder path

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

                    parts = line.strip().split()
                    original_position = (float(parts[1]) * image_size[0], float(parts[2]) * image_size[1])
                    #如果中心位置在目标框内
                    if is_inside_object(line, label_lines):
                        # 1.直接开始围绕圆圈跳点
                        label_lines_lists = [[float(value) for value in line.split()] for line in label_lines]
                        target_boxes = [(item[1] * 1024, item[2] * 1024, item[3] * 1024, item[4] * 1024) for item in
                                        label_lines_lists]  # box的信息
                        # 2.记录标签中的目标框信息

                        updated_position = update_position_random(original_position, target_positions, image_size)  # 先跳一次
                        a=0
                        while(is_inside_object_inputnochanged(updated_position,label_lines)):
                            nearest_boxes = find_nearest_boxes(target_boxes, original_position, num_boxes=3)
                            # max_dir = find_direction(nearest_boxes,updated_position)
                            # updated_position = update_position_correct_direction(original_position, target_positions,image_size,max_dir)  # 如果还在框内则进入循环再跳
                            updated_position = update_position_correct_direction(updated_position,target_positions,image_size,nearest_boxes=nearest_boxes)
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
                            a+=1
                            if a>10:
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
                        updated_positions.append((parts[0], original_position[0] / image_size[0], original_position[1] / image_size[1]))
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


