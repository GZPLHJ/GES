from PIL import Image, ImageDraw
import os
import tqdm

def draw_bounding_boxes(image_path, label_path, output_path):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    with open(label_path, 'r') as label_file:
        lines = label_file.readlines()

    color_map = {0: 'white', 1: 'yellow', 2: 'red'}

    for line in lines:
        parts = line.strip().split()
        label = int(parts[0])
        x_center = float(parts[1])
        y_center = float(parts[2])
        width = float(parts[3])
        height = float(parts[4])

        # Convert YOLO format to bounding box coordinates
        x1 = int((x_center - width / 2) * image.width)
        y1 = int((y_center - height / 2) * image.height)
        x2 = int((x_center + width / 2) * image.width)
        y2 = int((y_center + height / 2) * image.height)

        color = color_map.get(label, 'white')

        # Draw bounding box
        draw.rectangle([x1, y1, x2, y2], outline=color, width=3)

    output_image_path = os.path.join(output_path, os.path.basename(image_path))
    image.save(output_image_path)
    print(f"Processed {image_path} and saved to {output_image_path}")


# 输入的文件夹路径和输出文件夹路径
input_folder = r"E:\xfbd_clusters_n-bi3\xfbd_kmeans+smote+taoyi-wc\images\train"
label_folder = r"E:\xfbd_clusters_n-bi3\xfbd_kmeans+smote+taoyi-wc\labels\train"
output_folder = r"E:\xfbd_clusters_n-bi3\xfbd_kmeans+smote+taoyi-wc\gt"

# 遍历输入文件夹中的图片和标签文件
for image_name in os.listdir(input_folder):
    if image_name.endswith('.png'):
        image_path = os.path.join(input_folder, image_name)
        label_path = os.path.join(label_folder, image_name.replace('.png', '.txt'))

        if os.path.exists(label_path):
            draw_bounding_boxes(image_path, label_path, output_folder)
        else:
            print(f"No label file found for {image_name}")

