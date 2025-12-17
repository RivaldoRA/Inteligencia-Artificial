import os
import cv2
import albumentations as A

# =================================================================
# CONFIGURATION
# =================================================================
BASE_DIR = r'C:\Users\rival\Downloads\Dataset\Dataset'
CATEGORIES = ['gato', 'perros', 'tortugas', 'mariquitas', 'hormigas']
OUTPUT_DIR = r'C:\Users\rival\Downloads\Dataset\Augmented_85'
AUG_PER_IMAGE = 5 
TARGET_SIZE = (85, 85) # Updated to 150x150

# =================================================================
# AUGMENTATION PIPELINE
# =================================================================
transform = A.Compose([
    # Step 1: Resize to the specific target size
    A.Resize(TARGET_SIZE[0], TARGET_SIZE[1]),
    
    # Step 2: Spatial augmentations
    A.HorizontalFlip(p=0.5),
    A.RandomRotate90(p=0.5),
    A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.1, rotate_limit=45, p=0.5),
    
    # Step 3: Brightness, Contrast, and Color adjustments
    A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.7),
    A.RGBShift(r_shift_limit=15, g_shift_limit=15, b_shift_limit=15, p=0.3),
])

def run_augmentation():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for category in CATEGORIES:
        input_path = os.path.join(BASE_DIR, category)
        output_path = os.path.join(OUTPUT_DIR, category)
        
        if not os.path.exists(input_path):
            print(f"Directory not found: {input_path}")
            continue
            
        os.makedirs(output_path, exist_ok=True)
        print(f"Processing category: {category}")
        
        images = [f for f in os.listdir(input_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        for img_name in images:
            image_path = os.path.join(input_path, img_name)
            image = cv2.imread(image_path)
            
            if image is None:
                print(f"Could not read: {img_name}")
                continue
                
            # Convert BGR (OpenCV default) to RGB for Albumentations
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            for i in range(AUG_PER_IMAGE):
                augmented = transform(image=image)["image"]
                
                # Convert back to BGR to save using OpenCV
                save_img = cv2.cvtColor(augmented, cv2.COLOR_RGB2BGR)
                save_name = f"aug_{i}_{img_name}"
                cv2.imwrite(os.path.join(output_path, save_name), save_img)

    print(f"\nFinished. Dataset expanded and normalized to {TARGET_SIZE}.")

if __name__ == "__main__":
    run_augmentation()