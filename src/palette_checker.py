import cv2 as cv
import numpy as np

# Define the color palette
PALETTE_BGR = [
    (220, 20, 60), (119, 11, 32), (0, 0, 142), (0, 0, 230), (106, 0, 228), 
    (0, 60, 100), (0, 80, 100), (0, 0, 70), (0, 0, 192), (250, 170, 30), 
    (100, 170, 30), (220, 220, 0), (175, 116, 175), (250, 0, 30), 
    (30, 144, 255), (0, 191, 255), (135, 206, 250), (70, 130, 180), (123, 104, 238),
    (72, 61, 139), (138, 43, 226), (148, 0, 211), (186, 85, 211), (255, 20, 147), 
    (255, 105, 180), (255, 160, 122), (255, 69, 0), (255, 99, 71), (218, 112, 214), 
    (238, 130, 238), (255, 222, 173)
]

# List of dental conditions
conditions = [
    "Caries", "Crown", "Filling", "Implant", "Malaligned", "Mandibular Canal", "Missing teeth", 
    "Periapical lesion", "Retained root", "Root Canal Treatment", "Root Piece", "impacted tooth", 
    "maxillary sinus", "Bone Loss", "Fracture teeth", "Permanent Teeth", "Supra Eruption", "TAD", 
    "abutment", "attrition", "bone defect", "gingival former", "metal band", "orthodontic brackets", 
    "permanent retainer", "post - core", "plating", "wire", "Cyst", "Root resorption"
]

# Create an image to display the colors and their BGR values
block_height = 100  # height of each color block
block_width = 130   # width of each color block
font_scale = 0.4    # scale of the font
thickness = 1       # thickness of the text
num_colors = len(PALETTE_BGR)
image_height = block_height + 80  # extra space for text below each block
image_width = block_width * num_colors

# Create a blank image
img = np.zeros((image_height, image_width, 3), dtype=np.uint8)

# Draw each color block and the BGR values below
for i, (color, condition) in enumerate(zip(PALETTE_BGR, conditions)):
    # Draw the color block
    start_x = i * block_width
    end_x = (i + 1) * block_width
    img[0:block_height, start_x:end_x] = color
    
    # Prepare the BGR text
    bgr_text = f"{color}"

    # Get the text size for centering
    text_size_bgr = cv.getTextSize(bgr_text, cv.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
    text_x_bgr = start_x + (block_width - text_size_bgr[0]) // 2
    text_y_bgr = block_height + text_size_bgr[1] + 10  # Position the text below the block
    
    # Put the BGR text below the block
    cv.putText(img, bgr_text, (text_x_bgr, text_y_bgr), cv.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)
    
    # Prepare the condition text
    condition_text = condition

    # Get the text size for centering
    text_size_condition = cv.getTextSize(condition_text, cv.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
    text_x_condition = start_x + (block_width - text_size_condition[0]) // 2
    text_y_condition = text_y_bgr + text_size_condition[1] + 10  # Position below BGR text
    
    # Put the condition text below the BGR text
    cv.putText(img, condition_text, (text_x_condition, text_y_condition), cv.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)

# Display the image
cv.imshow('Color Palette with BGR and Conditions', img)
cv.waitKey(0)
cv.destroyAllWindows()
