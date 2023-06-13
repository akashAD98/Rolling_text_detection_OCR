## without frameinfo new added


import os
import re
from Levenshtein import ratio
from fuzzywuzzy import fuzz

def process_files(dir_path, log_file_path):
    txt_files = sorted([f for f in os.listdir(dir_path) if f.endswith('.txt')], key=lambda x: int(x.split('_')[1].split('.')[0]))
    frame_start = int(txt_files[0].split('_')[1].split('.')[0])
    frame_end = int(txt_files[0].split('_')[1].split('.')[0])

    with open(os.path.join(dir_path, txt_files[0]), 'r') as in_file, open(os.path.join(dir_path, 'output.txt'), 'w') as out_file:
        out_file.write(in_file.read().strip() + ' | from file: ' + txt_files[0] + '\n')

    output_lines_set = set()
    for i, txt_file in enumerate(txt_files[1:]):
        current_frame = int(txt_file.split('_')[1].split('.')[0])

        # Check if we're in a new frame interval
        if current_frame // 1000 > frame_end // 1000:
            frame_end = current_frame
            with open(os.path.join(dir_path, 'output.txt'), 'a') as out_file:
                out_file.write('\nframe_' + str(frame_start) + '.txt to frame_' + str(frame_end - 1) + '.txt\n')
            frame_start = frame_end

        with open(os.path.join(dir_path, 'output.txt'), 'r') as out_file:
            output_lines = out_file.readlines()
            for line in output_lines:
                output_lines_set.add(line.strip().split(' | ')[0].split(',')[0])

        with open(os.path.join(dir_path, txt_file), 'r') as in_file:
            in_lines = in_file.readlines()

            start_idx = None
            # first, check for exact matches
            for output_line in reversed(output_lines):
                last_word = output_line.strip().split(' | ')[0].split(',')[0]
                for i, line in enumerate(in_lines):
                    if last_word in line:
                        start_idx = i
                        break
                if start_idx is not None:
                    break

            # if no exact match is found, find most similar line
            if start_idx is None:
                max_ratio = 0.65
                for output_line in reversed(output_lines):
                    last_word = output_line.strip().split(' | ')[0].split(',')[0]
                    for i, line in enumerate(in_lines):
                        for word_bbox in line.split():
                            word = word_bbox.split(',')[0]
                            if ratio(last_word, word) > max_ratio:
                                max_ratio = ratio(last_word, word)
                                start_idx = i
                    if start_idx is not None:
                        break

            if start_idx is None:
                start_idx = 0

            with open(os.path.join(dir_path, 'output.txt'), 'a') as out_file:
                for line in in_lines[start_idx:]:
                    line_text = line.strip().split(',')[0]
                    if line_text not in output_lines_set:
                        out_file.write(line.strip() + ' | from file: ' + txt_file + '\n')
                        output_lines_set.add(line_text)

    with open(os.path.join(dir_path, 'output.txt'), 'a') as out_file:
        out_file.write('\nframe_' + str(frame_start) + '.txt to frame_' + str(frame_end) + '.txt\n')

    with open(os.path.join(dir_path, 'output.txt'), 'r') as out_file, open(log_file_path, 'w') as log_file:
        output = out_file.read()
        log_file.write(output)

        text_parts = [line.split(' | ')[0].split(',')[0] for line in output.split('\n')]
        full_lines = output.split('\n')

        i = 0
        while i < len(text_parts) - 1:
            similarity_ratio = fuzz.ratio(text_parts[i], text_parts[i + 1])
            if similarity_ratio > 70:
                removed_line = f"Removing line: {full_lines[i + 1]}\nBecause it's {similarity_ratio}% similar to: {full_lines[i]}\n"
                log_file.write(removed_line)
                print(removed_line)
                del text_parts[i + 1]
                del full_lines[i + 1]
            else:
                i += 1

        output = '\n'.join(full_lines)
        log_file.write('\n\nFinal output:\n' + output)

        with open(os.path.join(dir_path, 'finaloutput_withbbox_fileinfo.txt'), "w") as file:
            file.write(output)

        with open(os.path.join(dir_path, 'output_final.txt'), "w") as text_file, open(os.path.join(dir_path, 'output_final_withoutframeinfo.txt'), "w") as text_file_without_info:
            for line in output.split('\n'):
                text_part = line.split(' | ')[0].split(',')[0]
                text_file.write(text_part + '\n')
                # Exclude lines that match the frame interval pattern
                if not re.match(r'^frame_\d+\.txt to frame_\d+\.txt$', text_part.strip()):
                    text_file_without_info.write(text_part.split(' | ')[0] + '\n')

# Prompt the user to enter the folder path
folder_path = '/content/drive/MyDrive/zz_newocr/new_catme_txtbbdemo'
log_file_path = folder_path +'/ocrlog.log'

# Call the function to process the files
process_files(folder_path, log_file_path)


