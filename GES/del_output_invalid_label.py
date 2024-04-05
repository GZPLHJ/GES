import json

# 假设preds是模型的预测结果
valid_category_ids = set(range(3))  # num_categories是COCO数据集中的类别总数

# 读取模型预测结果的输入数据
with open(r'E:\xfbd_clusters_n-bi3\data\coco\annotations\train.json', 'r') as file:
    preds = json.load(file)

# 筛选预测结果中的无效类别标签和输出无效标签
filtered_preds = []
invalid_labels = []
for pred in preds:
    labels = pred['labels']
    valid_labels = [label for label in labels if label in valid_category_ids]
    if valid_labels:
        pred['labels'] = valid_labels
        filtered_preds.append(pred)
    else:
        invalid_labels.extend(labels)

# 输出无效标签
print("无效的标签：", invalid_labels)

# 打开COCO JSON结果文件并写入有效标签的预测结果
with open(r'E:\xfbd_clusters_n-bi3\data\coco\annotations\train.json', 'w') as outfile:
    json.dump(filtered_preds, outfile)
