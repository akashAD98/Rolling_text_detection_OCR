## correct format working correctly 
## lineup logic with bbox format data


import cv2
import easyocr
import numpy as np
import os

# Define the path to the folder containing the image files
input_folder_path = '/content/drive/MyDrive/zz_newocr/inputimg'
output_folder_path = '/content/drive/MyDrive/zz_newocr/output_txtNew'
bbox_folder_path = '/content/drive/MyDrive/zz_newocr/output_bboxNew'

# Create output folders if they do not exist
os.makedirs(output_folder_path, exist_ok=True)
os.makedirs(bbox_folder_path, exist_ok=True)

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

def get_bbox_parameters(bbox):
    """Retrieve parameters of the bounding box"""
    xmin = min([point[0] for point in bbox])
    ymin = min([point[1] for point in bbox])
    xmax = max([point[0] for point in bbox])
    ymax = max([point[1] for point in bbox])
    
    return {"left": xmin, "top": ymin, "width": xmax - xmin, "height": ymax - ymin}

def lineup(boxes):
    """Combine boxes that are on the same line"""
    linebox = None
    for box in sorted(boxes, key=lambda x: get_bbox_parameters(x[0])['top']):
        bbox_params = get_bbox_parameters(box[0])
        if linebox is None:
            linebox = {"left": bbox_params['left'], "top": bbox_params['top'], "width": bbox_params['width'], "height": bbox_params['height'], "text": box[1]}  # first line begins
        elif bbox_params['top'] <= linebox['top'] + linebox['height']:  # box in same line
            linebox['top'] = min(linebox['top'], bbox_params['top'])
            linebox['left'] = min(linebox['left'], bbox_params['left']) 
            linebox['width'] = max(linebox['left'] + linebox['width'], bbox_params['left'] + bbox_params['width']) - linebox['left'] 
            linebox['height'] = max(linebox['top'] + linebox['height'], bbox_params['top'] + bbox_params['height']) - linebox['top'] 
            linebox['text'] += ' ' + box[1]
        else:  # Start a new line
            yield linebox  # Return the completed linebox
            linebox = {"left": bbox_params['left'], "top": bbox_params['top'], "width": bbox_params['width'], "height": bbox_params['height'], "text": box[1]}  # Start a new line with the current box
    if linebox is not None:  # If there is a linebox left
        yield linebox  # Return it

for filename in os.listdir(input_folder_path):
    # Skip non-image files
    if not (filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg')):
        continue

    # Define the paths for this image
    image_path = os.path.join(input_folder_path, filename)
    output_text_path = os.path.join(output_folder_path, filename.rsplit('.', 1)[0] + '.txt')
    output_image_path = os.path.join(bbox_folder_path, filename)

    # Read the image
    img = cv2.imread(image_path)

    # Read the text from the image
    results = reader.readtext(image_path, width_ths=3, detail=1)

    # Filter out results with less than 60% confidence
    results = [result for result in results if result[2] >= 0.55]

    lines = list(lineup(results))

    # Save the results in a text file
    with open(output_text_path, 'w') as f:
        for line in lines:
            bbox_str = f"[({line['left']}, {line['top']}), ({line['left'] + line['width']}, {line['top']}), ({line['left'] + line['width']}, {line['top'] + line['height']}), ({line['left']}, {line['top'] + line['height']})]"
            f.write(f"{line['text']}, BBox: {bbox_str}\n")

    # Draw bounding boxes on the image and save the image
    for line in lines:
        bbox = np.array([(line['left'], line['top']), (line['left'] + line['width'], line['top']), (line['left'] + line['width'], line['top'] + line['height']), (line['left'], line['top'] + line['height'])], dtype=np.int32).reshape((-1, 1, 2))
        cv2.polylines(img, [bbox], isClosed=True, color=(0, 255, 0), thickness=2)
    cv2.imwrite(output_image_path, img)
