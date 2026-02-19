
import os
from pathlib import Path

dataset_root = Path("d:/Build2-hackthon/Dataset/Combined")

def rename_split(split_name):
    img_dir = dataset_root / split_name / "images"
    lbl_dir = dataset_root / split_name / "labels"
    
    if not img_dir.exists():
        print(f"Skipping {split_name} (not found)")
        return

    print(f"Renaming files in {split_name}...")
    
    # Get all images
    images = list(img_dir.glob("*.[jp][pn][g]")) # jpg, png
    
    for idx, img_path in enumerate(images):
        # Create new stem
        new_stem = f"{split_name}_{idx:05d}"
        new_img_name = f"{new_stem}{img_path.suffix}"
        new_img_path = img_dir / new_img_name
        
        # Rename image
        try:
            img_path.rename(new_img_path)
            
            # Rename corresponding label
            lbl_path = lbl_dir / f"{img_path.stem}.txt"
            if lbl_path.exists():
                new_lbl_name = f"{new_stem}.txt"
                new_lbl_path = lbl_dir / new_lbl_name
                lbl_path.rename(new_lbl_path)
        except OSError as e:
            print(f"Error renaming {img_path.name}: {e}")

for split in ["train", "valid", "test"]:
    rename_split(split)

print("Renaming complete.")
