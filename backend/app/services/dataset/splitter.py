import random
import shutil
from pathlib import Path
from app.services.dataset.config import (
   CVAT_EXPORT_DIR,
   TRAIN_IMAGES_DIR,
   VAL_IMAGES_DIR,
   TEST_IMAGES_DIR,
   TRAIN_LABELS_DIR,
   VAL_LABELS_DIR,
   TEST_LABELS_DIR,
   TRAIN_SPLIT,
   VAL_SPLIT,
   RANDOM_SEED,
)

class DatasetSplitter:
   def __init__(self):
       random.seed(RANDOM_SEED)
       self.source = CVAT_EXPORT_DIR
   def split(self):
       print("\n" + "=" * 60)
       print("BUILDING TRAIN / VAL / TEST DATASET")
       print("=" * 60)
       images = list(self.source.rglob("*.jpg"))
       images += list(self.source.rglob("*.jpeg"))
       images += list(self.source.rglob("*.png"))
       print(f"Images Found : {len(images)}")
       random.shuffle(images)
       total = len(images)
       train_end = int(total * TRAIN_SPLIT)
       val_end = train_end + int(total * VAL_SPLIT)
       train = images[:train_end]
       val = images[train_end:val_end]
       test = images[val_end:]
       self.prepare_folders()
       self.copy_dataset(train, TRAIN_IMAGES_DIR, TRAIN_LABELS_DIR)
       self.copy_dataset(val, VAL_IMAGES_DIR, VAL_LABELS_DIR)
       self.copy_dataset(test, TEST_IMAGES_DIR, TEST_LABELS_DIR)
       print(f"Train : {len(train)}")
       print(f"Val   : {len(val)}")
       print(f"Test  : {len(test)}")
       return {
           "train": train,
           "val": val,
           "test": test
       }
   def prepare_folders(self):
       folders = [
           TRAIN_IMAGES_DIR,
           VAL_IMAGES_DIR,
           TEST_IMAGES_DIR,
           TRAIN_LABELS_DIR,
           VAL_LABELS_DIR,
           TEST_LABELS_DIR,
       ]
       for folder in folders:
           if folder.exists():
               shutil.rmtree(folder)
           folder.mkdir(parents=True, exist_ok=True)
   def copy_dataset(self, images, image_destination, label_destination):
       for image in images:
           label = image.with_suffix(".txt")
           shutil.copy2(
               image,
               image_destination / image.name
           )
           if label.exists():
               shutil.copy2(
                   label,
                   label_destination / label.name
               )
