
#Sure, you can add a loop to check the last few lines of the previous file, starting from the very last line and going upwards. If a line doesn't exist in the next file, the loop continues to the line above, and so on. Here's how you can implement it:

# i have case

# 1.txt
# cast
# akash
# des


# 2.txt
# akash
# desai
# okoko

# here last line of 1.txt is des- so its going to check if its present in 2.txt
# its not present so it will give wrong output

# my ocr has done bymistake

# so i want my code to check last des is present in next txt , if not present thke second last txt & check if that present in 2.txt if its present follow the same logic

# my final output will be

# cast
# akash
# des
# desai
# okoko




import os
from Levenshtein import ratio

dir_path = '/content/demosimilarity'
txt_files = sorted([f for f in os.listdir(dir_path) if f.endswith('.txt')])

# Initialize output.txt with the first file's contents
with open(os.path.join(dir_path, txt_files[0]), 'r') as in_file, \
        open(os.path.join(dir_path, 'output.txt'), 'w') as out_file:
    out_file.write(in_file.read().strip() + '\n')

# Process the remaining files
for i, txt_file in enumerate(txt_files[1:]):
    with open(os.path.join(dir_path, 'output.txt'), 'r') as out_file:
        output_lines = out_file.readlines()

    with open(os.path.join(dir_path, txt_file), 'r') as in_file:
        in_lines = in_file.readlines()

        # Find the line index that contains the word most similar to one of the last words from the previous file
        max_ratio = 0.8  # You can adjust the threshold as needed
        start_idx = None
        for output_line in reversed(output_lines):  # Iterate over the lines in reverse order
            last_word = output_line.strip().split()[-1]
            for i, line in enumerate(in_lines):
                for word in line.split():
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
                if line not in output_lines:
                    out_file.write(line.strip() + '\n')

# Print the final output
with open(os.path.join(dir_path, 'output.txt'), 'r') as out_file:
    print(out_file.read())
