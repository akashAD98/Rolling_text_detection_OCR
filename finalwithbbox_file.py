import os
from Levenshtein import ratio

dir_path = '/content/n_bbox'
txt_files = sorted([f for f in os.listdir(dir_path) if f.endswith('.txt')])

# Initialize output.txt with the first file's contents
with open(os.path.join(dir_path, txt_files[0]), 'r') as in_file, \
        open(os.path.join(dir_path, 'output.txt'), 'w') as out_file:
    out_file.write(in_file.read().strip() + ' | from file: ' + txt_files[0] + '\n')

output_lines_set = set()

# Process the remaining files
for i, txt_file in enumerate(txt_files[1:]):
    with open(os.path.join(dir_path, 'output.txt'), 'r') as out_file:
        output_lines = out_file.readlines()
        for line in output_lines:
            output_lines_set.add(line.strip().split(' | ')[0].split(',')[0])  # Add only text part to set

    with open(os.path.join(dir_path, txt_file), 'r') as in_file:
        in_lines = in_file.readlines()

        # Find the line index that contains the word most similar to one of the last words from the previous file
        max_ratio = 0.65  # You can adjust the threshold as needed
        start_idx = None
        for output_line in reversed(output_lines):  # Iterate over the lines in reverse order
            last_word = output_line.strip().split(' | ')[0].split(',')[0]
            for i, line in enumerate(in_lines):
                for word_bbox in line.split():
                    word = word_bbox.split(',')[0]
                    if ratio(last_word, word) > max_ratio:
                        max_ratio = ratio(last_word, word)
                        start_idx = i
            if start_idx is not None:  # If a similar word was found, stop the loop
                break

        # If no similar word was found, set start_idx to 0
        if start_idx is None:
            start_idx = 0

        # Append the remaining lines to output.txt, skipping the ones already present
        with open(os.path.join(dir_path, 'output.txt'), 'a') as out_file:
            for line in in_lines[start_idx:]:
                line_text = line.strip().split(',')[0]  # Extract text part of line
                if line_text not in output_lines_set:  # Check if text part is already in output
                    out_file.write(line.strip() + ' | from file: ' + txt_file + '\n')
                    output_lines_set.add(line_text)  # Add text part to set

# Print the final output
with open(os.path.join(dir_path, 'output.txt'), 'r') as out_file:
    print(out_file.read())
