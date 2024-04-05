import json

def replace_image_id_with_id(json_file1, json_file2, output_file):
    # Step 1: Read the first JSON file and create a dictionary with id and file_name mapping
    id_file_name_map = {}
    with open(json_file1, 'r') as f1:
        data1 = json.load(f1)
        for image_info in data1['images']:
            id_file_name_map[image_info['file_name']] = image_info['id']

    # Step 2: Replace image_id with id in the second JSON file
    with open(json_file2, 'r') as f2:
        data2 = json.load(f2)
        for prediction in data2:
            file_name = prediction['image_id']
            if file_name+".png" in id_file_name_map:
                prediction['image_id'] = id_file_name_map[file_name+".png"]

    # Step 3: Save the modified data as a new JSON file
    with open(output_file, 'w') as f_out:
        json.dump(data2, f_out)

# Replace image_id with id in the second JSON file and save the result
json_file1 = r"D:\GuoZhoupeng\object_detect\yolov8\xfbd\instances_val2017_del_ex-smalllabel.json"
json_file2 = r"D:\GuoZhoupeng\xfbd训练日志\训练日志2\random_aug\val8\predictions.json"
output_file = r"D:\GuoZhoupeng\xfbd训练日志\训练日志2\random_aug\val8\predrection_-id.json"

replace_image_id_with_id(json_file1, json_file2, output_file)
