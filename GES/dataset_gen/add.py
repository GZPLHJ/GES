import json

# 读取原始JSON文件
json_file = r"D:\学习总结\我的论文\xbd\code\dataset_gen\xfbd_hold_train_label_mscoco.json"
with open(json_file, "r") as f:
    data = json.load(f)

# 添加licenses字段
licenses = [
    {
        "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License"
    }
]
data["licenses"] = licenses

# 添加categories字段
categories = [
    {"id": 1, "name": "no-damage"},
    {"id": 2, "name": "minor-damage"},
    {"id": 3, "name": "major-damage"},
    {"id": 4, "name": "destroyed"}
]
data["categories"] = categories

# 写入修改后的JSON文件
output_file = r"D:\学习总结\我的论文\xbd\code\dataset_gen\xfbd_hold_train_label_mscoco_modified.json"
with open(output_file, "w") as f:
    json.dump(data, f, indent=4)

print("JSON文件修改完成并保存到:", output_file)
