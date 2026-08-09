from pathlib import Path
import shutil

seed_dir = Path("dataset/seed_dataset")
label_dir = Path("dataset/task_dataset/obj_train_data/seed_dataset")

jpg_map = {}

for img in seed_dir.rglob("*.jpg"):
    jpg_map[img.stem] = img

copied = 0

for txt in label_dir.rglob("*.txt"):
    if txt.name == "train.txt":
        continue

    if txt.stem in jpg_map:
        shutil.copy2(
            jpg_map[txt.stem],
            txt.parent / f"{txt.stem}.jpg"
        )
        copied += 1

print(f"Copied {copied} images")
