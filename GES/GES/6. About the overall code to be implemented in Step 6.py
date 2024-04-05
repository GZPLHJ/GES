"""
请帮我写一段关于目标检测任务的python代码，代码前提如下：
首先此目标检测任务的训练集的图像存放于：D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\images\train
目标检测任务的训练集的标签存放于：D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\labels\train
此目标检测任务有三个类别，类别的标签索引是0和1和2。注意：所有的标签信息都是按照yolo格式写的。

另外，D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\s m l 4.center txt ++9 -smote-del in label points这个路径下的文件夹A中存放着很多txt文件
每个txt文件对应一个图像，每个txt文件中的内容示例如下：
s 0.4164822916666668 0.40687895507812505
m 0.7611493652343754 0.762106884765625
l 0.31573746892755683 0.06253630149147726
其中，第二三个数代表图像中一个点的位置，第二个数代表x坐标，第三个数代表y坐标。第一个字符代表这个点处我可以插入小目标、中目标还是大目标。如果是s则可以插入小目标，如果是m则可以插入中目标，如果是l则可以插入大目标。

在这之前，我们已经截取了很多标签索引为1和2的目标的图片，用于数据增强，而截取后的目标图片的相关信息也均保存于一个txt文件中，示例如下：
2 0.0192708984375 0.0196765625
第一个数字2代表着标签索引，第二三个数字代表着这个目标的宽width和高hight。
其中，截取的目标中的小目标的图片保存于：D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\small
其中，截取的目标中的小目标的标签保存于：D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\small
其中，截取的目标中的中目标的图片保存于：D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\middle
其中，截取的目标中的中目标的标签保存于：D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\middle
其中，截取的目标中的大目标的图片保存于：D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\large
其中，截取的目标中的大目标的标签保存于：D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\large

代码的要求如下：
请根据文件夹A中的txt文件保存的每个图像中点的位置信息以及可以放置的大中小的目标的信息将对应的截取的图片插入到训练集的图片当中。
如果是第一个字符为s则从D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\small任意找一张小目标的图片，插入到训练集对应图像的对应位置当中。
例如D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\s m l 4.center txt ++9 -smote-del in label points这个路径下存在palu-tsunami_00000000_5b4fa968-09ec-4db8-8721-8bf678ddd01b_post_disaster.txt这个文件，这个文件的内容如下：
s 0.4164822916666668 0.40687895507812505
m 0.7611493652343754 0.762106884765625
l 0.31573746892755683 0.06253630149147726
先看第一行：第一行的第一个字符为s，则从D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\small文件夹中任意找一个图片palu-tsunami_00000000_32a2f3c2-22dc-4317-b1d4-9b15a1a54852_post_disaster.png
此图片对应的信息为：2 0.0192708984375 0.0196765625
将此图片插入到，D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\images\train\palu-tsunami_00000000_5b4fa968-09ec-4db8-8721-8bf678ddd01b_post_disaster.png的x坐标为0.4164822916666668*1024，y坐标为0.40687895507812505*1024的位置上。
并且将：2 0.4164822916666668 0.40687895507812505 0.0192708984375 0.0196765625的标签信息，插入到D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\labels\train\palu-tsunami_00000000_5b4fa968-09ec-4db8-8721-8bf678ddd01b_post_disaster.txt标签文件中。
再看第二三行：第一个字符分别是m和l则对应从D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\middle和D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\large寻找图像，之后执行相同的工作。
请写出完整的代码

"""

"""
请帮我写一段关于目标检测任务的python代码，代码前提如下：
D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\s m l 4.center txt ++9 -smote-del in label points这个路径下的文件夹A中存放着很多txt文件
每个txt文件对应一个图像，每个txt文件中的内容示例如下：
s 0.4164822916666668 0.40687895507812505
m 0.7611493652343754 0.762106884765625
l 0.31573746892755683 0.06253630149147726
其中，第二三个数代表图像中一个点的位置，第二个数代表x坐标，第三个数代表y坐标。第一个字符代表这个点处我可以插入小目标、中目标还是大目标。如果是s则可以插入小目标，如果是m则可以插入中目标，如果是l则可以插入大目标。

另外，我们保存了很多标签索引为1和2的目标的图片，用于数据增强，而保存后的目标图片的相关信息也均保存于一个txt文件中，示例如下：
2 0.0192708984375 0.0196765625
第一个数字2代表着标签索引，第二三个数字代表着这个目标的宽width和高hight。

其中，截取的目标中的小目标的图片保存于：D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\small
其中，截取的目标中的小目标的标签保存于：D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\small
其中，截取的目标中的中目标的图片保存于：D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\middle
其中，截取的目标中的中目标的标签保存于：D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\middle
其中，截取的目标中的大目标的图片保存于：D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\large
其中，截取的目标中的大目标的标签保存于：D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\large

代码的要求如下：
请根据文件夹A中的txt文件保存的每个图像中点的位置信息以及可以放置的大中小的目标的信息构造出新的标签并将对应的图片保存到新的文件夹。
例如D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\s m l 4.center txt ++9 -smote-del in label points这个路径下存在palu-tsunami_00000000_5b4fa968-09ec-4db8-8721-8bf678ddd01b_post_disaster.txt这个文件，这个文件的内容如下：
s 0.4164822916666668 0.40687895507812505
m 0.7611493652343754 0.762106884765625
l 0.31573746892755683 0.06253630149147726
先看第一行：第一行的第一个字符为s，则从D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\small文件夹中任意找一个图片palu-tsunami_00000000_32a2f3c2-22dc-4317-b1d4-9b15a1a54852_post_disaster.png
此图片对应的信息为：2 0.0192708984375 0.0196765625
将此图片复制到，D:\GuoZhoupeng\xfbd-dataset2\full information 1and2 object images\images这个文件夹下。
并且将：2 0.4164822916666668 0.40687895507812505 0.0192708984375 0.0196765625的标签信息，复制到D:\GuoZhoupeng\xfbd-dataset2\full information 1and2 object images\labels的文件夹下。
再看第二三行：第一个字符分别是m和l则对应从D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\middle和D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\large寻找图像，之后执行相同的工作。
请写出完整的代码

D:\GuoZhoupeng\xfbd-dataset2\full information 1and2 object images\images


没有实现不要用！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
没有实现不要用！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
没有实现不要用！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
没有实现不要用！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
没有实现不要用！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
没有实现不要用！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
没有实现不要用！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
没有实现不要用！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
没有实现不要用！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
没有实现不要用！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
没有实现不要用！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
没有实现不要用！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
没有实现不要用！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
没有实现不要用！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
没有实现不要用！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
没有实现不要用！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
没有实现不要用！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
没有实现不要用！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
没有实现不要用！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
没有实现不要用！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！


"""


import os
import shutil

# 设置相关路径
src_small_images_dir = r"D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\small"
src_middle_images_dir = r"D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\middle"
src_large_images_dir = r"D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\large"
src_labels_dir = r"D:\GuoZhoupeng\fbd-dataset2\yolo-xfbd-delete ex small object\labels\train"
output_images_dir = r"D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-kmeans+taoyi+smote+sml\train\images"
output_labels_dir = r"D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-kmeans+taoyi+smote+sml\train\labels"

# 获取文件夹A中的所有txt文件
txt_files_dir = r"D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\s m l 4.center txt ++9 -smote-del in label points"
txt_files = os.listdir(txt_files_dir)

# 处理每个txt文件
for txt_file in txt_files:
    txt_file_path = os.path.join(txt_files_dir, txt_file)

    # 读取txt文件内容
    with open(txt_file_path, 'r') as f:
        lines = f.readlines()

    # 遍历每一行
    for line in lines:
        parts = line.split()
        if len(parts) == 3:
            obj_type, x, y = parts

            # 获取对应的源图片和标签文件
            if obj_type == 's':
                src_image_dir = src_small_images_dir
            elif obj_type == 'm':
                src_image_dir = src_middle_images_dir
            elif obj_type == 'l':
                src_image_dir = src_large_images_dir
            else:
                continue

            # 选择一个源图片
            src_images = os.listdir(src_image_dir)
            if src_images:
                src_image = os.path.join(src_image_dir, src_images[0])

                # 构建输出图片的路径
                output_image_path = os.path.join(output_images_dir, os.path.basename(txt_file).replace('.txt', '.png'))

                # 复制源图片到输出图片路径，并更新标签文件
                shutil.copy(src_image, output_image_path)
                with open(os.path.join(output_labels_dir, txt_file), 'a') as label_file:
                    label_file.write(f"{obj_type} {x} {y}\n")

