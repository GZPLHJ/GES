import json

# 读取包含预测结果的MSCOCO JSON文件
with open(r'H:\data\coco\annotations\instances_val2017.json', 'r') as json_file:
    coco_data = json.load(json_file)

# 获取预测结果列表
predictions = coco_data['annotations']

# 将每个预测结果的iscrowd字段设置为0
for prediction in predictions:
    prediction['iscrowd'] = 0

# 保存修改后的JSON文件
with open(r'E:\xfbd_clusters_n-bi3\data\coco\annotations\instances_val2017.json', 'w') as json_file:
    json.dump(coco_data, json_file)
#
# import json
#
# # 读取包含预测结果的MSCOCO JSON文件
# with open(r'E:\xfbd_clusters_n-bi3\data\coco\annotations\instances_train2017.json', 'r') as json_file:
#     coco_data = json.load(json_file)
#
# # 获取预测结果列表
# predictions = coco_data['annotations']
#
# # 将每个预测结果的iscrowd字段设置为0
# for prediction in predictions:
#     prediction['segmentation'] = []
#
# # 保存修改后的JSON文件
# with open(r'E:\xfbd_clusters_n-bi3\data\coco\annotations\instances_train2017.json', 'w') as json_file:
#     json.dump(coco_data, json_file)
