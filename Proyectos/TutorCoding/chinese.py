import json
import re

def contains_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fff]')
    return bool(pattern.search(text))

def filter_jsonl_file(input_path, output_path):
    """
    Reads a file line-by-line. 
    Saves the entry only if it contains NO Chinese.
    """
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        
        kept_count = 0
        removed_count = 0
        
        for line in infile:
            if line.strip():  # Skip empty lines
                if contains_chinese(line):
                    removed_count += 1
                else:
                    outfile.write(line)
                    kept_count += 1
                    
    print(f"Finished! Kept: {kept_count}, Removed: {removed_count}")

# Usage
filter_jsonl_file('tutor_dataset.jsonl', 'cleaned_dataset.jsonl')