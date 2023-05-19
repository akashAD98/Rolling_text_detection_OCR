import os
import sys
from Levenshtein import ratio

dir_path = '/content/drive/MyDrive/NEWLOGIC_OCR_/video/22sec_ssim_Text'

# Adjust the key function to get the number after "frame_"
txt_files = sorted([f for f in os.listdir(dir_path) if f.endswith('.txt')], key=lambda f: int(f.split('_')[1].split('.')[0]))

original_stdout = sys.stdout # Save a reference to the original standard output
with open(os.path.join(dir_path, 'output_print.txt'), 'w') as f:
    sys.stdout = f # Change the standard output to the file we created.

    with open(os.path.join(dir_path, txt_files[0]), 'r') as in_file, \
            open(os.path.join(dir_path, 'output.txt'), 'w') as out_file:
        out_file.write(in_file.read().strip() + '\n')

    print(f"Processed file: {txt_files[0]}")

    start_frame = int(txt_files[0].split('_')[1].split('.')[0])  # Get the frame number from the first file name
    end_frame = start_frame + 100
    new_block = True

    for i, txt_file in enumerate(txt_files[1:]):
        current_frame = int(txt_file.split('_')[1].split('.')[0])  # Get the frame number from the current file name
        if current_frame >= end_frame:  # Check if we've moved to a new set of frames
            start_frame = current_frame
            end_frame = current_frame + 100
            new_block = True

        with open(os.path.join(dir_path, 'output.txt'), 'r') as out_file:
            output_lines = out_file.readlines()

        with open(os.path.join(dir_path, txt_file), 'r') as in_file:
            in_lines = in_file.readlines()

            max_ratio = 0.8
            start_idx = None
            for output_line in reversed(output_lines): 
                last_words_split = output_line.strip().split()
                if last_words_split: 
                    found_match = False
                    for i, line in enumerate(in_lines):
                        line_split = line.split()
                        matches = sum([1 for last_word in last_words_split for word in line_split if ratio(last_word, word) > max_ratio])
                        if matches > len(last_words_split) * 0.6:  
                            start_idx = i
                            found_match = True
                            break
                    if found_match:
                        break

            if start_idx is None:
                start_idx = 0

            with open(os.path.join(dir_path, 'output.txt'), 'a') as out_file:
                for line in in_lines[start_idx:]:
                    if line not in output_lines:
                        out_file.write(line.strip() + '\n')

            # Print the text block
            if new_block:
                print(f"\n\nframe_{start_frame} to frame_{end_frame}\n")
                with open(os.path.join(dir_path, 'output.txt'), 'r') as out_file:
                    print(out_file.read())
                new_block = False

    with open(os.path.join(dir_path, 'output.txt'), 'r') as out_file:
        print(out_file.read())

sys.stdout = original_stdout # Reset the standard output to its original value
