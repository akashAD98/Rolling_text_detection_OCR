import cv2
import numpy as np
import os

from skimage.metrics import structural_similarity as ssim
import easyocr

# Define the video file path
video_path = "/content/drive/MyDrive/ocr/900hdimg/edited_firlmorevideo_2minhd.mp4"

# Create a folder for the output frames
output_folder = "/content/drive/MyDrive/ocr/900hdimg/uni_frame"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Initialize EasyOCR reader for text extraction
reader = easyocr.Reader(['en'])

# Initialize variables for frame comparison
previous_frame = None
similarity_threshold = 0.97

# Open the video file
cap = cv2.VideoCapture(video_path)

# Loop through each frame in the video
while cap.isOpened():
    # Read the frame from the video
    ret, frame = cap.read()

    # If there are no more frames, exit the loop
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Extract the text from the grayscale image using EasyOCR
    result = reader.readtext(gray)

    # Concatenate all the detected text into a single string
    text = ' '.join([word[1] for word in result])

    # If there was no text detected in the frame, skip it
    if len(text) == 0:
        continue

    # If this is not the first frame, compare it to the previous frame
    if previous_frame is not None:
        # Calculate the similarity between the previous and current frame using SSIM
        sim = ssim(previous_frame, gray)

        # If the similarity is less than the threshold, add the current frame to the unique frames list
        if sim < similarity_threshold:
            # Save the current frame to the output folder
            filename = os.path.join(output_folder, f"frame_{cap.get(cv2.CAP_PROP_POS_FRAMES)}.jpg")
            cv2.imwrite(filename, frame)

            # Set the current frame as the previous frame for the next iteration
            previous_frame = gray

    else:
        # If this is the first frame, save it to the output folder and set it as the previous frame for the next iteration
        filename = os.path.join(output_folder, f"frame_{cap.get(cv2.CAP_PROP_POS_FRAMES)}.jpg")
        cv2.imwrite(filename, frame)
        previous_frame = gray

# Release the video capture object and close the window
cap.release()
cv2.destroyAllWindows()
