import shutil
from pathlib import Path
from app.services.dataset.config import (
   IMAGES_DIR,
   LABELS_DIR,
)

class DatasetBuilder:
   def __init__(self):
       self.images_dir = IMAGES_DIR
       self.labels_dir = LABELS_DIR
   def build(self, splits):
       print("\n" + "=" * 60)
       print("BUILDING FINAL DATASET")
       print("=" * 60)
       self.prepare_directories()
       self.copy_split("train", splits["train"])
       self.copy_split("val", splits["val"])
       self.copy_split("test", splits["test"])
       print("\n✓ Final Dataset Created")
   def prepare_directories(self):
       if self.images_dir.exists():
           shutil.rmtree(self.images_dir)
       if self.labels_dir.exists():
           shutil.rmtree(self.labels_dir)
       for split in ["train", "val", "test"]:
           (self.images_dir / split).mkdir(
               parents=True,
               exist_ok=True
           )
           (self.labels_dir / split).mkdir(
               parents=True,
               exist_ok=True
           )
   def copy_split(self, split_name, images):
       copied = 0
       for image in images:
           label = image.with_suffix(".txt")
           if not label.exists():
               continue
           shutil.copy2(
               image,
               self.images_dir / split_name / image.name
           )
           shutil.copy2(
               label,
               self.labels_dir / split_name / label.name
           )
           copied += 1
       print(f"{split_name.capitalize()} : {copied} images")

