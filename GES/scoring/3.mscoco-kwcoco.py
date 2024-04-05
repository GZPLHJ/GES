import json

def convert_mscoco_to_kwcoco(mscoco_annotations_file, output_file):
    with open(mscoco_annotations_file, 'r') as f:
        mscoco_data = json.load(f)

    kwcoco_data = {
        'images': [],
        'annotations': [],
        'categories': []
    }

    # Create a mapping from MSCOCO category IDs to KWCOCO category IDs
    category_mapping = {}

    # Convert MSCOCO categories to KWCOCO categories
    for category in mscoco_data['categories']:
        kwcoco_category = {
            'id': len(kwcoco_data['categories']) + 1,
            'name': category['name']
            # Add other category properties if needed, e.g., 'supercategory'
        }
        kwcoco_data['categories'].append(kwcoco_category)
        category_mapping[category['id']] = kwcoco_category['id']

    # Convert MSCOCO images to KWCOCO images
    for image in mscoco_data['images']:
        kwcoco_image = {
            'id': image['id'],
            'file_name': image['file_name'],
            'height': image['height'],
            'width': image['width']
            # Add other image properties if needed
        }
        kwcoco_data['images'].append(kwcoco_image)

    # Convert MSCOCO annotations to KWCOCO annotations
    for annotation in mscoco_data['annotations']:
        # Provide a default value of 0 for 'iscrowd' if it is missing
        iscrowd = annotation.get('iscrowd', 0)
        kwcoco_annotation = {
            'id': annotation['id'],
            'image_id': annotation['image_id'],
            'category_id': category_mapping[annotation['category_id']],
            'bbox': annotation['bbox'],
            'area': annotation['area'],
            'iscrowd': iscrowd,
            'score':annotation['score']
            # Add other annotation properties if needed
        }
        kwcoco_data['annotations'].append(kwcoco_annotation)

    # Save the KWCOCO annotations to the output file
    with open(output_file, 'w') as f:
        json.dump(kwcoco_data, f)

if __name__ == '__main__':
    # Replace 'mscoco_annotations.json' with the path to your MSCOCO annotations file
    mscoco_annotations_file = r"D:\GuoZhoupeng\xfbd训练日志\训练日志3+score\yolov8x\正常 no del\val100\predrection_-image-id-mscoco.json"
    # Replace 'kwcoco_annotations.json' with the desired output path for KWCOCO annotations
    output_file = r"D:\GuoZhoupeng\xfbd训练日志\训练日志3+score\yolov8x\正常 no del\val100\predrection_-image-id-kwcoco-score.json"

    convert_mscoco_to_kwcoco(mscoco_annotations_file, output_file)