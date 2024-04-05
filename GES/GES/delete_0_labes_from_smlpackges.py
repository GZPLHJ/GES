import os

# 指定文件夹路径
folder_path = r'E:\xfbd_clusters(6-wuqiong)\sml-smote_clusters_have_run - del_edge_connect'

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)

        # 打开文件进行读取和处理
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # 查找包含以0开头的行的文件
        has_zero_start_line = any(line.strip().startswith('0') for line in lines)

        if has_zero_start_line:
            # 删除文件内容
            with open(file_path, 'w') as file:
                file.truncate(0)

            print(f"Deleted content in file: {filename}")
