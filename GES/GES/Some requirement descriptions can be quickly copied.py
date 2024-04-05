"""
请帮我写一段python代码，代码前提如下：
1.
D:\GuoZhoupeng\xfbd-dataset2\yolo-xfbd-delete ex small object\center txt ++9 - del edge and in label and connected points在这个路径下的文件夹A存放着很多个txt文件，每个txt文件都对应一个图像（所有图像的原尺寸都很大），txt文件中的内容为图像中某些点的位置信息，具体内容如下：
0 0.7611493652343754 0.8264149902343749
0 0.35108964843749996 0.15271127929687492
0 0.826904296875 0.6911179361979166
0 0.30214230143229165 0.3638953776041667
（其中第一个数代表类别标签索引，这个类别标签不需要，我们只用后两个点。第二三个数代表点在图像中的位置信息x和y。像素位置x和y是具体的像素位置再除以图片尺寸后的结果，比如x和y假如是50和100.则对应的txt文件中xy的值是：50/1024和100/1024.）

2.
1.中的txt文件所对应的图像都保存于文件夹：image_folder = "D:/GuoZhoupeng/datasets/xfbd_yolo/val/images"另外，每张图片中目标标签均存放于一个txt文件中，这些标签的格式都是yolo格式。这些txt文件均保存到的文件夹为：label_folder = "D:/GuoZhoupeng/datasets/xfbd_yolo/val/labels"的地方，另外图片原尺寸为1024*1024。

我们需要通过以上前提，去寻找，图像中的类别标签为1和2的大中小目标，并将对应的图片与标签分别保存，保存路径如下：
  其中，需要寻找的目标的内容包括：1.从图片中截取的类别索引为1和2的目标的图片。2.所截取目标的标签信息和w和h的信息。这个标签信息需要每个截取出来的图片都有对应的一个txt文件去表示。
  其次，需要将所截取的目标计算其面积，并分为大中小三类目标，小目标即小于32*32像素面积大小的目标，中目标即像素面积为32*32-96*96大小的目标，大目标即像素面积大于96*96的目标。
  将截取到的小目标的图片存放到D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\small
  将截取到的中目标的图片存放到D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\middle
  将截取到的大目标的图片存放到D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\images\large
  将截取到的小目标的标签存放到D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\small
  将截取到的中目标的标签存放到D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\middle
  将截取到的大目标的标签存放到D:\GuoZhoupeng\xfbd-dataset2\train-val bigger300 xfbd-damage images(without ex small object)\labels\large
"""