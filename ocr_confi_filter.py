import cv2
import easyocr

reader = easyocr.Reader(['en'])

image_path = '/content/1frame_5.jpg'

# Load the image in grayscale
image = cv2.imread(image_path, 0)

# Apply thresholding to create a binary image
thresh_value, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Apply a median filter to remove noise
filtered_image = cv2.medianBlur(binary_image, 3)

# Save the filtered image
cv2.imwrite('/content/1frame_5opop.jpg', filtered_image)

# Run the filtered image through EasyOCR
result = reader.readtext(filtered_image)

# Iterate through each detected text region and print the text and confidence score
for detection in result:
    if detection[2] > 0.5:
        print("Text: ", detection[1])
        print("Confidence: ", detection[2])
