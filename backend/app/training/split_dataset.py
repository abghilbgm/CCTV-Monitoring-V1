from pathlib import Path
import random
import shutil
import yaml
# -------------------------------------------------------
# Configuration
# -------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET = PROJECT_ROOT / "dataset" / "auto_annotations"
IMAGES = DATASET / "images" / "train"
LABELS = DATASET / "labels" / "train"
TRAIN_RATIO = 0.80
VAL_RATIO = 0.10
TEST_RATIO = 0.10
random.seed(42)
# -------------------------------------------------------
# Collect images
# -------------------------------------------------------
images = sorted(IMAGES.glob("*.jpg"))
print(f"Found {len(images)} images")
random.shuffle(images)
total = len(images)
train_end = int(total * TRAIN_RATIO)
val_end = train_end + int(total * VAL_RATIO)
train_images = images[:train_end]
val_images = images[train_end:val_end]
test_images = images[val_end:]
print(f"Train : {len(train_images)}")
print(f"Val   : {len(val_images)}")
print(f"Test  : {len(test_images)}")
# -------------------------------------------------------
# Create folders
# -------------------------------------------------------
for split in ["train", "val", "test"]:
   (DATASET / "images" / split).mkdir(parents=True, exist_ok=True)
   (DATASET / "labels" / split).mkdir(parents=True, exist_ok=True)

def move_files(image_list, split):
   for img in image_list:
       label = LABELS / f"{img.stem}.txt"
       shutil.move(
           str(img),
           str(DATASET / "images" / split / img.name)
       )
       if label.exists():
           shutil.move(
               str(label),
               str(DATASET / "labels" / split / label.name)
           )

# -------------------------------------------------------
# Move dataset
# -------------------------------------------------------
move_files(train_images, "train")
move_files(val_images, "val")
move_files(test_images, "test")
# -------------------------------------------------------
# Remove old folders
# -------------------------------------------------------
try:
   IMAGES.rmdir()
except:
   pass
try:
   LABELS.rmdir()
except:
   pass
# -------------------------------------------------------
# Update data.yaml
# -------------------------------------------------------
yaml_file = DATASET / "data.yaml"
with open(yaml_file) as f:
   data = yaml.safe_load(f)
data["train"] = "images/train"
data["val"] = "images/val"
data["test"] = "images/test"
with open(yaml_file, "w") as f:
   yaml.dump(data, f, sort_keys=False)
print("\nDataset split completed successfully.")
