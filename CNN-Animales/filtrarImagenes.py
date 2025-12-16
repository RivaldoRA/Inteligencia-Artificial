import pandas as pd
import requests
import os
import concurrent.futures
from PIL import Image
from ultralytics import YOLO
import numpy as np
import sys 

# =================================================================
# CONFIGURATION
# =================================================================

# 2. YOLO Model Path (LOAD YOUR TRAINED MODEL HERE)
#TRAINED_MODEL_PATH = "./ModelosYolo/cat.v2i.yolov11/runs/detect/cat_detection_local/weights/best.pt" 
TRAINED_MODEL_PATH = "./hormigas.pt" 

# 3. Processing Parameters
MIN_CONFIDENCE = 0.40        # Only keep images with detection confidence >= 75%
TARGET_SIZE = 224             
#MAX_WORKERS = 32*4
MAX_WORKERS = 256
TARGET_CLASS_ID = 0

# Directory Setup
PROCESSED_DIR = 'processed_high_confidence'
TEMP_DOWNLOAD_DIR = 'hormigas_temp'
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(TEMP_DOWNLOAD_DIR, exist_ok=True)

# =================================================================
# UTILITY FUNCTIONS (Download and Cleanup)
# =================================================================

def download_image(url, output_path):
    """Downloads an image from a URL and saves it."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, stream=True, timeout=15)
        response.raise_for_status() 

        with open(output_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        return True, output_path
    except requests.exceptions.RequestException as e:
        return False, f"Download failed for {url}: {e}"
    except Exception as e:
        return False, f"An unexpected error occurred for {url}: {e}"

def cleanup_temp_files(files):
    """Removes temporary downloaded files."""
    for file_path in files:
        if os.path.exists(file_path):
            os.remove(file_path)
    # Only remove the temp directory if it's empty
    if os.path.exists(TEMP_DOWNLOAD_DIR) and not os.listdir(TEMP_DOWNLOAD_DIR):
        os.rmdir(TEMP_DOWNLOAD_DIR)

# =================================================================
# STAGE 2: YOLO DETECTION, CROP, AND RENAME
# =================================================================

def process_image(file_path, model):
    """Runs YOLO, finds the highest-confidence detection, crops, and renames."""
    try:
        img = Image.open(file_path).convert("RGB")
        img_w, img_h = img.size

        # 1. Run YOLOv8 Detection with conf filtering
        # NOTE: Your trained model is for ladybugs. Ensure your images contain ladybugs.
        results = model(file_path, conf=MIN_CONFIDENCE, verbose=False)
        
        best_box = None
        best_conf = 0.0

        for r in results:
            for box in r.boxes:
                #conf = box.conf.item()
                conf = box.conf.item()
                cls_id = int(box.cls.item()) # Get the class ID

                    # ONLY PROCESS DETECTIONS THAT MATCH THE TARGET CLASS
                if cls_id == TARGET_CLASS_ID and conf > best_conf:
                    best_conf = conf
                    # xyxy format: [x1, y1, x2, y2]
                    best_box = [int(x) for x in box.xyxy[0].tolist()]

                
                # Identify the highest confidence detection
                #if conf > best_conf:
                #    best_conf = conf
                #    best_box = [int(x) for x in box.xyxy[0].tolist()]

        if best_box:
            # 2. Crop the image to a square around the detection (224x224)
            x1, y1, x2, y2 = best_box
            center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2
            
            det_w, det_h = x2 - x1, y2 - y1
            square_size = max(det_w, det_h) 

            # Calculate padded square crop coordinates (10% padding)
            padding = square_size * 0.10
            crop_size_padded = square_size + padding
            
            final_x1 = int(max(0, center_x - crop_size_padded / 2))
            final_y1 = int(max(0, center_y - crop_size_padded / 2))
            final_x2 = int(min(img_w, center_x + crop_size_padded / 2))
            final_y2 = int(min(img_h, center_y + crop_size_padded / 2))

            crop_box = (final_x1, final_y1, final_x2, final_y2)
            
            # Crop and resize to 224x224
            cropped_img = img.crop(crop_box)
            resized_img = cropped_img.resize((TARGET_SIZE, TARGET_SIZE), Image.Resampling.LANCZOS)
            
            # 3. Rename and Save
            # Confidence format: 0.985 -> 985
            conf_percent_str = f"{best_conf * 100:.1f}".replace('.', '') 
            file_id = os.path.splitext(os.path.basename(file_path))[0]
            
            # Output Name: original_file_id_985.jpg
            output_file_name = f"{file_id}_{conf_percent_str}.jpg"
            output_path = os.path.join(PROCESSED_DIR, output_file_name)
            resized_img.save(output_path)
            
            return True, best_conf
        
        else:
            return False, 0.0 # No detection above MIN_CONFIDENCE
            
    except Exception as e:
        # print(f"Error processing {file_path}: {e}")
        return False, 0.0


def main_pipeline():
    # This function is retained for clarity, but is commented out in __main__
    # The logic is correctly implemented in the `if __name__ == "__main__":` block 
    # to demonstrate the detection-only call.
    pass 
    
def detection_pipeline(downloaded_files, model):
    """
    Processes a list of downloaded image files using the YOLO model.
    Filters, crops, and renames images based on confidence.
    """
    total_downloaded = len(downloaded_files)
    total_files_processed = 0
    processed_count = 0

    print("\nStarting YOLO detection, cropping, and filtering...")
    
    for i, file_path in enumerate(downloaded_files):
        success, confidence = process_image(file_path, model)
        
        total_files_processed += 1
        if success:
            processed_count += 1
        
        if (i + 1) % 5000 == 0:
            print(f"[Processing] Progress: {i + 1}/{total_downloaded} files scanned. Kept: {processed_count}")

    
    # NOTE: The detection pipeline is now responsible for returning the results
    return total_files_processed, processed_count

if __name__ == "__main__":
    # Ensure dependencies are installed 
    os.system("pip install pandas requests Pillow ultralytics tqdm --quiet")
    
    # --- 1. Load Model ---
    print(f"Loading model from: {TRAINED_MODEL_PATH}")
    try:
        model = YOLO(TRAINED_MODEL_PATH)
    except Exception as e:
        print(f"\nFATAL ERROR: Could not load the trained model. Check the path: {TRAINED_MODEL_PATH}")
        sys.exit(1)

    # --- 2. Determine Already Processed Files (THE NEW LOGIC) ---
    processed_base_names = set()
    
    for filename in os.listdir(PROCESSED_DIR):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            # The processed file name is like: original_id_985.jpg
            # We want to extract 'original_id' which corresponds to the file in TEMP_DOWNLOAD_DIR
            
            # Find the last underscore followed by 3 digits (or 4, for the confidence score)
            parts = filename.rsplit('_', 1) 
            if len(parts) == 2:
                base_name = parts[0]
                # Re-add the extension to match the temp file naming convention
                original_filename = base_name + os.path.splitext(filename)[1] 
                processed_base_names.add(original_filename)
            else:
                # Handle files that don't match the expected naming convention (just in case)
                processed_base_names.add(filename)

    print(f"Found {len(processed_base_names)} files already successfully processed in '{PROCESSED_DIR}'.")
    
    # --- 3. Collect Downloaded Files and Filter ---
    print(f"Collecting files from temporary directory: {TEMP_DOWNLOAD_DIR}")
    
    if not os.path.isdir(TEMP_DOWNLOAD_DIR) or not os.listdir(TEMP_DOWNLOAD_DIR):
        print("\nERROR: Temporary download directory is empty or does not exist. Exiting.")
        sys.exit(1)
        
    all_temp_files = [f for f in os.listdir(TEMP_DOWNLOAD_DIR) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    # Filter out files that are already in the processed set
    downloaded_files_to_process = [
        os.path.join(TEMP_DOWNLOAD_DIR, f)
        for f in all_temp_files
        if f not in processed_base_names
    ]

    print(f"Total downloaded images found: {len(all_temp_files)}")
    print(f"Files to be processed in this run (Excluding previously processed): {len(downloaded_files_to_process)}")
    
    if not downloaded_files_to_process:
        print("All available downloaded images have already been processed. Nothing to do. Exiting.")
        sys.exit(0)

    # --- 4. Run Detection Pipeline ---
    total_files_scanned, total_files_kept = detection_pipeline(
        downloaded_files_to_process, 
        model
    )

    # --- 5. Final Summary ---
    print("\n========================================================")
    print("DETECTION-ONLY PIPELINE COMPLETE")
    print(f"Total files scanned in this run: {total_files_scanned}")
    print(f"Total high-confidence images (>= {MIN_CONFIDENCE*100:.0f}%) saved to '{PROCESSED_DIR}' in this run: {total_files_kept}")
    print(f"Total processed files now in '{PROCESSED_DIR}': {len(os.listdir(PROCESSED_DIR))}")
    print("========================================================")