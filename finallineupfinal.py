import os
from Levenshtein import ratio
from fuzzywuzzy import fuzz

def process_files(dir_path, log_file_path):
    #txt_files = sorted([f for f in os.listdir(dir_path) if f.endswith('.txt')])
    # frame_1.txt ,frame_2.txt --- sorted
    
    txt_files = sorted([f for f in os.listdir(dir_path) if f.endswith('.txt')], key=lambda x: int(x.split('_')[1].split('.')[0]))

    #txt_files = sorted([f for f in os.listdir(dir_path) if f.endswith('.txt')], key=lambda x: int(x.split('_')[1].split('.')[0]))


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

    # Print the final output and save it to the log file
    with open(os.path.join(dir_path, 'output.txt'), 'r') as out_file, \
            open(log_file_path, 'w') as log_file:
        output = out_file.read()
        print(output)
        log_file.write(output)

        # Extract only the text part from each line
        text_parts = [line.split(' | ')[0].split(',')[0] for line in output.split('\n')]

        # Compare two consecutive text parts and remove one if they are more than 70% similar
        i = 0
        while i < len(text_parts) - 1:
            similarity_ratio = fuzz.ratio(text_parts[i], text_parts[i + 1])
            if similarity_ratio > 70:
                removed_line = f"Removing line: {output.splitlines()[i + 1]}\nBecause it's {similarity_ratio}% similar to: {output.splitlines()[i]}\n"
                print(removed_line)
                print("______")
                log_file.write(removed_line)
                del text_parts[i + 1]
                output = '\n'.join(output.splitlines()[:i + 1] + output.splitlines()[i + 2:])
            else:
                i += 1

        # Save the final output to a file
        with open(os.path.join(dir_path, 'final_output.txt'), "w") as file:
            file.write(output)

        # Now generate output_last_final.txt
        final_output_lines = output.splitlines()
        last_final_output_lines = []


        for line in final_output_lines:
            parts = line.split(' | ')
            # parts[0] is the part before ' | ', which is text and bbox information
            text_bbox_parts = parts[0].split(',')
            text_part = text_bbox_parts[0]  # First part before ',' is text
            if len(parts) > 1:
                file_part = parts[1].replace('from file: ', '')  # Remove 'from file: ' from file part
            else:
                file_part = ''  # Default value if 'from file: ' part is missing
            #last_final_output_line = f"{text_part} | from file: {file_part}"
            last_final_output_line = f"{text_part}"
            last_final_output_lines.append(last_final_output_line)

        with open(os.path.join(dir_path, 'output_last_final.txt'), 'w') as file:
            file.write('\n'.join(last_final_output_lines))

# Prompt the user to enter the folder path
folder_path = '/content/op'
log_file_path = folder_path +'/ocrlog.log'

# Call the function to process the files
process_files(folder_path, log_file_path)
