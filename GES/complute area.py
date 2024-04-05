# label = "3 0.127147216796875 0.17994077148437498 0.01465107421875 0.01413701171875"
# label = "3 0.24785693359375 0.521004638671875 0.0185845703125 0.01436083984375"
label = "2 0.79317802734375 0.01967392578125 0.0112224609375 0.014533984375"

parts = label.split()
class_index = int(parts[0])
x_center = float(parts[1])
y_center = float(parts[2])
width = float(parts[3])
height = float(parts[4])

# 原始图片尺寸
image_width = 1024
image_height = 1024

# 转换为绝对坐标
abs_x_center = x_center * image_width
abs_y_center = y_center * image_height
abs_width = width * image_width
abs_height = height * image_height

# 计算目标面积
area = abs_width * abs_height
print("目标的面积:", area)
