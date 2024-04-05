import json

def replace_annotations(json_file1, json_file2, output_file, iscrowd_threshold=50):
    # Step 1: Read the first JSON file and extract existing annotations
    with open(json_file1, 'r') as f1:
        data1 = json.load(f1)
        existing_annotations = data1.get('annotations', [])

    # Step 2: Read the second JSON file and create new annotations based on predictions
    new_annotations = []
    with open(json_file2, 'r') as f2:
        predictions = json.load(f2)
        for idx, prediction in enumerate(predictions):
            image_id = prediction['image_id']
            bbox = prediction['bbox']
            score = prediction['score']

            # Calculate the width and height of the bounding box
            bbox_width = bbox[2]
            bbox_height = bbox[3]

            # Determine iscrowd value based on bbox size
            iscrowd = 1 if bbox_width * bbox_height > iscrowd_threshold else 0

            # Get the category_id from the second JSON file prediction
            category_id = prediction['category_id']

            # Create a new annotation entry
            new_annotation = {
                'image_id': image_id,
                'category_id': category_id,  # Update this value based on your category mapping
                'bbox': bbox,
                'id': idx + 1,  # Assigning id based on the order in predictions
                'area': bbox_width * bbox_height,
                'iscrowd': iscrowd,
                'segmentation': [],  # Update this value if necessary
                'attributes': '',  # Update this value if necessary
                'score': score  # Adding the score information
            }

            new_annotations.append(new_annotation)

    # Step 3: Update the first JSON file with the new annotations
    data1['annotations'] = new_annotations

    # Step 4: Save the modified data as a new JSON file
    with open(output_file, 'w') as f_out:
        json.dump(data1, f_out)

# Replace annotations in the first JSON file with predictions from the second JSON file
json_file1 = r'D:\GuoZhoupeng\xfbd-datasets1\xfbd_coco\annotations\instances_val2017_3category_id__del_ex-smalllabel.json'
json_file2 = r"D:\GuoZhoupeng\xfbd训练日志\训练日志2\random_aug\val8\predrection_-id.json"
output_file = r"D:\GuoZhoupeng\xfbd训练日志\训练日志2\random_aug\val8\predrection_-image-id-mscoco.json"

# Set the iscrowd_threshold based on your dataset characteristics
iscrowd_threshold = 50

replace_annotations(json_file1, json_file2, output_file, iscrowd_threshold)


