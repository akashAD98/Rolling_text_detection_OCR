import os
import easyocr
import cv2

# Define the path to the input images folder and output text files folder
input_folder = '/content/drive/MyDrive/ocr/new_ocr/13sec_78conf_img'
output_folder = '/content/drive/MyDrive/ocr/new_ocr/OP_txt_13sec_78conf'

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

# Define the confidence threshold
confidence_threshold = 0.65

# Loop through each image file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        # Read the image and apply preprocessing
        image_path = os.path.join(input_folder, filename)
        img = cv2.imread(image_path)

        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


        # Apply thresholding to create a binary image
        thresh_value, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Apply a median filter to remove noise
        filtered_image = cv2.medianBlur(binary_image, 3)

        # Read the text in the preprocessed image
        results = reader.readtext(filtered_image)

        # Write the text to a text file if the confidence score is above the threshold
        output_path = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}.txt')
        with open(output_path, 'w') as f:
            for result in results:
                if result[2] >= confidence_threshold:
                    f.write(f"{result[1]}\n")
