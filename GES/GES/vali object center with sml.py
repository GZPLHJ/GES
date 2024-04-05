import os
import cv2

# Paths
center_txt_folder = r'H:\paper-img\kes\label'
image_folder = r'H:\paper-img\kes\input img'
output_folder = r'H:\paper-img\kes\r w y'  # Change this to the desired output folder

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Process each center txt file
for txt_file in os.listdir(center_txt_folder):
    if txt_file.endswith('.txt'):
        txt_path = os.path.join(center_txt_folder, txt_file)
        image_name = os.path.splitext(txt_file)[0] + '.png'
        image_path = os.path.join(image_folder, image_name)
        output_image_path = os.path.join(output_folder, image_name)

        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to read image: {image_path}")
            continue

        # Read and process center coordinates from txt file
        with open(txt_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 3:  # Expected format: label x y
                label = parts[0]
                x_center = float(parts[1])
                y_center = float(parts[2])

                # Calculate pixel coordinates from YOLO format
                height, width, _ = image.shape
                x_pixel = int(x_center * width)
                y_pixel = int(y_center * height)

                # Draw a red circle at the calculated pixel coordinates
                radius = 5
                color = (0, 0, 255)  # Red
                thickness = -1  # Filled circle
                cv2.circle(image, (x_pixel, y_pixel), radius, color, thickness)

                # Write the label text at the marked point
                font = cv2.FONT_HERSHEY_SIMPLEX
                label_position = (x_pixel - 30, y_pixel + 20)
                font_scale = 1
                font_color = (0, 255, 255)  # Green
                font_thickness = 3
                cv2.putText(image, label, label_position, font, font_scale, font_color, font_thickness)

        # Save the marked image to the output folder
        cv2.imwrite(output_image_path, image)

print("Marking and image generation completed.")
