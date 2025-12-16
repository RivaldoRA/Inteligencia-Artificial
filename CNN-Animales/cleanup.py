import os
import sys

# =================================================================
# CONFIGURATION (Matching your main script)
# =================================================================

# 1. Directory where the original, untouched images are
IMAGE_FOLDER = './hormigas_temp'

# 2. Directory where the AI placed its crops (where we look for IDs)
OUTPUT_FOLDER = './processed_high_confidence'

# 3. Directory to safely move the processed originals to (Use DONE_FOLDER to be safe)
DONE_FOLDER = './hormiguis_originales'

# 4. Prefix used in the original image filenames (e.g., 'hormigas_')
ORIGINAL_FILE_PREFIX = 'hormigas_'

# 5. Suffix used to denote a specific crop (e.g., '_c01', '_523', '_90')
# The script relies on the crop suffix starting with an underscore: '_523', '_90', etc.

# =================================================================
# MAIN CLEANUP LOGIC
# =================================================================

def cleanup_processed_originals(confidence_threshold=50):
    """
    Scans the OUTPUT_FOLDER, extracts original image IDs from cropped files 
    (based on the structure hormigas_05247_523), and moves the corresponding 
    original image to the DONE_FOLDER if its highest confidence crop meets the threshold.
    """
    
    if not os.path.isdir(IMAGE_FOLDER) or not os.path.isdir(OUTPUT_FOLDER) or not os.path.isdir(DONE_FOLDER):
        print("Error: One or more configuration folders do not exist.")
        print(f"Check: {IMAGE_FOLDER}, {OUTPUT_FOLDER}, {DONE_FOLDER}")
        sys.exit(1)

    print("--- Starting AI Processed Original Cleanup ---")
    print(f"Processing crops from: {OUTPUT_FOLDER}")
    print(f"Confidence Threshold: {confidence_threshold}%")
    
    # Dictionary to store the highest confidence score for each original image ID
    # { '05247': 90, '05248': 85, ... }
    original_id_scores = {}

    # 1. Scan AI Output Folder to find the highest confidence for each original image
    for filename in os.listdir(OUTPUT_FOLDER):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        try:
            # Expected structure: hormigas_05247_523.jpg
            parts = filename.split('_')
            
            # The original ID is usually the second-to-last part (e.g., '05247')
            # The confidence is the last part before the extension (e.g., '523')
            
            # Find the index of the first numeric part that is *not* the confidence score
            # This is fragile, so we rely on the known pattern.
            
            # Example: ['hormigas', '05247', '523.jpg']
            
            if len(parts) >= 3:
                # Assuming the structure is exactly 'prefix_ID_CONFIDENCE.ext'
                original_id = parts[-2]
                
                # Get the confidence score (the last part before the extension)
                confidence_str = parts[-1].split('.')[0]
                confidence_score = int(confidence_str)
                
                # Full unique ID for the original file: hormigas_05247
                full_original_id = f"{ORIGINAL_FILE_PREFIX}{original_id}"
                
                # Store the maximum confidence found for this original image ID
                current_max = original_id_scores.get(full_original_id, 0)
                original_id_scores[full_original_id] = max(current_max, confidence_score)

        except ValueError:
            print(f"Skipping malformed filename (ID/score not integer): {filename}")
        except IndexError:
            print(f"Skipping filename (structure not matched): {filename}")


    if not original_id_scores:
        print("No AI-cropped images with recognizable IDs found. Exiting.")
        return

    # 2. Iterate through the collected IDs and move the originals
    moved_count = 0
    
    for full_original_id, max_score in original_id_scores.items():
        
        # Check if the highest confidence score meets the threshold
        if max_score >= confidence_threshold:
            
            # We need to find the actual original file name, which could be .jpg, .png, etc.
            original_file_found = False
            
            for ext in ['.jpg', '.jpeg', '.png']:
                original_filename = f"{full_original_id}{ext}"
                original_path = os.path.join(IMAGE_FOLDER, original_filename)
                
                if os.path.exists(original_path):
                    
                    destination_path = os.path.join(DONE_FOLDER, original_filename)
                    
                    try:
                        os.rename(original_path, destination_path)
                        print(f"✅ MOVED: {original_filename} (Max Score: {max_score})")
                        moved_count += 1
                        original_file_found = True
                        break # Found and moved, go to the next ID
                    except OSError as e:
                        print(f"Error moving {original_filename}: {e}")
                        
            if not original_file_found:
                print(f"⚠️ NOT FOUND: Original file for ID {full_original_id} not found in {IMAGE_FOLDER}")

    print(f"\n--- Cleanup Complete ---")
    print(f"Total processed original images moved to {DONE_FOLDER}: {moved_count}")
    print(f"Total unique IDs checked: {len(original_id_scores)}")


if __name__ == "__main__":
    # You can change the confidence_threshold here. 
    # Only originals with a crop score of 90 or higher will be marked as 'done'.
    cleanup_processed_originals(confidence_threshold=90)