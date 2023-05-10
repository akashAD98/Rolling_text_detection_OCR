##############   working correctly #########

import os

dir_path = '/content/drive/MyDrive/ocr/txt_testing_rolling'
txt_files = sorted([f for f in os.listdir(dir_path) if f.endswith('.txt')])

# initialize output.txt with the first file's contents
with open(os.path.join(dir_path, txt_files[0]), 'r') as in_file, \
        open(os.path.join(dir_path, 'output.txt'), 'w') as out_file:
    out_file.write(in_file.read().strip() + '\n')

# process the remaining files
for i, txt_file in enumerate(txt_files[1:]):
    with open(os.path.join(dir_path, 'output.txt'), 'r') as out_file:
        last_word = out_file.readlines()[-1].strip().split()[-1]  # get last word of last line

    with open(os.path.join(dir_path, txt_file), 'r') as in_file:
        in_lines = in_file.readlines()

        # find the line index that contains the last word from the previous file
        start_idx = next((i for i, line in enumerate(in_lines) if last_word in line), 0)

        # append the remaining lines to output.txt
        with open(os.path.join(dir_path, 'output.txt'), 'a') as out_file:
            out_file.write('\n'.join(in_lines[start_idx:]).strip() + '\n')

# print the final output
with open(os.path.join(dir_path, 'output.txt'), 'r') as out_file:
    print(out_file.read())

######## doblble txt but working correctly- last line last word logic
