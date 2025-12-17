import os
import re
import sys

# =================================================================
# CONFIGURATION
# =================================================================

# 1. Target Directory: The folder containing your processed, renamed images
TARGET_DIR = r'C:\Users\rival\Downloads\Dataset\Dataset\tortugas' 

# 2. ***CRITICAL***: SET THE MAXIMUM NUMBER OF IMAGES TO KEEP
# The script will delete the lowest-confidence images until this count is reached.
MAX_IMAGES_TO_KEEP = 10860 

# =================================================================
# CORE LOGIC
# =================================================================

def extract_confidence(filename):
    """
    Extracts the confidence score (the last sequence of digits before the extension) 
    from a filename using a regular expression.
    
    Expected format: [base_name]_[index]_[accuracy].jpg
    Example: mariquitas_00123_985.jpg -> returns 985 (for 98.5%)
    """
    # Regex to find the last sequence of digits before the file extension
    match = re.search(r'_(\d+)\.jpg$', filename, re.IGNORECASE)
    
    if match:
        # Convert the matched group (the accuracy score) to an integer
        return int(match.group(1))
    return -1 # Return -1 for files that don't match the expected format

def curate_dataset_by_count():
    """
    Scans the target directory, sorts files by confidence (low to high),
    and deletes files until MAX_IMAGES_TO_KEEP is reached.
    """
    if not os.path.isdir(TARGET_DIR):
        print(f"Error: Target directory '{TARGET_DIR}' not found. Please run the detection pipeline first. Exiting.")
        sys.exit(1)

    all_files = os.listdir(TARGET_DIR)
    
    # Filter for image files and extract confidence
    conf_files = []
    
    for filename in all_files:
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            confidence = extract_confidence(filename)
            if confidence >= 0:
                # Store as a tuple: (confidence_score, full_path)
                conf_files.append((confidence, os.path.join(TARGET_DIR, filename)))
            else:
                print(f"Warning: Skipping file '{filename}'. Could not parse confidence.")

    current_count = len(conf_files)
    
    if current_count <= MAX_IMAGES_TO_KEEP:
        print(f"\n--- Curation Skipped ---")
        print(f"Current count ({current_count}) is already less than or equal to the target count ({MAX_IMAGES_TO_KEEP}).")
        print("No files will be deleted.")
        sys.exit(0)

    # --- Deletion Calculation ---
    files_to_delete_count = current_count - MAX_IMAGES_TO_KEEP
    
    # 1. Sort files by confidence: lowest confidence comes first
    # Sorting by the first element of the tuple (confidence score)
    conf_files.sort(key=lambda x: x[0]) 

    # 2. Select the lowest-confidence files for deletion
    files_to_delete = conf_files[:files_to_delete_count]
    
    # Determine the cutoff confidence score (the score of the lowest kept file)
    # The first file we KEEP is at index files_to_delete_count
    cutoff_confidence = conf_files[files_to_delete_count][0]
    
    print(f"\n--- Dataset Curating Tool ---")
    print(f"Found {current_count} files. Target to keep: {MAX_IMAGES_TO_KEEP}")
    print(f"Confidence scores range from: {min(c for c, p in conf_files)} to {max(c for c, p in conf_files)} (e.g., 985 = 98.5%)")

    print(f"\n--- Deletion Plan ---")
    print(f"Total files to delete: {files_to_delete_count}")
    print(f"All files with confidence below {cutoff_confidence} (e.g., {cutoff_confidence/10:.1f}%) will be deleted.")
    print(f"Lowest deleted confidence: {files_to_delete[0][0]}")
    print(f"Highest deleted confidence: {files_to_delete[-1][0]}")
    
    confirm = input("Confirm automatic deletion? (Type 'yes' to proceed): ")
    
    if confirm.lower() == 'yes':
        deleted_count = 0
        for confidence, path in files_to_delete:
            try:
                os.remove(path)
                deleted_count += 1
            except OSError as e:
                print(f"Could not delete file {path}: {e}")
        
        print("\n--- Summary ---")
        print(f"Successfully deleted {deleted_count} files.")
        print(f"Files remaining in '{TARGET_DIR}': {current_count - deleted_count}")
        print("Operation complete.")
    else:
        print("Deletion cancelled by user.")

if __name__ == "__main__":
    curate_dataset_by_count()