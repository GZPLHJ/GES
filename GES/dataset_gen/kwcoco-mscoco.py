# import json
#
# # 加载KW-COCO数据集的标签文件
# with open(r'D:\学习总结\我的论文\xbd\code\xview2\xview2_hold_label_kwcoco.json', 'r') as f:
#     kwcoco_labels = json.load(f)
#
# # 定义类别名称映射关系
# mapping = {
#     "no-damage": "building",
#     "minor-damage": "building",
#     "major-damage": "building",
#     "destroyed": "building"
# }
#
# # 更新类别名称
# for category in kwcoco_labels['categories']:
#     category['name'] = mapping.get(category['name'], category['name'])
#
# # 保存更新后的标签文件
# with open('xview2_hold_mscoco_labels.json', 'w') as f:
#     json.dump(kwcoco_labels, f)

import json

# 加载KW-COCO数据集的标签文件
with open(r'E:\xfbd_hold_val_label_kwcoco.json', 'r') as f:
    kwcoco_labels = json.load(f)

# 定义类别名称映射关系
mapping = {
    "no-damage": "building",
    "minor-damage": "building",
    "major-damage": "building",
    "destroyed": "building"
}

# 更新类别名称
for category in kwcoco_labels['categories']:
    category['name'] = mapping.get(category['name'], category['name'])

# 生成MSCOCO数据集格式的字典
mscoco_labels = {
    "info": {
        "description": "mpj Dataset",
        "url": "www.mpj520.com",
        "version": "1.0",
        "year": 2022,
        "contributor": "mpj",
        "date_created": "2023-06-05 09:45:13.302179"
    },
    "licenses": [
        {
            "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
            "id": 1,
            "name": "Attribution-NonCommercial-ShareAlike License"
        }
    ],
    "images": [
        {
            "id": image['id'],
            "file_name": image['file_name'],
            "width": 2048,
            "height": 1024,
            "date_captured": "2023-06-05 09:45:13.353861",
            "license": 1
        } for image in kwcoco_labels['images']
    ],
    "annotations": kwcoco_labels['annotations']
}

# 保存MSCOCO数据集格式的标签文件
with open('xfbd_hold_val_label_mscoco.json', 'w') as f:
    json.dump(mscoco_labels, f, indent=1)

