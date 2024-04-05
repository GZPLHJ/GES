"""

D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\center txt ++9 - del edge and in label and connected points在这个路径下的文件夹A存放着很多个txt文件，每个txt文件都对应一个图像（所有图像的原尺寸都很大），txt文件中的内容为图像中某些点的位置信息，具体内容如下：
0 0.7611493652343754 0.8264149902343749
0 0.35108964843749996 0.15271127929687492
0 0.826904296875 0.6911179361979166
0 0.30214230143229165 0.3638953776041667
（其中第一个数代表类别标签索引，这个类别标签不需要，我们只用后两个点。第二三个数代表点在图像中的位置信息x和y。像素位置x和y是具体的像素位置再除以图片尺寸后的结果，比如x和y假如是50和100.则对应的txt文件中xy的值是：50/1024和100/1024.）
另外这些txt文件所对应的图像都保存于文件夹：image_folder = "D:/GuoZhoupeng/datasets/xfbd_yolo/train/images"另外，每张图片中目标标签均存放于一个txt文件中，这些标签的格式都是yolo格式。这些txt文件均保存到的文件夹B：label_folder = "D:/GuoZhoupeng/datasets/xfbd_yolo/train/labels"的地方，另外图片原尺寸为1024*1024。
装有标签的txt文件的内容示例如下：
0 0.7611493652343754 0.8264149902343749 0.30214230143229165 0.3638953776041667
0 0.35108964843749996 0.15271127929687492 0.826904296875 0.6911179361979166
其中第一个数字代表了类别标签，第二三个数代表了这个目标的中心点的位置信息（分别是x值和y值），第三四个数代表了这个目标框的宽和高。

请以以上信息为基础帮我写一个代码，要求如下：
设s2=16倍根号2
s1=16

s3=48倍根号2
文件夹A中的txt文件保存着图像中许多的点的位置，文件夹B中的txt文件保存着图像中许多目标的信息。请对于每张图像中的每个点进行判断：
1.判断以此点为圆点以s1为半径的圆是否与图片内的任何目标框有相交，如果有则删除此点的信息。
2.如果第一个判断为没有相交，则再以此点为圆点以s2为半径的圆是否与图片内的任何目标框有相交，如果有则判断此点为小目标点，将文件夹A中的文件对应的此点的信息的第一个元素0改为s。
3.如果第一个第二个判断都为没有相交，则再以此点为圆点以s3为半径的圆是否与图片内的任何目标框有相交，如果有则判断此点为中目标点，将文件夹A中的文件对应的此点的信息的第一个元素0改为m。
4.如果第一个第二个第三个判断都为没有相交，则将文件夹A中的文件对应的此点的信息的第一个元素0改为l。

"""
# import os
# import math
#
# # Define constants
# s1 = 16
# s2 = 16 * math.sqrt(2)
# s3 = 48 * math.sqrt(2)
# image_folder = r"D:\GuoZhoupeng\datasets\xfbd_yolo\train\images"
# label_folder = r"D:\GuoZhoupeng\datasets\xfbd_yolo\train\labels"
#
#
# # Function to check if two circles intersect
# def circles_intersect(x1, y1, r1, x2, y2, r2):
#     distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
#     return distance < r1 + r2
#
#
# # Iterate through each txt file in folder A
# txt_files = os.listdir(
#     r"D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\s m l 4.center txt ++9 -smote-del in label points")
# for txt_file in txt_files:
#     txt_path = os.path.join(
#         r"D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\s m l 4.center txt ++9 -smote-del in label points",
#         txt_file)
#
#     # Read the points from the txt file
#     with open(txt_path, 'r') as f:
#         points = [line.strip().split() for line in f]
#         points = [(float(x), float(y)) for _, x, y in points]
#
#     # Load corresponding label file
#     label_file = os.path.splitext(txt_file)[0] + ".txt"
#     label_path = os.path.join(label_folder, label_file)
#
#     if not os.path.exists(label_path):
#         continue
#
#     with open(label_path, 'r') as f:
#         labels = [line.strip().split() for line in f]
#
#     # Process each point
#     for point in points:
#         x, y = point
#         label_changed = False
#
#         # Check for intersections with circles of different radii
#         for label in labels:
#             _, bbox_x, bbox_y, bbox_w, bbox_h = map(float, label)
#             bbox_cx = bbox_x + bbox_w / 2
#             bbox_cy = bbox_y + bbox_h / 2
#
#             if circles_intersect(x, y, s1, bbox_cx, bbox_cy, max(bbox_w, bbox_h) / 2):
#                 # Intersection with s1 circle, remove point
#                 points.remove(point)
#                 label_changed = True
#                 break
#             elif circles_intersect(x, y, s2, bbox_cx, bbox_cy, max(bbox_w, bbox_h) / 2):
#                 # Intersection with s2 circle, update label to small object
#                 label[0] = "s"
#                 label_changed = True
#                 break
#             elif circles_intersect(x, y, s3, bbox_cx, bbox_cy, max(bbox_w, bbox_h) / 2):
#                 # Intersection with s3 circle, update label to medium object
#                 label[0] = "m"
#                 label_changed = True
#                 break
#
#         if not label_changed:
#             # No intersections, update label to large object
#             label[0] = "l"
#
#     # Write the modified labels back to the file
#     with open(label_path, 'w') as f:
#         for label in labels:
#             f.write(' '.join(map(str, label)) + '\n')

"""
有一个名为circle的元组内容示例如这个(0.4426611979166671, 0.4183116048177084, 16)。这个circle元组为一个圆的位置信息，第一个数为x坐标，第二个数为y坐标，第三个数16再除以1024为圆的半径。有一个名为rect的元组内容示例如这个(0.9898390625, 0.9129980468750001, 1.0101609375, 0.9451091796875001)，第一个数为x坐标，第二个数为y坐标，第三个数为宽的信息，第四个数为高的信息
"""


"""
问题：
1.最终还是没有用circle_intersects_rect_easy来判断是否相交，而是用circle_intersects_rect。
circle_intersects_rect函数，首先判断这些个目标框的四个点是否处于圆圈内如果处于则相交。
其次，判断这些目标框的上下左右边与原点的距离，如果上下+左右任意两个边的这个线段到原点的距离小于半径则存在相交的情况（当这个目标框很大，矩形的某个边很大的时候，这个点又恰好在这个很大的边的中间时这种判断方法失效）
2.在实际的判定中，当这个point周围很空旷时并不能判定为Large而是判定为了small，也不知道为啥
3.在实际的判定中，就是存在一些明明挨着目标框的点但是就是被分为了middle而不是large
4.关于圆圈半径按理说应该是16往上，但是不知道是哪里的（概念上的问题？）问题，这个值得取很小效果才好。

"""


import os
import math

# Define constants
# s1 = 16
# s2 = 16 * math.sqrt(2)
# s3 = 48 * math.sqrt(2)
s1 = 1
s2 = 8
s3 = 12

# Function to check if a point lies within a rectangle
def find_nearest_boxes(target_boxes, original_position, num_boxes):
    sorted_boxes = sorted(target_boxes, key=lambda box: p_distance((box[1], box[2]), original_position))
    return sorted_boxes[:num_boxes]
def p_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


# Function to check if a circle intersects with a rectangle
# def circle_intersects_rect(circle, labels):
#     for label in labels:
#         class_idx, x1, y1, width, height = map(float, label.strip().split())
#         rect = (x1, y1, width, height)
#         sum = 0
#
#         circle_x, circle_y, circle_radius = circle
#         circle_o =(circle_x,circle_y)
#         rect_cx, rect_cy, rect_w, rect_h = rect
#         rect_x1 = rect_cx-rect_w/2#左边
#         rect_x2 = rect_cx+rect_w/2#右边
#         rect_y1 = rect_cy-rect_h/2#上边
#         rect_y2 = rect_cy+rect_h/2#下边
#         rect_x1_y1 =(rect_x1,rect_y1)
#         #左上角
#         rect_x2_y1 =(rect_x2,rect_y1)
#         #右上角
#         rect_x1_y2 =(rect_x1,rect_y2)
#         #左下角
#         rect_x2_y2 =(rect_x2,rect_y2)
#         #右下角
#         circle_radius = circle_radius/1024
#         co_to_linex1_y1_x2_y1 = abs(circle_y-rect_y1)
#         #到上边的距离
#
#         co_to_linex1_y2_x2_y2 = abs(circle_y-rect_y2)
#         #到下边的距离
#
#         co_to_linex1_y1_x1_y2 = abs(circle_x-rect_x1)
#         #到左边的距离
#
#         co_to_linex2_y1_x2_y2 = abs(circle_y-rect_x2)
#         #到右边的距离
#
#         top_left= co_to_linex1_y1_x2_y1<circle_radius and co_to_linex1_y1_x2_y1< circle_radius
#         #到上左边的距离均小于半径则一定相交
#
#         top_right= co_to_linex1_y1_x2_y1<circle_radius and co_to_linex2_y1_x2_y2<circle_radius
#         #到上右边的距离均小于半径则一定相交
#
#         bottom_left = co_to_linex1_y2_x2_y2<circle_radius and co_to_linex1_y1_x1_y2<circle_radius
#         #到下左边的距离均小于半径则一定相交
#
#         bottom_right = co_to_linex1_y2_x2_y2<circle_radius and co_to_linex2_y1_x2_y2<circle_radius
#         #到下右边的距离均小于半径则一定相交
#
#         if p_distance(circle_o,rect_x1_y1)<circle_radius or p_distance(circle_o,rect_x2_y1)<circle_radius or p_distance(circle_o,rect_x1_y2)<circle_radius or p_distance(circle_o,rect_x2_y2)<circle_radius :
#             sum +=1
#         elif top_right or top_left or bottom_left or bottom_right:
#             sum +=1
#     if sum>0:
#         #存在相交则返回True
#         return True
#     else:
#         #不存在相交则返回False
#         return False
#
#     # # Calculate the closest point on the rectangle to the circle center
#     # closest_x = max(rect_x1, min(circle_x, rect_x2))
#     # closest_y = max(rect_y1, min(circle_y, rect_y2))
#     #
#     # # Calculate the distance between the circle center and the closest point
#     # distance = math.sqrt((circle_x - closest_x) ** 2 + (circle_y - closest_y) ** 2)
#     #
#     # return distance < circle_radius


# Process each txt file in folder A

def circle_intersects_rect_easy(circle, labels,point):
    label_lines_lists = [[float(value) for value in line.split()] for line in labels]
    labels = [(item[1] , item[2] , item[3] , item[4] ) for item in
                    label_lines_lists]  # box的信息
    nearest_boxes = find_nearest_boxes(labels,point,num_boxes=3)
    sum = 0
    for box in nearest_boxes:
        x1, y1, width, height = box[0],box[1],box[2],box[3]
        rect = (x1, y1, width, height)
        circle_x, circle_y, circle_radius = circle
        circle_o =(circle_x,circle_y)
        rect_cx, rect_cy, rect_w, rect_h = rect
        rect_x1 = rect_cx-rect_w/2#左边
        rect_x2 = rect_cx+rect_w/2#右边
        rect_y1 = rect_cy-rect_h/2#上边
        rect_y2 = rect_cy+rect_h/2#下边
        rect_x1_y1 =(rect_x1,rect_y1)
        #左上角
        rect_x2_y1 =(rect_x2,rect_y1)
        #右上角
        rect_x1_y2 =(rect_x1,rect_y2)
        #左下角
        rect_x2_y2 =(rect_x2,rect_y2)
        #右下角
        circle_radius = circle_radius/1024
        co_to_linex1_y1_x2_y1 = abs(circle_y-rect_y1)
        #到上边的距离

        co_to_linex1_y2_x2_y2 = abs(circle_y-rect_y2)
        #到下边的距离

        co_to_linex1_y1_x1_y2 = abs(circle_x-rect_x1)
        #到左边的距离

        co_to_linex2_y1_x2_y2 = abs(circle_y-rect_x2)
        #到右边的距离


        if p_distance(circle_o,rect_x1_y1)<circle_radius or p_distance(circle_o,rect_x2_y1)<circle_radius or p_distance(circle_o,rect_x1_y2)<circle_radius or p_distance(circle_o,rect_x2_y2)<circle_radius :
            sum +=1
        elif co_to_linex1_y1_x2_y1<circle_radius or co_to_linex1_y2_x2_y2<circle_radius or co_to_linex1_y1_x1_y2<circle_radius or co_to_linex2_y1_x2_y2<circle_radius:
            sum +=1
    if sum>0:
        #存在相交则返回True
        return True
    else:
        #不存在相交则返回False
        return False




def circle_intersects_rect(circle, labels):
    sum = 0
    for label in labels:
        class_idx, x1, y1, width, height = map(float, label.strip().split())
        rect = (x1, y1, width, height)
        circle_x, circle_y, circle_radius = circle
        circle_o =(circle_x,circle_y)
        rect_cx, rect_cy, rect_w, rect_h = rect
        rect_x1 = rect_cx-rect_w/2#左边
        rect_x2 = rect_cx+rect_w/2#右边
        rect_y1 = rect_cy-rect_h/2#上边
        rect_y2 = rect_cy+rect_h/2#下边
        rect_x1_y1 =(rect_x1,rect_y1)
        #左上角
        rect_x2_y1 =(rect_x2,rect_y1)
        #右上角
        rect_x1_y2 =(rect_x1,rect_y2)
        #左下角
        rect_x2_y2 =(rect_x2,rect_y2)
        #右下角
        circle_radius = circle_radius/1024
        co_to_linex1_y1_x2_y1 = abs(circle_y-rect_y1)
        #到上边的距离

        co_to_linex1_y2_x2_y2 = abs(circle_y-rect_y2)
        #到下边的距离

        co_to_linex1_y1_x1_y2 = abs(circle_x-rect_x1)
        #到左边的距离

        co_to_linex2_y1_x2_y2 = abs(circle_x-rect_x2)
        #到右边的距离

        top_left= co_to_linex1_y1_x2_y1<circle_radius and co_to_linex1_y1_x2_y1< circle_radius
        #到上左边的距离均小于半径则一定相交

        top_right= co_to_linex1_y1_x2_y1<circle_radius and co_to_linex2_y1_x2_y2<circle_radius
        #到上右边的距离均小于半径则一定相交

        bottom_left = co_to_linex1_y2_x2_y2<circle_radius and co_to_linex1_y1_x1_y2<circle_radius
        #到下左边的距离均小于半径则一定相交

        bottom_right = co_to_linex1_y2_x2_y2<circle_radius and co_to_linex2_y1_x2_y2<circle_radius
        #到下右边的距离均小于半径则一定相交

        if p_distance(circle_o,rect_x1_y1)<circle_radius or p_distance(circle_o,rect_x2_y1)<circle_radius or p_distance(circle_o,rect_x1_y2)<circle_radius or p_distance(circle_o,rect_x2_y2)<circle_radius :
            sum +=1
        elif top_right or top_left or bottom_left or bottom_right:
            sum +=1
    if sum>0:
        #存在相交则返回True
        return True
    else:
        #不存在相交则返回False
        return False

    # # Calculate the closest point on the rectangle to the circle center
    # closest_x = max(rect_x1, min(circle_x, rect_x2))
    # closest_y = max(rect_y1, min(circle_y, rect_y2))
    #
    # # Calculate the distance between the circle center and the closest point
    # distance = math.sqrt((circle_x - closest_x) ** 2 + (circle_y - closest_y) ** 2)
    #
    # return distance < circle_radius

folder_a = r"D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\sml"
folder_b = r"D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\labels\train"

for filename in os.listdir(folder_a):
    if filename.endswith(".txt"):
        with open(os.path.join(folder_a, filename), 'r') as file:
            points = file.readlines()
        updated_points = []
        label_filename = os.path.join(folder_b, filename)
        if os.path.exists(label_filename):
            with open(label_filename, 'r') as label_file:
                labels = label_file.readlines()

            for point in points:
                _, x, y = map(float, point.strip().split())
                circle1 = (x, y, s1)
                circle2 = (x, y, s2)
                circle3 = (x, y, s3)
                point_position=(x,y)
                lm =True
                l=True
                # if circle_intersects_rect_easy(circle=circle1, labels=labels,point=point_position):
                #     delete_point = True
                #     #最小的16的圆有相交则删除此点，不将词典更新到新位置的列表
                #     #之后再判断对于16*1.412的圆是否相交
                # elif circle_intersects_rect_easy(circle=circle2,labels=labels,point=point_position):
                #     #与16的圆不相交，与16*1.412的圆相交则认定可以放小目标
                #     updated_point = 's' + point[1:]
                #     updated_points.append(updated_point)
                #     lm= False#这个是停止此循环的标志位，如果这个代码执行了，那么下一个判断结果就要依照此次执行的代码来决定是否执行
                # elif circle_intersects_rect_easy(circle=circle3, labels=labels,point=point_position) or lm:#只有42*1.412的圆与rect相交且lm标志位没有变仍未True时才执行以下代码
                #     updated_point = 'm' + point[1:]
                #     updated_points.append(updated_point)
                #     l = False
                #     #当执行了这些代码时l变成False防止再执行最后的代码。防止把m又变成了l
                #
                # elif l :
                #     #如果都没变上一个代码执行了那么l变为False就不执行下面这个代码了，但是如果上面那个没执行那么l仍旧是True则执行下面的代码
                #     updated_point = 'l' + point[1:]
                #     updated_points.append(updated_point)

                if circle_intersects_rect(circle=circle1, labels=labels):
                    delete_point = True
                    #最小的16的圆有相交则删除此点，不将词典更新到新位置的列表
                    #之后再判断对于16*1.412的圆是否相交
                elif circle_intersects_rect(circle=circle2,labels=labels):
                    #与16的圆不相交，与16*1.412的圆相交则认定可以放小目标
                    updated_point = 's' + point[1:]
                    updated_points.append(updated_point)
                    lm= False#这个是停止此循环的标志位，如果这个代码执行了，那么下一个判断结果就要依照此次执行的代码来决定是否执行
                elif circle_intersects_rect(circle=circle3, labels=labels) or lm:#只有42*1.412的圆与rect相交且lm标志位没有变仍未True时才执行以下代码
                    updated_point = 'm' + point[1:]
                    updated_points.append(updated_point)
                    l = False
                    #当执行了这些代码时l变成False防止再执行最后的代码。防止把m又变成了l

                elif l :
                    #如果都没变上一个代码执行了那么l变为False就不执行下面这个代码了，但是如果上面那个没执行那么l仍旧是True则执行下面的代码
                    updated_point = 'l' + point[1:]
                    updated_points.append(updated_point)

        # Write back the modified points to the file
        with open(os.path.join(folder_a, filename), 'w') as file:
            file.writelines(updated_points)

