import os

dir_path = '/content/drive/MyDrive/ocr/5img_op'
txt_files = sorted([f for f in os.listdir(dir_path) if f.endswith('.txt')])

# initialize output.txt with the first file's contents
with open(os.path.join(dir_path, txt_files[0]), 'r') as in_file, \
        open(os.path.join(dir_path, 'output.txt'), 'w') as out_file:
    out_file.write(in_file.read().strip() + '\n')

# process the remaining files
for txt_file in txt_files[1:]:
    with open(os.path.join(dir_path, 'output.txt'), 'r') as out_file:
        last_line = out_file.readlines()[-1].strip()

    with open(os.path.join(dir_path, txt_file), 'r') as in_file:
        in_lines = in_file.readlines()

        # skip lines until the last line from output.txt is found
        start_idx = 0
        for i, line in enumerate(in_lines):
            if line.strip() == last_line:
                start_idx = i + 1
                break

        # append the remaining lines to output.txt
        with open(os.path.join(dir_path, 'output.txt'), 'a') as out_file:
            out_file.write('\n'.join(in_lines[start_idx:]).strip() + '\n')

# print the final output
with open(os.path.join(dir_path, 'output.txt'), 'r') as out_file:
    print(out_file.read())
