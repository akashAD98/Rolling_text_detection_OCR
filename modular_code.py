import os
import shutil
from Levenshtein import ratio
from fuzzywuzzy import fuzz

def process_files(dir_path, log_file_path, output_folder):
    txt_files = sorted([f for f in os.listdir(dir_path) if f.endswith('.txt')], key=lambda x: int(x.split('_')[1].split('.')[0]))

    output_file_path = os.path.join(output_folder, 'output.txt')
    with open(os.path.join(dir_path, txt_files[0]), 'r') as in_file, open(output_file_path, 'w') as out_file:
        out_file.write(in_file.read().strip() + ' | from file: ' + txt_files[0] + '\n')

    output_lines_set = set()
    for i, txt_file in enumerate(txt_files[1:]):
        with open(output_file_path, 'r') as out_file:
            output_lines = out_file.readlines()
            for line in output_lines:
                output_lines_set.add(line.strip().split(' | ')[0].split(',')[0])

        with open(os.path.join(dir_path, txt_file), 'r') as in_file:
            in_lines = in_file.readlines()

            start_idx = find_start_index(in_lines, output_lines, output_lines_set)

            with open(output_file_path, 'a') as out_file:
                write_output_lines(in_lines, start_idx, output_lines_set, out_file, txt_file)

    with open(output_file_path, 'r') as out_file, open(log_file_path, 'w') as log_file:
        output = out_file.read()
        log_file.write(output)

        text_parts = [line.split(' | ')[0].split(',')[0] for line in output.split('\n')]
        full_lines = output.split('\n')

        remove_similar_lines(text_parts, full_lines, log_file)

        output = '\n'.join(full_lines)
        log_file.write('\n\nFinal output:\n' + output)

        write_final_outputs(output, output_folder)

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
    for line in in_lines[start_idx:]:
        line_text = line.strip().split(',')[0]
        if line_text not in output_lines_set:
            out_file.write(line.strip() + ' | from file: ' + txt_file + '\n')
            output_lines_set.add(line_text)

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

def main():
    #print("Please enter the folder path:")
    folder_path = '/content/drive/MyDrive/zz_newocr/new_catme_txtbbox'

    output_folder = os.path.join(folder_path, 'output')
    log_file_path = os.path.join(output_folder, 'ocr_all.log')

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    os.makedirs(output_folder, exist_ok=True)

    process_files(folder_path, log_file_path, output_folder)

if __name__ == "__main__":
    main()
