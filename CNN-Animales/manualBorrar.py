import cv2
import numpy as np
import os
import sys

# =================================================================
# CONFIGURATION
# =================================================================

# 1. Directory to load images from
IMAGE_FOLDER = './Datasets/FotosListas/tortugas' 

# 2. Batch/Pagination Parameters
BATCH_SIZE = 100          
GRID_COLS = 10            
IMAGE_SIZE = 150          

# 3. Visual Cues
STATUS_DELETE_COLOR = (0, 0, 255)  # BGR color for the 'Marked for Deletion' status (RED)
STATUS_KEEP_COLOR = (0, 255, 0)    # BGR color for the 'Kept' status (Green)
SELECTION_HIGHLIGHT_COLOR = (255, 255, 0) # BGR color for the temporary selection (CYAN/YELLOW)
BORDER_THICKNESS = 5


# =================================================================
# GLOBAL STATE & UTILITIES
# =================================================================

# Stored as: (file_path, is_marked_for_deletion, is_temporarily_selected)
all_file_status = [] 
current_batch_data = [] 
current_batch_start_index = 0

WINDOW_NAME = "Image Curator"
INFO_HEIGHT = 40
CELL_WIDTH = IMAGE_SIZE + BORDER_THICKNESS * 2
CELL_HEIGHT = IMAGE_SIZE + BORDER_THICKNESS * 2

# --- Helper Functions ---

def load_file_list():
    """Reads all file paths and initializes their deletion status."""
    global all_file_status
    
    if not os.path.isdir(IMAGE_FOLDER):
        print(f"Error: Directory '{IMAGE_FOLDER}' not found.")
        sys.exit(1)
        
    print(f"Reading file list from {IMAGE_FOLDER}...")
    
    file_names = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    file_names.sort() 
    
    if not file_names:
        print("No images found. Exiting.")
        sys.exit(0)

    # Initialize with False for marked (index 1) and False for temporary selection (index 2)
    all_file_status = [(os.path.join(IMAGE_FOLDER, f), False, False) for f in file_names]
    print(f"Total images found: {len(all_file_status)}")
    
    global BATCH_SIZE
    if BATCH_SIZE > len(all_file_status):
        BATCH_SIZE = len(all_file_status)

def load_current_batch(start_index):
    """Loads and resizes images for the current batch, clearing previous ones."""
    global current_batch_data, current_batch_start_index
    
    current_batch_data.clear()
    current_batch_start_index = start_index
    end_index = min(start_index + BATCH_SIZE, len(all_file_status))
    
    print(f"\nLoading batch: Indices {start_index} to {end_index - 1}")

    for i in range(start_index, end_index):
        # We only need the image data for the current batch. Status is read from all_file_status.
        file_path, _, _ = all_file_status[i] 
        
        img = cv2.imread(file_path)
        
        if img is not None:
            resized_img = cv2.resize(img, (IMAGE_SIZE, IMAGE_SIZE), interpolation=cv2.INTER_AREA)
            # Store [image_data]
            current_batch_data.append(resized_img) 
        else:
            placeholder = np.zeros((IMAGE_SIZE, IMAGE_SIZE, 3), dtype=np.uint8)
            cv2.putText(placeholder, "LOAD FAILED", (5, IMAGE_SIZE//2), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
            current_batch_data.append(placeholder)

def create_grid_image():
    """Generates the grid display from the currently loaded batch."""
    
    display_count = len(current_batch_data)
    grid_rows = int(np.ceil(display_count / GRID_COLS))
    
    grid_width = GRID_COLS * CELL_WIDTH
    grid_height = grid_rows * CELL_HEIGHT
    grid_img = np.full((grid_height + INFO_HEIGHT, grid_width, 3), 50, dtype=np.uint8) 

    # --- Draw Images and Borders ---
    for i, img in enumerate(current_batch_data):
        row = i // GRID_COLS
        col = i % GRID_COLS

        abs_index = current_batch_start_index + i
        
        # --- Retrieve Status from Global List ---
        _, is_marked, is_temp_selected = all_file_status[abs_index]
        
        # Cell and Image coordinates
        x_start_cell = col * CELL_WIDTH
        y_start_cell = row * CELL_HEIGHT + INFO_HEIGHT
        
        x_start_img = x_start_cell + BORDER_THICKNESS
        y_start_img = y_start_cell + BORDER_THICKNESS
        x_end_img = x_start_img + IMAGE_SIZE
        y_end_img = y_start_img + IMAGE_SIZE
        
        grid_img[y_start_img:y_end_img, x_start_img:x_end_img] = img

        # 1. STATUS border (Red/Green)
        status_color = STATUS_DELETE_COLOR if is_marked else STATUS_KEEP_COLOR
        cv2.rectangle(grid_img, 
                      (x_start_img - BORDER_THICKNESS, y_start_img - BORDER_THICKNESS), 
                      (x_end_img + BORDER_THICKNESS, y_end_img + BORDER_THICKNESS), 
                      status_color, 
                      BORDER_THICKNESS)
        
        # 2. SELECTION HIGHLIGHT (Cyan/Yellow) - ONLY draw if is_temporarily_selected is True
        if is_temp_selected:
            HIGHLIGHT_THICKNESS = 2 
            
            x_end_cell = x_start_cell + CELL_WIDTH
            y_end_cell = y_start_cell + CELL_HEIGHT
            
            cv2.rectangle(grid_img, 
                          (x_start_cell, y_start_cell), 
                          (x_end_cell, y_end_cell), 
                          SELECTION_HIGHLIGHT_COLOR, 
                          HIGHLIGHT_THICKNESS)

        # Draw absolute file index
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(grid_img, str(abs_index), (x_start_img, y_start_img - 10), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        
    # --- Draw Instructions and Status ---
    
    # Calculate how many are currently selected (marked True for is_temporarily_selected)
    selected_count = sum(1 for _, _, is_temp in all_file_status if is_temp)

    instructions = "[SPACE]: Toggle Delete Mark (Selected Images) | [Click]: Single Select | [CTRL+Click]: Toggle Multi-Select | [A/D]: Previous/Next Batch"
    status_text = f"Batch {current_batch_start_index//BATCH_SIZE + 1} of {len(all_file_status)//BATCH_SIZE + 1} | Total: {len(all_file_status)} | Selected Count: {selected_count}"
    
    grid_width = GRID_COLS * CELL_WIDTH
    cv2.putText(grid_img, instructions, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(grid_img, status_text, (grid_width - 350, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    return grid_img

def get_absolute_index(x, y):
    """Calculates absolute file index from screen coordinates (x, y)."""
    
    y_adjusted = y - INFO_HEIGHT
    
    col = x // CELL_WIDTH
    row = y_adjusted // CELL_HEIGHT
    
    index_in_view = row * GRID_COLS + col
    absolute_index = current_batch_start_index + index_in_view
    
    # Check bounds
    if absolute_index < len(all_file_status) and index_in_view < len(current_batch_data) and y_adjusted >= 0:
        return absolute_index
    return -1

# --- Mouse Callback (FIXED Logic) ---
def mouse_callback(event, x, y, flags, param):
    """Handles mouse clicks for single and multi-selection."""
    
    if event == cv2.EVENT_LBUTTONDOWN:
        abs_index = get_absolute_index(x, y)
        
        if abs_index != -1:
            is_multi_select = flags & (cv2.EVENT_FLAG_CTRLKEY | cv2.EVENT_FLAG_SHIFTKEY)
            path, is_marked, is_temp = all_file_status[abs_index]
            
            if is_multi_select:
                # CTRL+Click: Toggle the temporary selection flag
                all_file_status[abs_index] = (path, is_marked, not is_temp)
                
            else:
                # Single Click: Clear ALL previous temporary selections
                for i in range(len(all_file_status)):
                    p, m, t = all_file_status[i]
                    if t:
                        all_file_status[i] = (p, m, False)
                
                # Set the temporary selection flag for the clicked image
                # This ensures ONLY the clicked image is highlighted after a single click
                all_file_status[abs_index] = (path, is_marked, True)
            
            print(f"Clicked index: {abs_index}. Multi-select: {is_multi_select}. New Selected State: {all_file_status[abs_index][2]}")

def execute_deletion():
    """Deletes all files marked for deletion in the all_file_status list."""
    # Filter the list based on the 'marked' flag
    files_to_delete = [path for path, marked, _ in all_file_status if marked]
    
    if not files_to_delete:
        print("\nNo files were marked for deletion. Exiting.")
        return

    print(f"\n--- Deletion Summary ---")
    print(f"Total files marked for deletion: {len(files_to_delete)}")
    
    confirm = input("Are you sure you want to PERMANENTLY delete these files? (Type 'YES' to proceed): ")
    
    if confirm == 'YES':
        deleted_count = 0
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                deleted_count += 1
            except OSError as e:
                print(f"Error deleting {os.path.basename(file_path)}: {e}")
                
        print(f"\n✅ Finished. Successfully deleted {deleted_count} files.")
    else:
        print("Deletion cancelled.")

# --- Main Execution ---

def run_curator():
    global current_batch_start_index
    
    load_file_list()
    load_current_batch(0)

    cv2.namedWindow(WINDOW_NAME)
    cv2.setMouseCallback(WINDOW_NAME, mouse_callback)

    while True:
        
        # 1. Redraw the image based on the current state
        grid_img = create_grid_image()
        cv2.imshow(WINDOW_NAME, grid_img)
        
        key = cv2.waitKey(1) & 0xFF
        
        # --- Keyboard Handlers ---

        if key == 27: # ESC key: Quit and Execute Deletion
            break
        
        elif key == ord(' '): # SPACEBAR: Toggle Mark on Selected Images
            
            # Identify all indices that are temporarily selected
            selected_indices = [i for i, (_, _, is_temp) in enumerate(all_file_status) if is_temp]
            
            if selected_indices:
                # Determine the toggle action (new_status) based on the first selected item
                path, is_marked, is_temp = all_file_status[selected_indices[0]]
                new_status = not is_marked
                
                print(f"Toggling status of {len(selected_indices)} file(s) to: {'DELETE' if new_status else 'KEEP'}")

                # Apply the toggle to ALL selected images
                for i in selected_indices:
                    path, _, is_temp = all_file_status[i]
                    all_file_status[i] = (path, new_status, is_temp) # Update marked status
                
                # Re-load the current batch to refresh the grid visually 
                load_current_batch(current_batch_start_index)
                
        elif key == ord('d') or key == 83: # 'd' or Right Arrow: Next Batch
            if current_batch_start_index + BATCH_SIZE < len(all_file_status):
                current_batch_start_index += BATCH_SIZE
                load_current_batch(current_batch_start_index)
                
        elif key == ord('a') or key == 81: # 'a' or Left Arrow: Previous Batch
            if current_batch_start_index > 0:
                current_batch_start_index = max(0, current_batch_start_index - BATCH_SIZE)
                load_current_batch(current_batch_start_index)
                
    cv2.destroyAllWindows()
    execute_deletion()

if __name__ == "__main__":
    run_curator()