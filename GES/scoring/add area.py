import json

# 读取包含预测结果的MSCOCO JSON文件
with open(r'D:\GuoZhoupeng\xfbd训练日志\训练日志2\平行实验\auto assign\pridect.json', 'r') as json_file:
    coco_data = json.load(json_file)

# 获取预测结果列表
predictions = coco_data['annotations']

# 将每个预测结果的iscrowd字段设置为0
for prediction in predictions:
    bbox = prediction['bbox']
    x,y,w,h = bbox[0],bbox[2],bbox[1],bbox[3]
    bbox[0], bbox[1], bbox[2], bbox[3]= x,y,w,h
    prediction['bbox']=bbox
    area = w*h
    prediction['area'] = area

# 保存修改后的JSON文件
with open(r'D:\GuoZhoupeng\xfbd训练日志\训练日志2\平行实验\auto assign\pridect-icw0.json', 'w') as json_file:
    json.dump(coco_data, json_file)
