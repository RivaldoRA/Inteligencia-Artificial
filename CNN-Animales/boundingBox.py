import cv2
import numpy as np
import os
import sys

# =================================================================
# CONFIGURATION
# =================================================================

# 1. Directory to load images from
IMAGE_FOLDER = './hormigas_temp'

# 2. Output directory for cropped images
# Setting this to IMAGE_FOLDER will overwrite the originals or save new files here. 
OUTPUT_FOLDER = './hormiguis' 


DONE_FOLDER = './hormiguis_originales' 

# 3. Target output resolution (Fixed for deep learning input)
TARGET_RESOLUTION = (224, 224) 

# 4. Maximum display size for the main window (to fit most monitors)
MAX_DISPLAY_WIDTH = 1200
MAX_DISPLAY_HEIGHT = 800

# 5. Window Names
MAIN_WINDOW_NAME = "Image Cropper (Original)"
PREVIEW_WINDOW_NAME = f"Cropped Preview ({TARGET_RESOLUTION[0]}x{TARGET_RESOLUTION[1]} px)"


# =================================================================
# GLOBAL STATE
# =================================================================

image_files = []        
current_file_index = 0
current_img = None      
current_img_bgr = None  
drag_start = None       
drag_end = None         
is_dragging = False
scaling_factor = 1.0    
display_img = None      
crop_counter = 0        


# =================================================================
# UTILITY FUNCTIONS
# =================================================================

def load_file_list():
    """Reads all image file paths."""
    global image_files
    
    if not os.path.isdir(IMAGE_FOLDER):
        print(f"Error: Directory '{IMAGE_FOLDER}' not found.")
        sys.exit(1)
        
    if not os.path.isdir(OUTPUT_FOLDER):
        print(f"Creating output directory: '{OUTPUT_FOLDER}'")
        os.makedirs(OUTPUT_FOLDER)
        
    if not os.path.isdir(DONE_FOLDER):
        print(f"Creating output directory: '{DONE_FOLDER}'")
        os.makedirs(DONE_FOLDER)
        
    print(f"Reading file list from {IMAGE_FOLDER}...")
    
    file_names = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    file_names.sort() 
    
    if not file_names:
        print("No images found. Exiting.")
        sys.exit(0)

    image_files = [os.path.join(IMAGE_FOLDER, f) for f in file_names]
    print(f"Total images found: {len(image_files)}")

# =================================================================
# UTILITY FUNCTIONS
# =================================================================

# ... (Insert this function after get_original_coords) ...

def move_file_to_done(file_path):
    """Moves the processed file from IMAGE_FOLDER to DONE_FOLDER."""
    global image_files, current_file_index
    
    file_name = os.path.basename(file_path)
    destination_path = os.path.join(DONE_FOLDER, file_name)
    
    try:
        os.rename(file_path, destination_path)
        print(f"📦 Moved original file to DONE: {file_name}")
        
        # Remove the file from our active list
        image_files.pop(current_file_index)
        
        # Adjust index to avoid skipping the next file
        if current_file_index >= len(image_files) and len(image_files) > 0:
            current_file_index = 0 
        elif len(image_files) == 0:
            current_file_index = 0 
            
        return True
    except OSError as e:
        print(f"Error moving file {file_name} to DONE: {e}")
        return False

# ... (rest of UTILITY FUNCTIONS) ...

def load_image(index):
    """Loads a new image based on the index, ensuring it fits the monitor."""
    global current_img, current_img_bgr, drag_start, drag_end
    global scaling_factor, display_img, is_dragging, current_file_index, crop_counter
    
    if not image_files:
        current_img = None
        return
        
    # Ensure index loops
    current_file_index = index % len(image_files)
    
    file_path = image_files[current_file_index]
    
    # 1. Load Original Image
    current_img = cv2.imread(file_path)
    
    if current_img is None:
        print(f"Warning: Could not load image {file_path}. Skipping.")
        current_img_bgr = None
        return

    # 2. Determine Scaling Factor for Display
    original_h, original_w, _ = current_img.shape
    
    scale_w = MAX_DISPLAY_WIDTH / original_w
    scale_h = MAX_DISPLAY_HEIGHT / (original_h + 50) # +50 for instructions text margin
    
    scaling_factor = min(scale_w, scale_h)
    
    # Ensure we don't scale up small images (max scale is 1.0)
    if scaling_factor > 1.0:
        scaling_factor = 1.0
        
    # 3. Create Display Image
    display_w = int(original_w * scaling_factor)
    display_h = int(original_h * scaling_factor)
    display_img = cv2.resize(current_img, (display_w, display_h), interpolation=cv2.INTER_AREA)

    # 4. Reset Drawing State and Crop Counter for the NEW image
    current_img_bgr = display_img.copy()
    drag_start = None
    drag_end = None
    is_dragging = False
    crop_counter = 0 
    
    print(f"\nLoaded image {current_file_index+1}/{len(image_files)}: {os.path.basename(file_path)}. Original Size: {original_w}x{original_h}, Display Size: {display_w}x{display_h}")


def get_original_coords(x, y):
    """Converts display coordinates back to original image coordinates."""
    
    original_x = int(x / scaling_factor)
    original_y = int(y / scaling_factor)
    
    if current_img is not None:
        h, w, _ = current_img.shape
        original_x = max(0, min(original_x, w))
        original_y = max(0, min(original_y, h))

    return original_x, original_y

# =================================================================
# DRAWING AND INTERACTION
# =================================================================

def draw_image():
    """Draws the current image with the bounding box."""
    global current_img_bgr
    
    if current_img is None:
        drawn_img = np.zeros((MAX_DISPLAY_HEIGHT, MAX_DISPLAY_WIDTH, 3), dtype=np.uint8)
        text = "No images loaded or image list empty." if not image_files else "Image loading failed. Skipping."
        cv2.putText(drawn_img, text, (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.imshow(MAIN_WINDOW_NAME, drawn_img)
        return
        
    drawn_img = display_img.copy()

    if drag_start and drag_end:
        cv2.rectangle(drawn_img, drag_start, drag_end, (0, 255, 255), 2)
        
    # Updated instructions
    instructions = "[S]: Save Crop & Next | [C]: Save New Crop (Same Img) | [CTRL+R]: Resize Full Img & Next | [SPACE]: DELETE | [A/D]: Next/Prev"
    cv2.putText(drawn_img, instructions, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
    current_img_bgr = drawn_img
    cv2.imshow(MAIN_WINDOW_NAME, drawn_img)

def create_preview(start_coord, end_coord):
    """Generates the cropped and RESIZED preview image."""
    
    if current_img is None:
        return None
        
    x_start_orig, y_start_orig = get_original_coords(start_coord[0], start_coord[1])
    x_end_orig, y_end_orig = get_original_coords(end_coord[0], end_coord[1])
    
    x1 = min(x_start_orig, x_end_orig)
    y1 = min(y_start_orig, y_end_orig)
    x2 = max(x_start_orig, x_end_orig)
    y2 = max(y_start_orig, y_end_orig)
    
    cropped_img = current_img[y1:y2, x1:x2]
    
    if cropped_img.size == 0 or (x2 - x1) < 10 or (y2 - y1) < 10:
        return None
        
    output_resized = cv2.resize(cropped_img, TARGET_RESOLUTION, interpolation=cv2.INTER_AREA)

    cv2.imshow(PREVIEW_WINDOW_NAME, output_resized)
    
    return output_resized

def mouse_callback(event, x, y, flags, param):
    """Handles mouse drawing events, enforcing a square bounding box."""
    global drag_start, drag_end, is_dragging
    
    if current_img is None:
        return
        
    if event == cv2.EVENT_LBUTTONDOWN:
        is_dragging = True
        drag_start = (x, y)
        drag_end = (x, y)
        
    elif event == cv2.EVENT_MOUSEMOVE:
        if is_dragging:
            dx = x - drag_start[0]
            dy = y - drag_start[1]
            
            size = max(abs(dx), abs(dy))
            
            new_x = drag_start[0] + (size if dx > 0 else -size)
            new_y = drag_start[1] + (size if dy > 0 else -size)
            
            drag_end = (new_x, new_y)
            
            draw_image()
            if drag_start != drag_end:
                create_preview(drag_start, drag_end)
            
    elif event == cv2.EVENT_LBUTTONUP:
        is_dragging = False
        draw_image()
        if drag_start != drag_end:
            create_preview(drag_start, drag_end)
            
def save_crop(move_next=False, save_as_new=False):
    """Saves the current bounding box crop."""
    global current_file_index, crop_counter
    
    if not drag_start or not drag_end:
        print("Please draw a bounding box first.")
        return False
        
    final_output = create_preview(drag_start, drag_end)
    
    if final_output is None:
        print("Invalid crop area or box not drawn correctly.")
        return False
        
    original_path = image_files[current_file_index]
    file_name = os.path.basename(original_path)
    base_name, ext = os.path.splitext(file_name)
    
    if save_as_new:
        crop_counter += 1
        new_file_name = f"{base_name}_c{crop_counter:02d}{ext}"
        save_path = os.path.join(OUTPUT_FOLDER, new_file_name)
        status_msg = f"Saved new crop ({crop_counter}): {new_file_name}"
    else:
        new_file_name = f"{base_name}{ext}" # Use the base name without a crop counter
        save_path = os.path.join(OUTPUT_FOLDER, new_file_name)
        status_msg = f"Overwrote original file: {file_name}"
    
    cv2.imwrite(save_path, final_output)
    print(f"✅ {status_msg} at {TARGET_RESOLUTION[0]}x{TARGET_RESOLUTION[1]} px.")
    
    if move_next:
        move_file_to_done(original_path)
        current_file_index = (current_file_index + 1) % len(image_files)
        load_image(current_file_index)
        
    return True

# --- NEW FUNCTION FOR FULL IMAGE RESIZE ---
def resize_full_image():
    """Takes the entire current image, resizes it to 224x224, saves, and moves next."""
    global current_file_index
    
    if current_img is None:
        print("Error: No image loaded to resize.")
        return False

    # 1. Resize the ENTIRE original image to the target resolution
    resized_img = cv2.resize(current_img, TARGET_RESOLUTION, interpolation=cv2.INTER_AREA)

    # 2. Determine save path (always overwrites the original file for simplicity)
    original_path = image_files[current_file_index]
    save_path = original_path
    file_name = os.path.basename(original_path)

    # 3. Save the image
    cv2.imwrite(save_path, resized_img)
    print(f"🖼️ Full image resized and saved (overwritten) at {TARGET_RESOLUTION[0]}x{TARGET_RESOLUTION[1]} px: {file_name}")

    # 4. Move to the next image
    current_file_index = (current_file_index + 1) % len(image_files)
    load_image(current_file_index)
    
    return True

def delete_current_image():
    """Deletes the current file and removes it from the list."""
    global image_files, current_file_index, current_img

    if not image_files:
        print("Cannot delete: Image list is empty.")
        return False
        
    file_path_to_delete = image_files[current_file_index]
    
    try:
        os.remove(file_path_to_delete)
        print(f"🗑️ Permanently deleted file: {os.path.basename(file_path_to_delete)}")
        
        image_files.pop(current_file_index)
        
        if current_file_index >= len(image_files) and len(image_files) > 0:
            current_file_index = 0 
        elif len(image_files) == 0:
            current_file_index = 0 
        
        return True
    except OSError as e:
        print(f"Error deleting file {os.path.basename(file_path_to_delete)}: {e}")
        return False

# =================================================================
# MAIN CURATOR LOOP (Updated to check for CTRL flag)
# =================================================================

def run_cropper():
    """Main function to run the visual cropping tool."""
    global current_file_index, current_img
    
    load_file_list()
    if not image_files:
        print("No images found. Exiting.")
        return

    cv2.namedWindow(MAIN_WINDOW_NAME, cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback(MAIN_WINDOW_NAME, mouse_callback)
    cv2.namedWindow(PREVIEW_WINDOW_NAME, cv2.WINDOW_AUTOSIZE)
    
    current_file_index = 0
    load_image(current_file_index)

    while True:
        
        draw_image()
        
        if not image_files:
            cv2.waitKey(100) 
            break
            
        key = cv2.waitKey(1)
        
        # Check for CTRL key (flag 2 is CV_EVENT_FLAG_CTRLKEY) and isolate the key code
        # The key is bitwise ANDed with 0xFF to get the character code, regardless of flags
        char_code = key & 0xFF
        is_ctrl_pressed = key & 0x080000 # On some systems/OpenCV versions, CTRL adds a large flag value
        
        if char_code == 27: # ESC key: Quit
            break
        
        # --- Handle CTRL + R (Full Resize) ---
        # Note: The 'R' character code is 18 in some console contexts, but we use the character code 'r' here
        if char_code == ord('r') and is_ctrl_pressed:
            resize_full_image()

        elif char_code == ord(' '): # SPACEBAR: DELETE FILE and move to next
            if delete_current_image():
                if image_files:
                    load_image(current_file_index)
                else:
                    current_img = None
                    continue

        elif char_code == ord('s'): # 'S': Save and OVERWRITE (move to next image)
            save_crop(move_next=True, save_as_new=False)

        elif char_code == ord('c'): # 'C': Save as NEW FILE (stay on current image)
            save_crop(move_next=False, save_as_new=True)

        elif char_code == ord('d') or char_code == 83: # 'd' or Right Arrow: Next Image (Skip)
            current_file_index = (current_file_index + 1) % len(image_files)
            load_image(current_file_index)
                
        elif char_code == ord('a') or char_code == 81: # 'a' or Left Arrow: Previous Image (Skip)
            current_file_index = (current_file_index - 1) % len(image_files)
            load_image(current_file_index)
                
    cv2.destroyAllWindows()
    print("Exiting Image Cropper.")

if __name__ == "__main__":
    run_cropper()