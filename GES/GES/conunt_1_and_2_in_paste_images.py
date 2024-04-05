import os

# 指定包含txt文件的文件夹路径
folder_path = r'E:\xfbd_clusters(6-wuqiong)\6.2full information\labels'

# 初始化标签1的图片计数器
label_1_count = 0
label_2_count = 0
# 遍历文件夹中的所有txt文件
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            # 逐行读取txt文件
            lines = file.readlines()
            for line in lines:
                # 将每行的内容拆分成标签和其他信息
                parts = line.strip().split()
                if len(parts) >= 1 and int(parts[0]) == 1:
                    # 如果标签为1，则增加标签1的图片计数
                    label_1_count += 1
                if len(parts) >= 1 and int(parts[0]) == 2:
                    # 如果标签为1，则增加标签1的图片计数
                    label_2_count += 1

# 打印标签1的图片总数
print("标签为1的图片总数:", label_1_count)
print("标签为1的图片总数:", label_2_count)
