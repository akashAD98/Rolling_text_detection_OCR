import os
import easyocr
import cv2

# Define the path to the input images folder and output text files folder
input_folder = '/content/drive/MyDrive/ocr/900hdimg/sorted_demo_ssim_frames'
output_folder = '/content/drive/MyDrive/ocr/900hdimg/op_uni_frames'

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

# Loop through each image file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        # Read the image and apply preprocessing
        image_path = os.path.join(input_folder, filename)
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Read the text in the preprocessed image
        results = reader.readtext(thresh)

        # Write the text to a text file
        output_path = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}.txt')
        with open(output_path, 'w') as f:
            for result in results:
                f.write(result[1] + '\n')
