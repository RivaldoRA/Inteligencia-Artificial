import pandas as pd
import requests
import os
import concurrent.futures
import sys 

# =================================================================
# CONFIGURATION
# =================================================================

# 1. ***CRITICAL***: DEFINE YOUR SINGLE CSV FILE HERE
CSV_FILE_PATH = './Datasets/AmazonCSV/gatos.csv' 
URL_COLUMN_NAME = 'identifier'       # Column in your CSV containing the image URLs (Verify this name!)
DOWNLOAD_LIMIT = 50000         # Target number of images from this single CSV
MAX_WORKERS = 64               # Threads for parallel downloading

# Directory Setup
TEMP_DOWNLOAD_DIR = 'temp_downloads'
os.makedirs(TEMP_DOWNLOAD_DIR, exist_ok=True)

# =================================================================
# UTILITY FUNCTION (Download)
# =================================================================

def download_image(url, output_path):
    """Downloads an image from a URL and saves it."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        # Use 'stream=True' to handle large files efficiently
        response = requests.get(url, headers=headers, stream=True, timeout=15)
        response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)

        with open(output_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        return True, output_path
    except requests.exceptions.RequestException as e:
        return False, f"Download failed for {url}: {e}"
    except Exception as e:
        return False, f"An unexpected error occurred for {url}: {e}"

# =================================================================
# MAIN EXECUTION BLOCK (Download Only)
# =================================================================

def main_download_pipeline():
    # Ensure dependencies are installed 
    os.system("pip install pandas requests --quiet")

    csv_path = CSV_FILE_PATH
    print(f"\n\n========================================================")
    print(f"STARTING IMAGE DOWNLOAD PIPELINE for: {csv_path}")
    print(f"Target directory: {TEMP_DOWNLOAD_DIR}")
    print(f"========================================================")

    # 1. Read CSV and prepare download tasks
    try:
        df = pd.read_csv(csv_path)
        # Sample or take the top N rows, limiting to DOWNLOAD_LIMIT
        sample_df = df.sample(n=min(DOWNLOAD_LIMIT, len(df)), random_state=42)
        urls = sample_df[URL_COLUMN_NAME].tolist()
    except Exception as e:
        print(f"FATAL ERROR: Could not read or sample from CSV at {csv_path}. Details: {e}")
        sys.exit(1)

    download_tasks = []
    # Prepare the list of (URL, desired_output_path) tuples
    for i, url in enumerate(urls):
        # Create a unique file name based on CSV name and index
        file_name = f"{os.path.basename(csv_path).replace('.csv', '')}_{i:05d}.jpg"
        output_path = os.path.join(TEMP_DOWNLOAD_DIR, file_name)
        download_tasks.append((url, output_path))

    downloaded_files = []
    print(f"Initiating parallel download of {len(download_tasks)} URLs using {MAX_WORKERS} workers...")
    
    # 2. Execute parallel download
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(download_image, url, path) for url, path in download_tasks]
        
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            success, result = future.result()
            if success:
                downloaded_files.append(result)
            else:
                # Optional: Print error for failed downloads
                # print(f"Failure: {result}")
                pass
            
            # Simple progress update
            if (i + 1) % 5000 == 0:
                 print(f"[Download] Progress: {i + 1}/{len(download_tasks)}. Successes: {len(downloaded_files)}")

    total_downloaded = len(downloaded_files)
    total_failed = len(download_tasks) - total_downloaded
    
    print("\n========================================================")
    print("DOWNLOAD PIPELINE COMPLETE")
    print(f"Total URLs processed: {len(download_tasks)}")
    print(f"Successfully downloaded: {total_downloaded}")
    print(f"Failed downloads: {total_failed}")
    print(f"Files saved to: {TEMP_DOWNLOAD_DIR}")
    print("========================================================")

if __name__ == "__main__":
    # The 'if __name__ == "__main__":' guard is crucial for safe multiprocessing on Windows.
    main_download_pipeline()