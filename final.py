## all code


import os
import shutil
from Levenshtein import ratio
from fuzzywuzzy import fuzz

def find_start_index(in_lines, output_lines, output_lines_set):
    start_idx = None
    for output_line in reversed(output_lines):
        last_word = output_line.strip().split(' | ')[0].split(',')[0]
        for i, line in enumerate(in_lines):
            if last_word in line:
                start_idx = i
                break
        if start_idx is not None:
            break

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

    return start_idx if start_idx is not None else 0

def write_output_lines(in_lines, start_idx, output_lines_set, out_file, txt_file):
    new_output_lines = []
    for line in in_lines[start_idx:]:
        line_text = line.strip().split(',')[0]
        if line_text not in output_lines_set:
            out_line = line.strip() + ' | from file: ' + txt_file
            out_file.write(out_line + '\n')
            new_output_lines.append(out_line)
            output_lines_set.add(line_text)
    return new_output_lines, output_lines_set

def remove_similar_lines(text_parts, full_lines, log_file):
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

def write_final_outputs(output, output_folder):
    with open(os.path.join(output_folder, 'finaloutput_withbbox_fileinfo.txt'), "w") as file:
        file.write(output)

    with open(os.path.join(output_folder, 'output_final.txt'), "w") as text_file:
        for line in output.split('\n'):
            text_part = line.split(' | ')[0].split(',')[0]
            text_file.write(text_part + '\n')

def process_files(dir_path, log_file_path, output_folder, frame_interval):
    txt_files = sorted([f for f in os.listdir(dir_path) if f.endswith('.txt')], key=lambda x: int(x.split('_')[-1].split('.')[0]))

    output_file_path = os.path.join(output_folder, 'output.txt')
    output_file_path_with_interval = os.path.join(output_folder, 'output_withframe_interval.txt')

    output_lines = []
    output_lines_set = set()

    for i in range(0, len(txt_files), frame_interval):
        txt_file_group = txt_files[i: i + frame_interval]

        with open(output_file_path_with_interval, 'a') as out_file:
            out_file.write(f'from {txt_file_group[0]} to {txt_file_group[-1]}:\n')
            for txt_file in txt_file_group:
                with open(os.path.join(dir_path, txt_file), 'r') as in_file:
                    in_lines = in_file.readlines()

                    start_idx = find_start_index(in_lines, output_lines, output_lines_set)
                    new_output_lines, new_output_lines_set = write_output_lines(in_lines, start_idx, output_lines_set, out_file, txt_file)
                    output_lines += new_output_lines
                    output_lines_set = output_lines_set.union(new_output_lines_set)
            out_file.write('\n')

    with open(output_file_path, 'w') as out_file:
        out_file.write('\n'.join(output_lines))

    with open(log_file_path, 'w') as log_file:
        output = '\n'.join(output_lines)
        log_file.write(output)

        text_parts = [line.split(' | ')[0].split(',')[0] for line in output.split('\n')]
        full_lines = output.split('\n')

        remove_similar_lines(text_parts, full_lines, log_file)

        output = '\n'.join(full_lines)
        log_file.write('\n\nFinal output:\n' + output)

        write_final_outputs(output, output_folder)

def main():
    folder_path = '/content/INP'
    output_folder = os.path.join(folder_path, 'output')
    log_file_path = os.path.join(output_folder, 'ocr_alllog.log')

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    os.makedirs(output_folder, exist_ok=True)
    
    frame_interval = 4  # change this to the desired frame interval
    process_files(folder_path, log_file_path, output_folder, frame_interval)

if __name__ == "__main__":
    main()
