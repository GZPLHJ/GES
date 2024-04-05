import json

# 读取原始的 MSCOCO JSON 文件
with open(r'E:\xfbd_clusters_n-bi3\data\coco\annotations\instances_val2017.json', 'r') as file:
    data = json.load(file)

# 遍历每个 annotation 条目，添加 "iscrowd": 0
for annotation in data['annotations']:
    annotation['iscrowd'] = 0

# 保存更新后的 JSON 文件
with open('updated_coco.json', 'w') as updated_file:
    json.dump(data, updated_file)
