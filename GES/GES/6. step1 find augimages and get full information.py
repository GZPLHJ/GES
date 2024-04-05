
"""
请帮我写一段关于目标检测任务的python代码，代码前提如下：
D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\s m l 4.center txt ++9 -smote-del in label points这个路径下的文件夹A中存放着很多txt文件
每个txt文件对应一个数据集中的图像，每个txt文件中的内容示例如下：
s 0.4164822916666668 0.40687895507812505
m 0.7611493652343754 0.762106884765625
l 0.31573746892755683 0.06253630149147726
其中，第二三个数代表图像中一个点的位置，第二个数代表x坐标，第三个数代表y坐标。第一个字符代表这个点处我可以插入小目标、中目标还是大目标。如果是s则可以插入小目标，如果是m则可以插入中目标，如果是l则可以插入大目标。

另外，我们保存了很多标签索引为1和2的目标的非数据集的目标图片，用于数据增强。每张目标图片的有一个信息并且保存于一个txt文件中，txt文件的内容示例如下：
2 0.0192708984375 0.0196765625
第一个数字2代表着标签索引，第二三个数字代表着这个目标的宽width和高hight。
其中，目标中的小目标的图片保存于：D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\small
其中，目标中的小目标的标签均保存于：D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\small
其中，目标中的中目标的图片保存于：D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\middle
其中，目标中的中目标的标签均保存于：D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\middle
其中，目标中的大目标的图片保存于：D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\large
其中，目标中的大目标的标签均保存于：D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\large

我们的代码的要求如下：
请根据文件夹A中的txt文件保存的每个图像中点的位置信息以及可以放置的大中小的目标的信息构造出新的标签并将对应的图片保存到新的文件夹
文件夹A中每个txt文件包含多行信息。另外，所对应生成的新的标签文件应该一一对应文件夹A中每个txt文件，而且每个生成的新的txt文件中的标签的行数也与文件A中的txt文件相对应。
具体过程如下：
D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\s m l 4.center txt ++9 -smote-del in label points这个路径文件夹A下存在一个txt文件P，这个文件的内容如下：
s 0.4164822916666668 0.40687895507812505
m 0.7611493652343754 0.762106884765625
l 0.31573746892755683 0.06253630149147726
先看第一行：第一行的第一个字符为s，则从D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\small文件夹中任意找一个图片
则对应的此图片对应的标签信息存放于：D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\small的对应名字的txt文件中
此txt文件的内容为：2 0.0192708984375 0.0196765625
将此图片复制到，D:\GuoZhoupeng\xfbd-dataset2\full information 1and2 object images\images这个文件夹下，并以此图片所对应标签信息的后两个数字为为名字重新命名，比如这里就是0.0192708984375 0.0196765625。
并且将此图片的对应的标签信息以这样的形式保存：2 0.4164822916666668 0.40687895507812505 0.0192708984375 0.0196765625
其中，第一个数是标签索引是啥，第二个和第三个分别是x和y坐标，第四个和第五个分别是宽width和高height
将这些标签信息写入与P同名的txt文件当中
再看第二三行：第一个字符分别是m和l则对应从D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\middle和D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\large寻找图像，之后执行相同的工作。
依次将文件P中每一行的标签信息更新，并统一保存到一个新的txt文件中，然后这些txt文件都存放于D:\GuoZhoupeng\xfbd-dataset2\full information 1and2 object images\labels的文件夹下。
请写出完整的代码

"""

# import os
# import shutil
# import random
#
# # Paths
# input_txt_folder = r'D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\s m l 4.center txt ++9 -smote-del in label points'
# output_image_folder = r'D:\GuoZhoupeng\xfbd-dataset2\full information 1and2 object images\images'
# output_label_folder = r'D:\GuoZhoupeng\xfbd-dataset2\full information 1and2 object images\labels'
# image_folders = {
#     's': r'D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\small',
#     'm': r'D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\middle',
#     'l': r'D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\large'
# }
# label_folders = {
#     's': r'D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\small',
#     'm': r'D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\middle',
#     'l': r'D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\large',
#     '0':r'D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\small'
# }
#
# # Create output directories if they don't exist
# os.makedirs(output_image_folder, exist_ok=True)
# os.makedirs(output_label_folder, exist_ok=True)
#
# # Process each txt file in the input folder
# for txt_file_name in os.listdir(input_txt_folder):
#
#     txt_file_path = os.path.join(input_txt_folder, txt_file_name)
#
#     # Check if the file is empty
#     if os.path.getsize(txt_file_path) == 0:
#         print(f"Skipping empty file: {txt_file_name}")
#         continue
#     else:
#         print(f"opt file: {txt_file_name}")
#         with open(txt_file_path, 'r') as txt_file:
#             lines = txt_file.readlines()
#
#         new_labels = []
#
#         for line in lines:
#             parts = line.split()
#             label = parts[0]
#             x = float(parts[1])
#             y = float(parts[2])
#
#             image_folder = image_folders[label]
#             image_files = os.listdir(image_folder)
#             n=len(image_files)
#             random_number = random.randint(0, n-1)
#             image_filename = image_files[random_number]
#             image_path = os.path.join(image_folder, image_filename)
#             # shutil.copy(image_path, output_images_folder)
#             # Read corresponding label
#             label_filename = image_filename.replace('.png', '.txt')
#             label_file_path = os.path.join(label_folders[label], label_filename)
#             # label_file_path = os.path.join(label_folders[label], f'{os.path.splitext(txt_file_name)[0]}.txt')
#
#             with open(label_file_path, 'r') as label_file:
#                 label_parts = label_file.readline().split()
#                 label_index = label_parts[0]
#                 width = float(label_parts[1])
#                 height = float(label_parts[2])
#
#             # Copy image
#             image_name = f'{x} {y}.png'
#             shutil.copy(os.path.join(image_folder, image_filename), os.path.join(output_image_folder, image_name))
#
#             # Update new label
#             new_label = f'{label_index} {x} {y} {width} {height}\n'
#             new_labels.append(new_label)
#
#         # Write new labels to output label file
#         new_label_file_path = os.path.join(output_label_folder, txt_file_name)
#         with open(new_label_file_path, 'w') as new_label_file:
#             new_label_file.writelines(new_labels)
#


import os
import shutil
import random

# Paths
input_txt_folder = r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\sml'
output_image_folder = r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\linshi_full_information\images'
output_label_folder = r'D:\GuoZhoupeng\xfbd-dataset2\weizhi_information\linshi_full_information\labels'
image_folders = {
    's': r'D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\small',
    'm': r'D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\middle',
    'l': r'D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\large'
}
label_folders = {
    's': r'D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\small',
    'm': r'D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\middle',
    'l': r'D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\large',
    '0': r'D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\small'
}

# Create output directories if they don't exist
os.makedirs(output_image_folder, exist_ok=True)
os.makedirs(output_label_folder, exist_ok=True)

# Process each txt file in the input folder
for txt_file_name in os.listdir(input_txt_folder):

    txt_file_path = os.path.join(input_txt_folder, txt_file_name)

    # Check if the file is empty
    if os.path.getsize(txt_file_path) == 0:
        print(f"Skipping empty file: {txt_file_name}")
        continue
    else:
        print(f"opt file: {txt_file_name}")
        with open(txt_file_path, 'r') as txt_file:
            lines = txt_file.readlines()

        new_labels = []

        for line in lines:
            parts = line.split()
            label = parts[0]
            x = float(parts[1])
            y = float(parts[2])
            label_index_random = random.randint(1,2)
            while True:
                    image_folder = image_folders[label]
                    image_files = os.listdir(image_folder)
                    n=len(image_files)
                    random_number = random.randint(0, n-1)
                    image_filename = image_files[random_number]
                    image_path = os.path.join(image_folder, image_filename)
                    # shutil.copy(image_path, output_images_folder)
                    # Read corresponding label
                    label_filename = image_filename.replace('.png', '.txt')
                    label_file_path = os.path.join(label_folders[label], label_filename)
                    # label_file_path = os.path.join(label_folders[label], f'{os.path.splitext(txt_file_name)[0]}.txt')

                    with open(label_file_path, 'r') as label_file:
                        label_parts = label_file.readline().split()
                        label_index = label_parts[0]
                        width = float(label_parts[1])
                        height = float(label_parts[2])
                    if label_index == label_index_random:
                        continue
                    else:
                        break

            # Copy image
            image_name = f'{x} {y}.png'
            shutil.copy(os.path.join(image_folder, image_filename), os.path.join(output_image_folder, image_name))

            # Update new label
            new_label = f'{label_index} {x} {y} {width} {height}\n'
            new_labels.append(new_label)

        # Write new labels to output label file
        new_label_file_path = os.path.join(output_label_folder, txt_file_name)
        with open(new_label_file_path, 'w') as new_label_file:
            new_label_file.writelines(new_labels)



