import os

folder_path = r"E:\xfbd_clusters(6-wuqiong)\4.2-del_inlabel_smote_clusters_have_run - del_edge_connect"  # 替换为您要统计的文件夹路径

# 初始化计数器
count = 0

# 遍历文件夹中的文件
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith(".txt"):  # 检查文件扩展名
            file_path = os.path.join(root, file)
            if os.path.getsize(file_path) > 0:  # 检查文件大小是否大于0
                count += 1

print("大小不为0的.txt文件数量:", count)
