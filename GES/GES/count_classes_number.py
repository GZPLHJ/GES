import os

# 定义类别索引
target_classes = [0, 1, 2]

# 指定标签文件所在的文件夹路径
label_folder = r'E:\xfbd_clusters_n-bi3\xfbd_kmeans+smote+taoyi\labels\train'

# 初始化计数器字典，用于存储每个类别的目标数量
target_counts = {class_idx: 0 for class_idx in target_classes}

# 遍历标签文件夹中的每个文件
for filename in os.listdir(label_folder):
    if filename.endswith(".txt"):
        label_path = os.path.join(label_folder, filename)

        # 打开标签文件并逐行解析
        with open(label_path, 'r') as f:
            lines = f.readlines()

        # 遍历标签文件中的每一行
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 1:
                # 提取类别索引
                class_idx = int(parts[0])

                # 如果类别索引在目标类别列表中，增加计数器
                if class_idx in target_classes:
                    target_counts[class_idx] += 1

# 打印统计结果
for class_idx, count in target_counts.items():
    print(f"类别 {class_idx} 的目标数量为：{count}")
