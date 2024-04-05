# -*- coding: utf-8 -*-

"""
请帮我写一段python代码，代码要求如下：
D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-kmeans+taoyi+smote+sml\train\images这个文件夹下存放着数据集训练集的图片（总共5287张图片），D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-kmeans+taoyi+smote+sml\train\labels这个文件夹A下存放着数据集训练集的标签，每个图片的标签信息都被写在对应名字的txt文件中，以yolo的格式保存，示例如下：
0 0.9898390625 0.9129980468750001 0.020321875 0.0321111328125
1 0.96171533203125 0.89996806640625 0.0362037109375 0.0366759765625
2 0.94364716796875 0.967108447265625 0.06553125 0.06375283203125
同时，在D:\GuoZhoupeng\xfbd-dataset2\augimages with full information 1and2 object images\labels这个文件夹B下存放着，训练集中个别图片名字所对应的额外的标签（总共1277个图片的标签）。
请遍历文件夹B中的标签文件（txt文件），并找到与A文件夹中的标签文件（txt文件）名字相同的，相对应的文件
B中的标签文件的内容示例如下：
2 0.826904296875 0.8467625976562504 0.0275099609375 0.025416796875
2 0.6795703124999999 0.29345520019531257 0.03947578125 0.03726123046875
其次，遍历B中的标签文件（txt文件）内的每一行，提取每一行的第二、三个数字，以第二三个数字（中间以空格空开）构造出新的名字N，并在D:\GuoZhoupeng\xfbd-dataset2\augimages with full information 1and2 object images\images文件夹中找到名字为N的图片，并将此图片以他名字的信息（第二三个数字）所代表的位置插入到此标签在D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-kmeans+taoyi+smote+sml\train\images这个文件夹下存放着数据集训练集的图片（总共5287张图片）中所对应的图片中。
其中，第二个数字代表x坐标，第三个数字代表y坐标，在图片中具体的坐标位置是（x*1024，y*1024）（1024为图片原尺寸）
最后，将B中标签文件的内容也都插入到A中对应标签文件（txt文件）当中去。
请写出完整的代码

"""
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import os
import cv2
from PIL import Image
def parse_label_line(line):
    values = line.split()
    x = float(values[1])
    y = float(values[2])
    return x, y

# def main():
#     folder_A = r'D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-kmeans+taoyi+smote+sml\train\labels'
#     images_folder_A =r'D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-kmeans+taoyi+smote+sml\train\images'
#     folder_B = r'D:\GuoZhoupeng\xfbd-dataset2\augimages with full information 1and2 object images\labels'
#     images_folder_B = r'D:\GuoZhoupeng\xfbd-dataset2\augimages with full information 1and2 object images\images'
#
#     # Step 1: Iterate over label files in folder B
#     for label_file_B in os.listdir(folder_B):
#         if label_file_B.endswith(".txt"):
#             label_path_B = os.path.join(folder_B, label_file_B)
#
#             # Extract x and y coordinates from each line in label file B
#             with open(label_path_B, 'r') as f:
#                 for line in f:
#                     x, y = parse_label_line(line)
#                     new_name = f"{x} {y}.png"
#                     image_path_B = os.path.join(images_folder_B, new_name)
#
#                     # Step 2: Search for corresponding image in folder A
#                     for label_file_A in os.listdir(folder_A):
#                         if label_file_A.endswith(".txt"):
#                             label_path_A = os.path.join(folder_A, label_file_A)
#
#                             # Find the corresponding label file in folder A
#                             if os.path.splitext(label_file_A)[0] == os.path.splitext(label_file_B)[0]:
#                                 # Step 3: Insert image information into label file A
#                                 with open(label_path_A, 'a') as label_file_A:
#                                     label_file_A.write(line)
#                 image_path_A = os.path.join(images_folder_A, label_file_A.replace('.txt', '.png'))
#                 position = (int(x * 1024), int(y * 1024))
#                 image_A = Image.open(image_path_A)
#                 image_B = Image.open(image_path_B)
#                 image_A.paste(image_B, position)
#             image_A.save(images_folder_A)
# if __name__ == "__main__":
#     main()

#
# def main():
#     folder_A = r'D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-kmeans+taoyi+smote+sml\train\labels'
#     images_folder_A =r'D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-kmeans+taoyi+smote+sml\train\images'
#     folder_B = r'D:\GuoZhoupeng\xfbd-dataset2\full information 1and2 object images\labels'
#     images_folder_B = r'D:\GuoZhoupeng\xfbd-dataset2\full information 1and2 object images\images'
#
#     # Step 1: Iterate over label files in folder B
#     for label_file_B in os.listdir(folder_B):
#         if label_file_B.endswith(".txt"):
#             label_path_B = os.path.join(folder_B, label_file_B)
#
#             # Step 2: Search for corresponding image in folder A
#             for label_file_A in os.listdir(folder_A):
#                 if os.path.splitext(label_file_A)[0] == os.path.splitext(label_file_B)[0]:
#                     label_path_A = os.path.join(folder_A, label_file_A)
#             # train中对应的图片的路径也找到
#             image_path_A = os.path.join(images_folder_A, label_file_A.replace('.txt', '.png'))
#
#             image_A = Image.open(image_path_A)
#
#             # Extract x and y coordinates from each line in label file B
#             with open(label_path_B, 'r') as f:
#                 for line in f:
#                     # 粘贴图片
#                     values = line.split()
#                     x, y = parse_label_line(line)
#                     w, h = float(values[3]) * 1024, float(values[4]) * 1024
#                     new_name = f"{x} {y}.png"
#                     image_path_B = os.path.join(images_folder_B, new_name)
#                     position = (int((x * 1024) - w / 2), int((y * 1024) - h / 2))
#                     image_B = Image.open(image_path_B)
#
#
#                     image_A.paste(image_B, position)
#                     # 将每行line的信息插入
#
#                     # Step 3: Insert image information into label file A
#                     with open(label_path_A, 'a') as label_file_A:
#                         label_file_A.write(line)
#
#             # 保存图片
#             image_A.save(image_path_A)
#
#
# if __name__ == "__main__":
#     main()


def main():
    folder_A = r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\linshi_final_dataset\labels\train'
    images_folder_A =r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\linshi_final_dataset\images\train'
    folder_B = r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\linshi_full_information\labels'
    images_folder_B = r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\linshi_full_information\images'

    # Step 1: Iterate over label files in folder B
    for label_file_B in os.listdir(folder_B):
        if label_file_B.endswith(".txt"):
            label_path_B = os.path.join(folder_B, label_file_B)

            # Step 2: Search for corresponding image in folder A
            for label_file_A in os.listdir(folder_A):
                if os.path.splitext(label_file_A)[0] == os.path.splitext(label_file_B)[0]:
                    label_path_A = os.path.join(folder_A, label_file_A)
                    break
            #train中对应的图片的路径也找到
            image_path_A = os.path.join(images_folder_A, label_file_A.replace('.txt', '.png'))
            image_A = cv2.imread(image_path_A)

            # Extract x and y coordinates from each line in label file B
            with open(label_path_B, 'r') as f:
                for line in f:
                    #粘贴图片
                    values = line.split()
                    x, y = parse_label_line(line)
                    w, h = float(values[3])*1024,float(values[4])*1024
                    new_name = f"{x} {y}.png"
                    image_path_B = os.path.join(images_folder_B, new_name)
                    position = (int((x * 1024)-w/2), int((y * 1024)-h/2))

                    if (position[0] >= 0 and position[0] + int(w) <= image_A.shape[1] and
                            position[1] >= 0 and position[1] + int(h) <= image_A.shape[0]):
                        # Load image B using OpenCV
                        image_B = cv2.imread(image_path_B)
                        image_B = cv2.resize(image_B, (int(w), int(h)))
                        # Paste image B onto image A
                        image_A[position[1]:position[1] + image_B.shape[0],
                        position[0]:position[0] + image_B.shape[1]] = image_B
                        # #将每行line的信息插入

                        # Step 3: Insert image information into label file A
                        with open(label_path_A, 'a') as label_file_A:
                            label_file_A.write(line)
            #保存图片
            cv2.imwrite(image_path_A, image_A)
if __name__ == "__main__":
    main()




# def main():
#     label_path_A = r"D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-kmeans+taoyi+smote+sml\train\labels"  # 修改为实际路径
#     label_path_B = r"D:\GuoZhoupeng\xfbd-dataset2\augimages with full information 1and2 object images\labels"  # 修改为实际路径
#     images_folder_B = r"D:\GuoZhoupeng\xfbd-dataset2\augimages with full information 1and2 object images\images"  # 修改为实际路径
#
#     with open(label_path_A, 'r') as f:
#         # Load image A using OpenCV
#         image_A = cv2.imread("path_to_image_A.png")  # 修改为实际路径
#
#     with open(label_path_B, 'r') as f:
#         for line in f:
#             values = line.split()
#             x, y = parse_label_line(line)
#             w, h = float(values[3]) * 1024, float(values[4]) * 1024
#             new_name = f"{x} {y}.png"
#             image_path_B = os.path.join(images_folder_B, new_name)
#             position = (int((x * 1024) - w / 2), int((y * 1024) - h / 2))
#
#             if (position[0] >= 0 and position[0] + int(w) <= image_A.shape[1] and
#                     position[1] >= 0 and position[1] + int(h) <= image_A.shape[0]):
#                 # Load image B using OpenCV
#                 image_B = cv2.imread(image_path_B)
#                 image_B = cv2.resize(image_B, (int(w), int(h)))
#
#                 # Paste image B onto image A
#                 image_A[position[1]:position[1] + image_B.shape[0],
#                         position[0]:position[0] + image_B.shape[1]] = image_B
#
#                 # Insert image information into label file A
#                 with open(label_path_A, 'a') as label_file_A:
#                     label_file_A.write(line)
#
# if __name__ == "__main__":
#     main()