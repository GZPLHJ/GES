import json

# 读取原始的MSCOCO JSON文件
with open(r'E:\xfbd_clusters_n-bi3\cocoiiiiiiiilabel\val.json', 'r') as file:
    coco_data = json.load(file)

# 减一每个目标的id
for annotation in coco_data['annotations']:
    annotation['id'] -= 1

# 保存修改后的JSON文件
with open(r'E:\xfbd_clusters_n-bi3\cocoiiiiiiiilabel\val.json', 'w') as outfile:
    json.dump(coco_data, outfile)
