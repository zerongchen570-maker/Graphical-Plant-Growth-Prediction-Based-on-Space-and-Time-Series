import os
import shutil
from pathlib import Path

# ================= Config =================
SOURCE_ROOT = "/Users/zachx/Documents/plants_prediction/data"
OUTPUT_DIR = "/Users/zachx/Documents/plants_prediction/PlantDS_Merged/Seg"

DS1_NAME = "plant_ds1"
DS2_NAME = "plant_ds2"

# 1. Target folder name (must be segmentation masks)
TARGET_FOLDER_NAME = "segmented_images"

# 2. Filename keyword (must be top-down view)
REQUIRED_FILENAME_KEYWORD = "RGB1"

# 3. DS2 Time Filter: Keep noon (12) and afternoon (17) only
DS2_KEEP_HOURS = [12, 17] 
HOUR_MARGIN = 1 
# ===========================================

def setup_output_dir(path):
    p = Path(path)
    if p.exists():
        print(f"Cleaning output directory: {path}")
        shutil.rmtree(path)
    p.mkdir(parents=True, exist_ok=True)
    print(f"Output directory ready: {path}")

def get_image_hour(filename):
    """Parse hour from filename (Standard: Index 4)."""
    try:
        parts = filename.split('_')
        return int(parts[4])
    except (IndexError, ValueError):
        return -1

def is_target_file(filename, dataset_type):
    """Main filter logic."""
    
    # Basic check: Image extension + contains RGB1
    if not (filename.endswith('.png') or filename.endswith('.jpg')):
        return False
    if REQUIRED_FILENAME_KEYWORD not in filename:
        return False
            
    # DS2 specific: Time downsampling
    if dataset_type == "DS2":
        h = get_image_hour(filename)
        is_keep_time = False
        for target in DS2_KEEP_HOURS:
            if (target - HOUR_MARGIN) <= h <= (target + HOUR_MARGIN):
                is_keep_time = True
                break
        if not is_keep_time:
            return False
            
    return True

def process_dataset(ds_path, dataset_type, start_plant_id):
    print(f"\nScanning {dataset_type} in: {ds_path}")
    
    current_plant_id = start_plant_id
    total_groups_created = 0
    
    # Collect target folders
    valid_folders = []
    
    for root, dirs, files in os.walk(ds_path):
        # Strategy: Direct check if folder name matches target
        if os.path.basename(root) == TARGET_FOLDER_NAME:
            valid_folders.append(root)
    
    # Sort to ensure order
    valid_folders.sort()

    print(f"Found {len(valid_folders)} folders named '{TARGET_FOLDER_NAME}'.")

    for root in valid_folders:
        files = os.listdir(root)
        files.sort() # Time sort
        
        # Filter files
        valid_files = []
        for f in files:
            if is_target_file(f, dataset_type):
                valid_files.append(f)
        
        # Slice into chunks (groups of 10)
        chunk_size = 10
        for i in range(0, len(valid_files), chunk_size):
            chunk = valid_files[i : i + chunk_size]
            
            if len(chunk) == chunk_size:
                day_counter = 1
                for img_name in chunk:
                    src_file = os.path.join(root, img_name)
                    
                    # Naming: plant00001_day01.png
                    new_name = f"plant{current_plant_id:05d}_day{day_counter:02d}.png"
                    dst_file = os.path.join(OUTPUT_DIR, new_name)
                    
                    shutil.copy2(src_file, dst_file)
                    day_counter += 1
                
                current_plant_id += 1
                total_groups_created += 1

    print(f"Finished {dataset_type}.")
    print(f" -> Created {total_groups_created} new sequence groups.")
    return current_plant_id

# ================= Main =================

if __name__ == "__main__":
    setup_output_dir(OUTPUT_DIR)
    
    plant_ds1_path = os.path.join(SOURCE_ROOT, DS1_NAME)
    plant_ds2_path = os.path.join(SOURCE_ROOT, DS2_NAME)
    
    # Process DS1
    next_id = process_dataset(plant_ds1_path, "DS1", start_plant_id=1)
    
    print("-" * 30)
    print(f"DS1 processing done. Next Plant ID: {next_id}")
    print("-" * 30)
    
    # Process DS2
    final_id = process_dataset(plant_ds2_path, "DS2", start_plant_id=next_id)
    
    print("=" * 30)
    print(f"All processing complete!")
    print(f"Total Unique Sequences Generated: {final_id - 1}")
    print(f"Output saved to: {OUTPUT_DIR}")