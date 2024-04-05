import json

# 读取原始JSON文件
with open(r'D:\GuoZhoupeng\xfbd-datasets1\xfbd_coco\annotations\instances_val2017_3category_id.json', 'r') as json_file:
    data = json.load(json_file)

# 获取annotations列表
annotations = data.get('annotations', [])

# 过滤出area大于等于300的标签
filtered_annotations = [annotation for annotation in annotations if annotation['area'] >= 300]

# 更新data字典中的annotations项
data['annotations'] = filtered_annotations


# 将过滤后的数据保存到新的JSON文件
with open(r'D:\GuoZhoupeng\xfbd-datasets1\xfbd_coco\annotations\instances_val2017_3category_id__del_ex-smalllabel.json', 'w') as new_json_file:
    json.dump(data, new_json_file, indent=4)




print("已删除area小于300的标签并保存到新的JSON文件。")
